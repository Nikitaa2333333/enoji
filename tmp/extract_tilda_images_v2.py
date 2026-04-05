import os
import re
from bs4 import BeautifulSoup
import json

tilda_dir = r"c:\Users\User\Downloads\tilda dododo\tilda_raw\emojitours.ru"
files_dir = os.path.join(tilda_dir, "files")
output_file = r"c:\Users\User\Downloads\tilda dododo\tmp\tilda_memo_detailed.json"

# First, map pages to countries using the main html files
memo_pages = {}
for filename in os.listdir(tilda_dir):
    if filename.startswith("page") and filename.endswith(".html") and "body" not in filename:
        filepath = os.path.join(tilda_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
                title = soup.title.string if soup.title else ""
                if "Памятка" in title:
                    # Clean up country name
                    country = title.replace("Памятка туриста", "").replace("Памятка", "").split("|")[0].strip()
                    page_id = filename.replace(".html", "")
                    memo_pages[country] = page_id
        except:
            continue

# Now extract from body files
final_data = {}
for country, page_id in memo_pages.items():
    body_file = f"{page_id}body.html"
    body_path = os.path.join(files_dir, body_file)
    if not os.path.exists(body_path):
        continue
    
    sections = []
    with open(body_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        # Tilda blocks often have headers in t-title, t-heading, etc.
        # Or images in t-img
        blocks = soup.find_all(class_="t-rec")
        for block in blocks:
            header = block.find(class_=re.compile("t-title|t-heading|t-name|t-descr"))
            img = block.find("img")
            
            if img:
                src = img.get("src") or img.get("data-original")
                if src and "logo.png" not in src:
                    header_text = header.get_text(strip=True) if header else "Без заголовка"
                    sections.append({"section": header_text, "image": src})
    
    final_data[country] = sections

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=4)
