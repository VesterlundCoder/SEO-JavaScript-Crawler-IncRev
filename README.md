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















