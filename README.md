<h1>🕷️ SEO JavaScriptCrawler by IncRev</h1>

SEO JavaScriptCrawler by https://IncRev.co is a powerful, asynchronous, and scalable web crawler built with Playwright that fully renders and analyzes JavaScript-powered content on modern websites — a feature most traditional SEO tools lack.

<h2>🔍 Why JavaScript Crawling Matters for SEO</h2>

Today’s websites rely heavily on JavaScript frameworks like React, Vue, and Angular to generate critical content such as navigation links, product listings, and metadata. If your crawler doesn’t render JavaScript, you’re missing the real DOM — and making SEO decisions based on incomplete data.

<h3>Googlebot renders JavaScript before indexing. Your crawler should too.</h3>

**🚀 Features**

✅ Full JavaScript rendering with Playwright and stealth mode (avoids bot detection)
✅ Detects whether a page includes JS and lists all <script> sources (inline & external)
✅ Analyzes internal and external links (including dynamically inserted links)
✅ Image auditing: counts images and flags missing alt tags
✅ Detects lazy-loaded images without src (broken or unhydrated images)
✅ Flags pages that require SSR or preload to display critical content
✅ Extracts JS-rendered menus and dynamic navigation
✅ Monitors DOM for client-side injections (menus, dropdowns, content)
✅ Parses and respects robots.txt for ethical crawling
✅ Asynchronous architecture with multiple parallel workers for speed
✅ Persistent SQLite database with resumable crawling
✅ Exports to Excel (.xlsx) for advanced SEO reporting and visualization

<h2>🧠 What Makes IncRev’s JavaScript Crawler Unique?</h2>

IncRev’s SEO JavaScriptCrawler gives you deep visibility into what search engines really see when crawling your site — not just raw HTML, but fully rendered content.

**With this tool, you can:**

Detect JS-dependent content and identify where preload or SSR is needed
Find broken lazy-loaded images that never get hydrated
Audit the difference between static and dynamic SEO structure
Flag missing image alt attributes, non-crawlable menus, and injected links
Analyze large-scale websites with resume capability and persistence
⚙️ Installation

pip install -r requirements.txt
playwright install

**▶️ How to Use**

python crawler.py
You’ll be prompted to enter:

A start URL (e.g. https://example.com)
The maximum number of pages to crawl
After the crawl, your results are exported to:

example.com_crawl_results.xlsx

**📊 Excel Output Includes**

URL	Has JavaScript	JavaScript Sources	Internal Links	External Links	Image Count	Images Missing Alt	Lazy Broken Images	Nav Elements	JS-Specific Images	Needs SSR
Perfect for auditing with Excel, Google Sheets, Power BI, or Data Studio.

<h2>🧪 New Features in IncRev SEO JavaScript Crawler (Update 2025-06-15)</h2>

**✅ JavaScript-rendered Elements**
Crawls and discovers JS-rendered links, menus, and images
Executes client-side JavaScript to fully build the DOM
Captures dynamically injected elements such as:
Lazy-loaded images
SPA navigation components
JavaScript-created links in widgets or menus

**⚠️ Lazy Load Image Warnings**
Flags images using data-src or data-lazy without valid src
Identifies images that fail to load due to broken lazy-load logic
Logged as "Lazy Broken Images" in the report

**🔎 SSR / Preload Recommendation**
Flags pages where critical content (e.g. H1, .main-content) is missing unless JavaScript is rendered
Marks such pages with "Needs SSR" in the report

**🧪 Sample JSON Output (from internal structure)**

"DOMInfo": {
  "jsRenderedLinks": [
    "https://www.example.com/features",
    "https://www.example.com/contact"
  ],
  "jsRenderedImages": [
    "/img/hero-dynamic.jpg",
    "/img/avatar-lazy.png"
  ],
  "jsRenderedMenus": [
    {
       "id": "mainNav",
       "items": ["/home", "/about", "/blog"]
    }
  ]
}
<h2>🔐 Ethical Use of the JavaScript Crawler</h2>

SEO JavaScriptCrawler by IncRev strictly follows robots.txt directives and is designed for ethical SEO auditing. You are responsible for ensuring your usage complies with legal and website terms.

**🧭 Coming Soon**

Structured data (schema.org) extraction
Core Web Vitals auditing (via Lighthouse)
DOM diff between raw HTML and rendered DOM
Google Search Console & Ahrefs integration

<h3>💬 About IncRev</h3>

IncRev (Incredible Revenue AB) is a global SEO agency operating in 40+ countries, specializing in:

International link building
AI-powered SEO automation
JavaScript SEO diagnostics
Technical SEO audits at scale
We help SEO and marketing teams uncover hidden revenue opportunities — often buried deep inside JavaScript-driven websites.

<h3>🔑 SEO Keywords</h3>

SEO crawler, JavaScript SEO audit, IncRev SEO tool, technical SEO crawler,
SEO JavaScript rendering, Playwright SEO tool, scalable SEO crawler,
lazy load SEO audit, SSR SEO, JavaScript crawler, IncRev, SEO automation
