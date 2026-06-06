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
    
    # Open our map of 42 links
    with open("links.json", "r", encoding="utf-8") as f:
        links = json.load(f)
        
    print(f"Starting extraction of {len(links)} pages into '{kb_dir}' folder...")
    
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    
    for idx, link in enumerate(links):
        title = link["title"]
        url = link["url"]
        
        # Prefix the filename with the index to maintain the reading order
        filename = f"{idx+1:02d}_{sanitize_filename(title)}.md"
        filepath = os.path.join(kb_dir, filename)
        
        print(f"[{idx+1}/{len(links)}] Grabbing: {title} -> {filename}")
        
        try:
            # Go to the page and wait for the network to finish loading the JS content
            page.goto(url, wait_until="networkidle")
            
            # Wait until our target text container appears
            page.wait_for_selector(".docs-main-content", timeout=10000)
            
            # .inner_text() tries to format the DOM content cleanly with newlines
            content = page.locator(".docs-main-content").inner_text()
            
            # Write out to a clean Markdown file
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# {title}\n")
                f.write(f"Source URL: {url}\n\n")
                f.write(content)
                
        except Exception as e:
            print(f"  -> Error grabbing {title}: {e}")
            
    print("\nExtraction complete! All files saved in the 'knowledge_base' folder.")
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
