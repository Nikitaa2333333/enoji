
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
        # Fallback: look for <h1> or title in metadata (though body files usually don't have <title>)
        h1 = soup.find('h1')
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
        # Check for anchors first (they are often more reliable than text)
        anchor = block.find('a', attrs={"name": True})
        if anchor:
            # We don't use the anchor as the header text, but it helps keep context
            pass

        title_tag = block.find(['div', 'h1', 'h2', 'h3'], class_=['t-title', 't795__title'])
        if title_tag:
            last_header = clean_text(title_tag.get_text())
        else:
            text_tag = block.find('div', class_='t-text')
            if text_tag:
                strong = text_tag.find(['strong', 'b'])
                if strong:
                    header_candidate = clean_text(strong.get_text())
                    if 3 < len(header_candidate) < 100:
                        last_header = header_candidate

        img_tags = block.find_all('img')
        for img in img_tags:
            src = img.get('src') or img.get('data-original')
            if src and not src.endswith('.svg'):
                clean_src = src.replace('https://static.tildacdn.com/', '')
                data.append({
                    "section": last_header,
                    "image": f"images/{clean_src}"
                })
    
    return country_name, data

def main():
    result = {}
    print(f"Scanning directory: {RAW_FILES_DIR}")
    for filename in os.listdir(RAW_FILES_DIR):
        if filename.endswith("body.html"):
            filepath = os.path.join(RAW_FILES_DIR, filename)
            country, country_data = extract_from_file(filepath)
            if country:
                print(f"  Found data for: {country}")
                result[country] = country_data
    
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    print(f"\nExtraction complete. Saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
