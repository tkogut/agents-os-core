import json
import os
import re
from playwright.sync_api import sync_playwright

def sanitize_filename(name):
    """Replaces invalid filename characters with underscores."""
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name).strip('_')

def run(playwright):
    kb_dir = "knowledge_base"
    os.makedirs(kb_dir, exist_ok=True)
    
    if not os.path.exists("links.json"):
        print("Error: links.json not found!")
        return
        
    with open("links.json", "r", encoding="utf-8") as f:
        links = json.load(f)
        
    print(f"Starting extraction of {len(links)} pages into '{kb_dir}' folder...")
    if not links:
        return
        
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    
    success_count = 0
    for idx, link in enumerate(links):
        title = link["title"]
        url = link["url"]
        
        filename = f"{idx+1:02d}_{sanitize_filename(title)}.md"
        filepath = os.path.join(kb_dir, filename)
        
        print(f"[{idx+1}/{len(links)}] Grabbing: {title} -> {filename}")
        
        try:
            page.goto(url, wait_until="networkidle", timeout=20000)
            page.wait_for_timeout(1000)
            
            # Target primary documentation content containers in Astro/Starlight
            container = None
            for selector in ["main[data-pagefind-body]", "main", ".docs-main-content", "article"]:
                if page.locator(selector).count() > 0:
                    container = page.locator(selector).first
                    break
                    
            if container:
                content = container.inner_text()
            else:
                content = page.locator("body").inner_text()
                
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# {title}\n")
                f.write(f"Source URL: {url}\n\n")
                f.write(content)
            success_count += 1
                
        except Exception as e:
            print(f"  -> Error grabbing {title}: {e}")
            
    print(f"\nExtraction complete! Successfully saved {success_count}/{len(links)} files in '{kb_dir}'.")
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
