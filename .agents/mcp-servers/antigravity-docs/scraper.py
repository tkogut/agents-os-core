import json
import re
import urllib.request
import gzip
from playwright.sync_api import sync_playwright

def run_playwright(playwright):
    print("Launching headless browser...")
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    
    print("Navigating to Antigravity Docs...")
    page.goto("https://antigravity.google/docs/getting-started", wait_until="networkidle")
    page.wait_for_timeout(3000)
    
    print("Parsing sidebar navigation links...")
    links = []
    seen_urls = set()
    
    nav_anchors = page.locator(".sidebar-content a[href^='/docs/'], nav.sidebar a[href^='/docs/'], a[href^='/docs/']").all()
    
    for anchor in nav_anchors:
        try:
            href = anchor.get_attribute("href")
            if not href:
                continue
            clean_href = href.split("#")[0].rstrip("/")
            if not clean_href.startswith("/docs"):
                continue
                
            title = anchor.inner_text().strip()
            title = title.split("\n")[0].strip()
            if not title:
                continue
                
            full_url = f"https://antigravity.google{clean_href}"
            if full_url not in seen_urls:
                seen_urls.add(full_url)
                links.append({"title": title, "url": full_url})
                print(f"Found: {title} -> {full_url}")
        except Exception:
            continue
            
    browser.close()
    return links

def fallback_http_scrape():
    print("Fallback: extracting docs links directly via HTTP...")
    req = urllib.request.Request(
        "https://antigravity.google/docs/getting-started",
        headers={"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = resp.read()
        try:
            html = gzip.decompress(data).decode("utf-8", errors="ignore")
        except Exception:
            html = data.decode("utf-8", errors="ignore")
            
    raw_links = re.findall(r'<a[^>]+href="(/docs/[^"#]+)"[^>]*>(.*?)</a>', html, re.DOTALL)
    seen = set()
    links = []
    for href, text in raw_links:
        clean_text = re.sub(r'<[^>]+>', '', text).strip()
        clean_text = clean_text.split("\n")[0].strip()
        clean_href = href.rstrip("/")
        full_url = f"https://antigravity.google{clean_href}"
        if full_url not in seen and clean_text:
            seen.add(full_url)
            links.append({"title": clean_text, "url": full_url})
    return links

def run():
    links = []
    try:
        with sync_playwright() as playwright:
            links = run_playwright(playwright)
    except Exception as e:
        print(f"Playwright error: {e}")
        
    if not links:
        links = fallback_http_scrape()
        
    with open("links.json", "w", encoding="utf-8") as f:
        json.dump(links, f, indent=4)
        
    print(f"\nSuccessfully saved {len(links)} links to links.json!")

if __name__ == "__main__":
    run()
