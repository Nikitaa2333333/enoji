
import os
import json
from bs4 import BeautifulSoup
import re

# Mapping of Country Names to Page IDs (from earlier manual check or extraction)
PAGE_IDS = {
    "Египет": "128281366",
    "Тайланд": "128281096",
    "Шри-Ланка": "128280629",
    "ОАЭ": "128280459",
    "Турция": "128280227",
    "Мальдивы": "128279860",
    "Кипр": "128279717",
    "Сейшелы": "128279410",
    "Маврикий": "21389868",
    "Танзания": "128279148",
    "Мексика": "128278783",
    "Доминикана": "128278553",
    "Куба": "128278378",
    "Вьетнам": "128278148",
    "Индия": "128277983",
    "Тунис": "128277833",
    "Китай": "128277579",
    "Индонезия": "128277341",
    "Израиль": "128277157"
}

RAW_FILES_DIR = "tilda_raw/emojitours.ru/files/"
OUTPUT_JSON = "tmp/tilda_memo_comprehensive.json"

def clean_text(text):
    if not text: return ""
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove leading dots or special chars often used in headers
    text = re.sub(r'^[●\-\. ]+', '', text)
    return text

def extract_from_body(page_id):
    filename = f"page{page_id}body.html"
    filepath = os.path.join(RAW_FILES_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found")
        return []

    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    data = []
    # Find all records (blocks)
    records = soup.find_all('div', class_='t-records')
    if not records:
        records = [soup] # fallback if structure is different
    
    # We'll iterate through all divs with class "r t-rec"
    blocks = soup.find_all('div', class_='t-rec')
    
    last_header = "Без заголовка"
    
    for block in blocks:
        # Check for title
        title_tag = block.find(['div', 'h1', 'h2', 'h3'], class_=['t-title', 't795__title'])
        if title_tag:
            last_header = clean_text(title_tag.get_text())
        else:
            # Look for bold text in t-text that looks like a header
            text_tag = block.find('div', class_='t-text')
            if text_tag:
                strong = text_tag.find(['strong', 'b'])
                if strong:
                    header_candidate = clean_text(strong.get_text())
                    if len(header_candidate) > 3 and len(header_candidate) < 100:
                        last_header = header_candidate

        # Check for images in t107 or similar
        img_tags = block.find_all('img')
        for img in img_tags:
            src = img.get('src') or img.get('data-original')
            if src and not src.endswith('.svg'):
                # Strip the tilda path prefixes if any
                clean_src = src.replace('https://static.tildacdn.com/', '')
                data.append({
                    "section": last_header,
                    "image": f"images/{clean_src}"
                })
                # Once we found an image for this header, we might want to clear it or not
                # But usually one block has one main image.
    
    return data

def main():
    result = {}
    for country, page_id in PAGE_IDS.items():
        print(f"Processing {country}...")
        result[country] = extract_from_body(page_id)
    
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    print(f"Extraction complete. Saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
