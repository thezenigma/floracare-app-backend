import os
import time
import chromadb
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

INDEX_URL = "https://www.thespruce.com/plants-a-to-z-5116344"
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")

def scrape_index_page(page):
    print(f"Navigating to {INDEX_URL}...")
    page.goto(INDEX_URL)
    # Give the user 15 seconds to solve any Cloudflare captchas
    print("Waiting 15 seconds for page load / Cloudflare bypass...")
    page.wait_for_timeout(15000)
    
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    
    plants = []
    # New Spruce design uses a.mntl-link-list__link
    links = soup.select("a.mntl-link-list__link")
    for link in links:
        url = link.get("href")
        full_text = link.get_text(strip=True)
        if "|" in full_text:
            common_name = full_text.split('|')[0].strip()
            scientific_name = full_text.split('|')[1].strip()
        else:
            common_name = full_text
            scientific_name = ""
            
        if url:
            plants.append({
                "url": url,
                "common_name": common_name,
                "scientific_name": scientific_name
            })
            
    print(f"Found {len(plants)} plants in the A-Z index.")
    return plants

def extract_care_details(page, url):
    print(f"Scraping details from {url}...")
    try:
        page.goto(url)
        # Wait just enough for the content to render
        page.wait_for_timeout(4000)
    except Exception as e:
        print(f"Failed to load {url}: {e}")
        return None
        
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    
    # Try the new heading, fallback to generic h1
    title_el = soup.select_one("h1.article-heading")
    if not title_el:
        title_el = soup.select_one("h1")
    title = title_el.get_text(strip=True) if title_el else ""
    
    if not title or "contact support" in title.lower():
        print("Warning: Could not find plant title on the page or hit bot protection.")
        return None

    # Extract specs table
    specs = []
    table = soup.select_one("table.mntl-sc-block-universal-table__table")
    if table:
        rows = table.select("tr")
        for row in rows:
            cells = row.select("td")
            if len(cells) >= 2:
                key = cells[0].get_text(strip=True)
                val = cells[1].get_text(strip=True)
                specs.append(f"{key}: {val}")
                
    # Extract lifestyle care sections
    care_instructions = []
    headings = soup.find_all(['h2', 'h3'])
    for heading in headings:
        heading_text = heading.get_text(strip=True)
        
        # New Spruce design uses mntl-sc-block-subheading for care headers
        if "mntl-sc-block-subheading" in heading.get("class", []) or heading.name == 'h2':
            if heading_text.lower() in ['references', 'faq']:
                continue
                
            section_content = []
            sibling = heading.find_next_sibling()
            while sibling and sibling.name not in ['h2', 'h3']:
                if sibling.name == 'p' and "mntl-sc-block-html" in sibling.get("class", []):
                    section_content.append(sibling.get_text(strip=True))
                elif sibling.name == 'ul':
                    for li in sibling.find_all('li'):
                        section_content.append(f"- {li.get_text(strip=True)}")
                sibling = sibling.find_next_sibling()
                
            if section_content:
                care_instructions.append(f"[{heading_text}]\n" + "\n".join(section_content))
                
    # If a page has NO specs AND NO care instructions, it's not a valid guide. Skip it!
    if not specs and not care_instructions:
        print(f"Skipping {title} - No specs or care instructions found on page.")
        return None
                
    # Format into a single string chunk
    chunk = f"Plant: {title}\n"
    if specs:
        chunk += "--- Specifications ---\n" + "\n".join(specs) + "\n"
    if care_instructions:
        chunk += "--- Care Instructions ---\n" + "\n\n".join(care_instructions)
        
    return chunk

def main():
    os.makedirs(DB_DIR, exist_ok=True)
    
    print("Initializing ChromaDB...")
    from chromadb.config import Settings
    client = chromadb.PersistentClient(path=DB_DIR, settings=Settings(anonymized_telemetry=False))
    collection = client.get_or_create_collection(name="plants")
    
    print("Loading Nomic embedding model (v1.5)...")
    model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)
    
    # Track what we already have by querying IDs
    existing_ids = collection.get()["ids"] if collection.count() > 0 else []
    
    # We use headless=False to bypass Bot Protections!
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        Stealth().apply_stealth_sync(page)
        
        plants = scrape_index_page(page)
        
        # Process all plants
        for i, plant in enumerate(plants):
            plant_id = plant['common_name'].replace(" ", "_").lower()
            
            if plant_id in existing_ids:
                print(f"Skipping {plant['common_name']}, already in ChromaDB.")
                continue
                
            chunk = extract_care_details(page, plant["url"])
            if chunk:
                vector = model.encode([f"search_query: {chunk}"])[0].tolist()
                
                collection.add(
                    ids=[plant_id],
                    embeddings=[vector],
                    metadatas=[{"url": plant["url"], "name": plant["common_name"]}],
                    documents=[chunk]
                )
                print(f"[{i+1}/15] Embedded and added '{plant['common_name']}' to ChromaDB.")
            else:
                print(f"[{i+1}/15] Failed to extract data for '{plant['common_name']}'.")
                
            time.sleep(2)
            
        browser.close()
        print(f"Scraping and Ingestion complete. ChromaDB now has {collection.count()} plants.")

if __name__ == "__main__":
    main()
