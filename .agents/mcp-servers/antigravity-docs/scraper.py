import json
from playwright.sync_api import sync_playwright

def run(playwright):
    print("Launching headless browser...")
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    
    print("Navigating to Antigravity Docs...")
    # Load the page and wait for the network to idle so JavaScript finishes rendering
    page.goto("https://antigravity.google/docs/get-started", wait_until="networkidle")
    page.wait_for_timeout(2000)
    
    print("Parsing sidebar navigation links...")
    # The links are inside elements with class 'page-nav-item'
    nav_items = page.locator(".page-nav-list .page-nav-item").all()
    
    links = []
    for item in nav_items:
        # Extract the title from the inner span
        title_element = item.locator(".nav-title")
        if title_element.count() > 0:
            title = title_element.inner_text().strip()
        else:
            title = item.inner_text().strip()
            
        # Extract the href attribute from the anchor tag
        href = item.get_attribute("href")
        
        # Only add valid documentation links
        if title and href:
            full_url = f"https://antigravity.google{href}"
            links.append({"title": title, "url": full_url})
            print(f"Found: {title} -> {full_url}")
            
    # Save the links list to a JSON file
    with open("links.json", "w", encoding="utf-8") as f:
        json.dump(links, f, indent=4)
        
    print(f"\nSuccessfully saved {len(links)} links to links.json!")
    
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
