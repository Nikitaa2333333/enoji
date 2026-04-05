import os
import re
from bs4 import BeautifulSoup
import json

tilda_dir = r"c:\Users\User\Downloads\tilda dododo\tilda_raw\emojitours.ru"
output_file = r"c:\Users\User\Downloads\tilda dododo\tmp\tilda_memo_data.json"

# List of memo pages to process (manually mapped based on some previous knowledge)
# We can find them by looking for "Памятка... [Страна]" in the Title
memo_pages = {}

for filename in os.listdir(tilda_dir):
    if filename.startswith("page") and filename.endswith(".html"):
        filepath = os.path.join(tilda_dir, filename)
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            soup = BeautifulSoup(content, "html.parser")
            title = soup.title.string if soup.title else ""
            if "Памятка" in title:
                country_match = re.search(r"Памятка [^ ]+ ([^|]+)", title)
                if not country_match:
                    country_match = re.search(r"Памятка [^ ]+ ([^ ]+)", title)
                
                country = country_match.group(1).strip() if country_match else title
                memo_pages[country] = filename

# Now extract sections and images for each
final_data = {}
for country, filename in memo_pages.items():
    filepath = os.path.join(tilda_dir, filename)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        sections = {}
        # Tilda sections usually have headers or specific block classes
        # Let's look for images and their nearest previous header
        for img in soup.find_all("img"):
            src = img.get("src") or img.get("data-original")
            if not src or "tildacdn" not in src and not src.startswith("images/"):
                continue
            
            # Find the closest preceding text that looks like a section header
            parent = img.parent
            header_text = "Unknown Section"
            while parent:
                # Look for h1, h2, h3, or text with bold style
                prev = img.find_previous(["h1", "h2", "h3", "div"])
                if prev:
                    header_text = prev.get_text(strip=True)[:100]
                break
            
            sections[header_text] = src
        
        final_data[country] = sections

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=4)
