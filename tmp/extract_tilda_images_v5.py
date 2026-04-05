
import os
import json
from bs4 import BeautifulSoup
import re

RAW_FILES_DIR = "tilda_raw/emojitours.ru/files/"
OUTPUT_JSON = "tmp/tilda_memo_comprehensive.json"

# Mapping of Tilda aliases to our internal country names
ALIAS_TO_COUNTRY = {
    "memoegypt": "Египет",
    "memothailand": "Тайланд",
    "memosrilanka": "Шри-Ланка",
    "memouae": "ОАЭ",
    "memoturkey": "Турция",
    "memomaldives": "Мальдивы",
    "memocyprus": "Кипр",
    "memoseychelles": "Сейшелы",
    "memomauritius": "Маврикий",
    "memotanzania": "Танзания",
    "memomexico": "Мексика",
    "memodominicana": "Доминикана",
    "memocuba": "Куба",
    "memovietnam": "Вьетнам",
    "memoindia": "Индия",
    "memotunisia": "Тунис",
    "memochina": "Китай",
    "memoindonesia": "Индонезия",
    "memoisrael": "Израиль"
}

def clean_text(text):
    if not text: return ""
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'^[●\-\. ]+', '', text)
    # Remove trailing colons often found in Tilda headers
    text = text.rstrip(':')
    return text

def extract_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Try to identify country from alias
    all_records = soup.find('div', id='allrecords')
    country_name = None
    if all_records:
        alias = all_records.get('data-tilda-page-alias')
        if alias in ALIAS_TO_COUNTRY:
            country_name = ALIAS_TO_COUNTRY[alias]
    
    if not country_name:
        # Fallback: look for <h1> or <h1>-like text
        h1 = soup.find(['h1', 'div'], class_=['t-title', 't-text'])
        if h1:
            h1_text = h1.get_text().lower()
            for alias, name in ALIAS_TO_COUNTRY.items():
                if name.lower() in h1_text:
                    country_name = name
                    break

    if not country_name:
        return None, []

    data = []
    blocks = soup.find_all('div', class_='t-rec')
    last_header = "Без заголовка"
    
    for block in blocks:
        # 1. Look for explicit titles
        title_tag = block.find(['div', 'h1', 'h2', 'h3'], class_=['t-title', 't795__title', 't-name'])
        
        # 2. Look for strong tags that look like headers in text blocks
        text_tag = block.find('div', class_=['t-text', 't-descr'])
        
        if title_tag:
            header_text = clean_text(title_tag.get_text())
            if header_text and len(header_text) > 2:
                last_header = header_text
        elif text_tag:
            # Check for strong tags at the beginning of the text
            strong = text_tag.find(['strong', 'b'])
            if strong:
                header_candidate = clean_text(strong.get_text())
                # If it's a short bold text at the start, it's likely a header
                if 2 < len(header_candidate) < 100:
                    last_header = header_candidate

        img_tags = block.find_all('img')
        for img in img_tags:
            # Prefer data-original for high quality and to avoid __empty__ placeholders
            src = img.get('data-original') or img.get('src')
            if src and not src.endswith('.svg') and 'logo' not in src.lower():
                # Clean up Tilda CDN if present
                clean_src = src.replace('https://static.tildacdn.com/', '')
                
                # Check if it already has 'images/' prefix and normalize
                if clean_src.startswith('images/'):
                    clean_src = clean_src[len('images/'):]
                
                # Consistently store with 'images/' prefix
                final_path = f"images/{clean_src}"
                
                # Ensure we don't add the same image for the same header twice in a row
                if not data or data[-1]['image'] != final_path:
                    data.append({
                        "section": last_header,
                        "image": final_path
                    })
    
    return country_name, data

def main():
    result = {}
    print(f"Scanning directory: {RAW_FILES_DIR}")
    
    # Sort files to ensure consistency
    files = sorted(os.listdir(RAW_FILES_DIR))
    
    for filename in files:
        if filename.endswith("body.html"):
            filepath = os.path.join(RAW_FILES_DIR, filename)
            country, country_data = extract_from_file(filepath)
            if country:
                print(f"  Found data for: {country} in {filename} ({len(country_data)} images)")
                if country not in result:
                    result[country] = []
                # Append data instead of overwriting
                result[country].extend(country_data)
    
    # Deduplicate images for each country while maintaining order
    for country in result:
        unique_data = []
        seen_images = set()
        for item in result[country]:
            if item['image'] not in seen_images:
                unique_data.append(item)
                seen_images.add(item['image'])
        result[country] = unique_data
    
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    print(f"\nExtraction complete. Saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
