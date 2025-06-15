<H1>SEO JavaScriptCrawler by IncRev</H1>
SEO JavaScriptCrawler by https://IncRev.co is a powerful, asynchronous, and scalable web crawler built with Playwright that detects and analyzes JavaScript content on web pages – a critical feature that most traditional SEO audit tools lack.

<H2>🔍 JavaScript Crawler - Why does this matter for SEO?</H2>
Modern websites increasingly rely on JavaScript frameworks like React, Vue, and Angular. This means essential SEO elements such as internal links, metadata, and page content are dynamically rendered. Tools that don’t render JavaScript often miss major parts of a site’s actual structure, leading to incomplete audits and suboptimal SEO decisions.

**🚀 Features**

✅ JavaScript rendering via Playwright with stealth mode enabled

✅ Detects whether a page includes JavaScript and lists all script sources (inline + external)

✅ Full internal/external link analysis

✅ Image analysis with missing alt tag detection (a common SEO issue)

✅ Automatic robots.txt parsing and respectful crawling

✅ Asynchronous crawling with multiple workers for speed

✅ Persistent SQLite database with Excel export for in-depth SEO reporting

✅ Resumable crawling — designed for large-scale audits and robustness

<H2>🎯 What makes IncRev’s SEO JavaScript crawler unique?</H2>
🧠 With IncRev’s SEO JavaScriptCrawler, you get deep technical visibility into how Google and other search engines perceive your JavaScript-powered site.

**💡 This is not just another crawl tool – it’s a purpose-built SEO crawler that reveals:**

Pages that rely on JavaScript for full functionality

Technical SEO issues such as missing alt attributes, empty links, or hidden content

The contrast between static vs. dynamic SEO content

**🛠️ Installation**
bash
pip install -r requirements.txt
Install Playwright and its supported browsers:

bash
playwright install

**⚙️ How to Use**
bash
python crawler.py
Enter your start URL (e.g., https://example.com)

Enter max number of pages to crawl

Results are saved as an Excel file: example.com_crawl_results.xlsx

**📊 Output (Excel)**
URL	Has JavaScript	JavaScript Sources	Internal Links	External Links	Image Count	Images Missing Alt
https://example.com	✅	/main.js, /analytics.js	14	3	12	5

Perfect for further SEO analysis in Excel, Google Sheets, or visualization tools.

**🔐 Ethical Use**
SEO JavaScriptCrawler by IncRev strictly respects robots.txt and is built for ethical SEO crawling. You are responsible for complying with website terms and legal guidelines when using this tool.

**🧭 Coming Soon**
Structured data / schema.org extraction

Core Web Vitals auditing (via Lighthouse integration)

DOM-diff between raw and rendered HTML

Integration with Ahrefs and Google Search Console

<H2>💬 About IncRev </H2>
IncRev (https://increv.co, Incredible Revenue AB) is a global SEO agency operating in over 40 countries, specializing in link building, AI-powered SEO tools, and technical SEO optimization. We help SEO managers and marketing teams uncover hidden opportunities – often buried deep inside JavaScript-heavy websites.

**🔑 SEO Keywords**
SEO crawler, JavaScript SEO audit, IncRev SEO tool, technical SEO crawler, SEO JavaScript rendering, Playwright SEO tool, scalable SEO crawler, SEO automation, JavaScript site audit


## Features - Update 2025-06-15
...
- Supports crawling **Java-rendered links**, **images**, and **menus** — executes page JavaScript (via Puppeteer/Headless Chrome) to discover and snapshot elements injected dynamically.

## Usage / Configuration
Update your `config.js` tasks as usual:

```js
const tasks = [{
  distFolder: 'C:/snapshot/',
  startUrl: 'https://www.example.com/'
  // no extra flags needed — JS-enabled crawling is built-in
}];

Behind the scenes:

Pages are fully rendered with JS, ensuring dynamic elements appear in the DOM.

The crawler extracts:

Links injected or modified via JavaScript (in menus, widgets, etc.)

Images loaded dynamically (e.g. lazy‑loaded, srcset via JS)

Menu items, dropdowns, navigation components rendered client-side

Why JS-rendered support matters
Modern sites often generate navigation, links, and visuals via JS at runtime — if your crawler didn’t execute JS, it would miss critical content. By executing page scripts, our crawler finds those elements that would otherwise remain hidden during standard HTML fetch — improving coverage and accuracy.

Googlebot crawls in 3 phases (crawl, render, index) and requires JS rendering to discover client-injected content 
gitlab.com
github.com
github.com
github.com
+7
developers.google.com
+7
spencerlepine.medium.com
+7
.

Example output snippets
json

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
  ],
  ...
}
⚙️ How to Apply These Changes
Copy the updated sections above into your README.md under Features, Usage, and Why JS-rendered support matters.

Extend any output examples or CLI flags to reflect how JS-rendered items are captured in your code.

Commit and push the revised README to the repository.

Summary
Added Java-rendered links, images, and menus support.

Explained why JS execution is essential for modern SEO crawling.

Included a concrete output example showing JS-discovered elements.















