import asyncio
import openpyxl
import aiosqlite

from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright, Error
from robotexclusionrulesparser import RobotExclusionRulesParser
import aiohttp
from playwright_stealth import stealth_async

# --- CONFIGURATION ---
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
# ---------------------

class DatabaseManager:
    """Manages all database operations for the crawler."""
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    async def connect(self):
        self.conn = await aiosqlite.connect(self.db_name)

    async def close(self):
        await self.conn.close()

    async def setup_tables(self):
        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS queue (
                id INTEGER PRIMARY KEY, 
                url TEXT UNIQUE
            )
        ''')
        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS visited (
                id INTEGER PRIMARY KEY, 
                url TEXT UNIQUE
            )
        ''')
        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY, 
                url TEXT, 
                has_js BOOLEAN, 
                js_sources TEXT,
                internal_links INTEGER,
                external_links INTEGER,
                image_count INTEGER,
                images_missing_alt INTEGER,
                nav_elements_count INTEGER,
                js_specific_image_count INTEGER
            )
        ''')
        await self.conn.commit()

    async def add_to_queue(self, url):
        await self.conn.execute('INSERT OR IGNORE INTO queue (url) VALUES (?)', (url,))
        await self.conn.commit()

    async def get_from_queue(self):
        async with self.conn.execute('SELECT id, url FROM queue LIMIT 1') as cursor:
            row = await cursor.fetchone()
        if row:
            await self.conn.execute('DELETE FROM queue WHERE id = ?', (row[0],))
            await self.conn.commit()
            return row[1]
        return None

    async def add_to_visited(self, url):
        """Tries to add a URL to the visited set. Returns True if added, False if it already existed."""
        cursor = await self.conn.execute('INSERT OR IGNORE INTO visited (url) VALUES (?)', (url,))
        await self.conn.commit()
        return cursor.rowcount > 0

    async def get_visited_count(self):
        async with self.conn.execute('SELECT COUNT(*) FROM visited') as cursor:
            return (await cursor.fetchone())[0]

    async def save_result(self, url, has_js, js_sources, internal_links, external_links, image_count, images_missing_alt, nav_elements_count, js_specific_image_count):
        js_sources_str = ", ".join(js_sources)
        await self.conn.execute(
            'INSERT INTO results (url, has_js, js_sources, internal_links, external_links, image_count, images_missing_alt, nav_elements_count, js_specific_image_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (url, has_js, js_sources_str, internal_links, external_links, image_count, images_missing_alt, nav_elements_count, js_specific_image_count)
        )
        await self.conn.commit()

    async def get_all_results(self):
        async with self.conn.execute('SELECT url, has_js, js_sources, internal_links, external_links, image_count, images_missing_alt, nav_elements_count, js_specific_image_count FROM results') as cursor:
            return await cursor.fetchall()

    async def is_queue_empty(self):
        async with self.conn.execute('SELECT 1 FROM queue LIMIT 1') as cursor:
            return await cursor.fetchone() is None

class RobotsTxtHandler:
    _parsers = {}
    async def is_allowed(self, url):
        domain = urlparse(url).netloc
        if domain not in self._parsers:
            robots_url = urljoin(url, '/robots.txt')
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(robots_url, headers={'User-Agent': USER_AGENT}) as response:
                        if response.status == 200:
                            rules = await response.text()
                            parser = RobotExclusionRulesParser()
                            parser.parse(rules)
                            self._parsers[domain] = parser
                        else: self._parsers[domain] = None
            except Exception as e:
                print(f"Could not fetch robots.txt for {domain}: {e}")
                self._parsers[domain] = None
        parser = self._parsers.get(domain)
        return parser.is_allowed(USER_AGENT, url) if parser else True

class AsyncCrawler:
    """A scalable, persistent, asynchronous web crawler."""
    def __init__(self, start_url, max_pages, num_crawlers, db_name):
        self.start_url = start_url
        self.domain = urlparse(start_url).netloc # Keep original for reference if needed
        self.normalized_domain = self.domain.replace('www.', '')
        self.max_pages = max_pages
        self.num_crawlers = num_crawlers
        self.db = DatabaseManager(db_name)
        self.robots_handler = RobotsTxtHandler()
        self._crawl_finished = asyncio.Event()

    async def _extract_js_info(self, page):
        script_tags = await page.query_selector_all('script')
        js_sources = []
        for tag in script_tags:
            src = await tag.get_attribute('src')
            js_sources.append(urljoin(page.url, src) if src else "Inline JavaScript")
        return bool(js_sources), js_sources

    async def _worker(self, playwright_context):
        page = await playwright_context.new_page()
        await stealth_async(page)
        while not self._crawl_finished.is_set() and await self.db.get_visited_count() < self.max_pages:
            url = await self.db.get_from_queue()
            if not url:
                await asyncio.sleep(1) # Wait for more URLs
                continue

            # Atomically add the URL to the visited set. If it was already there, skip it.
            was_added = await self.db.add_to_visited(url)
            if not was_added:
                continue

            if not await self.robots_handler.is_allowed(url):
                continue
            
            try:
                visited_count = await self.db.get_visited_count()
                percentage = (visited_count / self.max_pages) * 100
                print(f"[{percentage:3.0f}%] Crawling page {visited_count}/{self.max_pages}: {url}")
                
                await page.goto(url, timeout=30000, wait_until='networkidle')

                has_js, js_list = await self._extract_js_info(page)

                # --- SEO Data Extraction & Link Discovery ---
                print(f"    [DEBUG] Worker for {url}: Starting link extraction.")
                links = await page.query_selector_all('a')
                print(f"    [DEBUG] Worker for {url}: Found {len(links)} <a> tags.")
                internal_links_count = 0
                external_links_count = 0
                
                for i, link_tag in enumerate(links):
                    href = await link_tag.get_attribute('href')
                    print(f"    [DEBUG] Worker for {url}: Link {i+1}/{len(links)} raw href: '{href}'")
                    if not href or href.strip().startswith('#') or href.strip().lower().startswith('javascript:'):
                        print(f"    [DEBUG] Worker for {url}: Link {i+1} skipped (empty, anchor, or JS link).")
                        continue
                    
                    abs_url = urljoin(url, href.strip())
                    link_domain_normalized = urlparse(abs_url).netloc.replace('www.', '')
                    print(f"    [DEBUG] Worker for {url}: Link {i+1} abs_url: '{abs_url}', normalized_link_domain: '{link_domain_normalized}', self.normalized_domain: '{self.normalized_domain}'")

                    if link_domain_normalized == self.normalized_domain:
                        internal_links_count += 1
                        await self.db.add_to_queue(abs_url)
                        print(f"    [DEBUG] Worker for {url}: Link {i+1} classified INTERNAL, added to queue: {abs_url}")
                    else:
                        external_links_count += 1
                        print(f"    [DEBUG] Worker for {url}: Link {i+1} classified EXTERNAL.")
                
                print(f"    [DEBUG] Worker for {url}: Finished link extraction. Internal links found on page: {internal_links_count}, External: {external_links_count}")

                images = await page.query_selector_all('img')
                image_count = len(images)
                images_missing_alt = 0
                for img in images:
                    alt = await img.get_attribute('alt')
                    if not alt or not alt.strip():
                        images_missing_alt += 1

                # --- JS-rendered content extraction (User Request) ---
                nav_elements = await page.query_selector_all('nav, [role="navigation"], .menu, .navbar')
                nav_elements_count = len(nav_elements)

                # Selectors for images specifically loaded/defined by JS (e.g. lazy-loaded, data URIs)
                js_specific_images = await page.query_selector_all('img[data-src], img[src^="data:"], img[src^="blob:"]')
                js_specific_image_count = len(js_specific_images)
                # --- End JS-rendered content extraction ---

                await self.db.save_result(
                    url, has_js, js_list,
                    internal_links_count, external_links_count,
                    image_count, images_missing_alt,
                    nav_elements_count, js_specific_image_count
                )

            except Error as e:
                print(f"Playwright error on {url}: {e}")
            except Exception as e:
                print(f"Error processing {url}: {e}")
        await page.close()

    async def _monitor(self):
        """Monitors the crawl and signals completion when the queue is empty."""
        while not self._crawl_finished.is_set():
            if await self.db.is_queue_empty() or await self.db.get_visited_count() >= self.max_pages:
                print("Monitor: Queue is empty or page limit reached. Waiting to confirm...")
                await asyncio.sleep(5) # Wait to see if workers add new URLs
                if await self.db.is_queue_empty() or await self.db.get_visited_count() >= self.max_pages:
                    print("Monitor: Confirming crawl completion. Signaling workers to stop.")
                    self._crawl_finished.set()
                    break
            await asyncio.sleep(2)

    async def run(self):
        await self.db.connect()
        await self.db.setup_tables()

        if await self.db.is_queue_empty() and await self.db.get_visited_count() == 0:
            print("Queue is empty and no pages visited. Seeding with start URL.")
            await self.db.add_to_queue(self.start_url)
        else:
            print("Resuming previous crawl.")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent=USER_AGENT)
            
            worker_tasks = [self._worker(context) for _ in range(self.num_crawlers)]
            monitor_task = self._monitor()
            
            await asyncio.gather(*worker_tasks, monitor_task)
            
            await context.close()
            await browser.close()
        await self.db.close()

    async def save_to_excel(self, filename="crawl_results.xlsx"):
        await self.db.connect()
        results = await self.db.get_all_results()
        await self.db.close()

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Crawl Results"
        sheet.append([
            "URL", "Has JavaScript", "JavaScript Sources",
            "Internal Links", "External Links", "Total Image Count", "Images Missing Alt Text",
            "Nav Elements Found", "JS-Specific Images"
        ])

        for row in results:
            sheet.append(row)

        workbook.save(filename)
        print(f"\nResults saved to {filename}")



async def main():
    # --- GET USER INPUT ---
    print("--- Python Web Crawler ---")
    start_url = input("Enter the starting URL to crawl (e.g., https://toscrape.com/): ")
    if not (start_url.startswith('http://') or start_url.startswith('https://')):
        print("Invalid URL. Please include http:// or https://")
        return

    while True:
        try:
            max_pages_str = input("Enter the maximum number of pages to crawl: ")
            max_pages = int(max_pages_str)
            if max_pages <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    # --- CONFIGURATION ---
    num_crawlers = 4  # Default number of workers

    # Generate database and output filenames from URL
    domain = urlparse(start_url).netloc.replace('www.', '')
    db_name = f"{domain}.db"
    output_filename = f"{domain}_crawl_results.xlsx"

    print(f"\n--- Starting Crawler ---")
    print(f"URL: {start_url}")
    print(f"Max Pages: {max_pages}")
    print(f"Workers: {num_crawlers}")
    print(f"Database: {db_name}")
    print(f"Output File: {output_filename}")
    print("------------------------")

    crawler = AsyncCrawler(start_url, max_pages=max_pages, num_crawlers=num_crawlers, db_name=db_name)
    await crawler.run()
    await crawler.save_to_excel(output_filename)

if __name__ == "__main__":
    asyncio.run(main())
