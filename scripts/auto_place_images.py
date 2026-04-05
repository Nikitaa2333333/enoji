
import os
import json
import re
from bs4 import BeautifulSoup

# Comprehensive Mapping
COUNTRY_FILE_MAP = {
    "Египет": "egypt.html",
    "Тайланд": "thailand.html",
    "Шри-Ланка": "sri-lanka.html",
    "ОАЭ": "oae.html",
    "Турция": "turkey.html",
    "Мальдивы": "maldives.html",
    "Кипр": "ofcyprus.html",
    "Сейшелы": "seychelles.html",
    "Маврикий": "mauritius.html",
    "Танзания": "tanzania.html",
    "Мексика": "mexico.html",
    "Доминикана": "dominikana.html",
    "Куба": "cuba.html",
    "Вьетнам": "vietnam.html",
    "Индия": "india.html",
    "Тунис": "tunisia.html",
    "Китай": "china.html",
    "Индонезия": "indonesia.html",
    "Израиль": "israel.html"
}

# Image Data File
IMAGE_DATA_FILE = "tmp/tilda_memo_comprehensive.json"
PAGES_DIR = "pages/memos/"
IMG_CLASSES = "no-print w-full h-auto rounded-[2rem] md:rounded-[3.5rem] shadow-2xl my-16 object-cover"

# Force Mapping for specific image filenames
FORCE_MAPPING = {
    "thumb_67866_expert_b.jpg": "багаж",
    "zagranpasport-novogo.jpg": "документы",
    "komfortnyi-otdykh-s-.jpg": "дети"
}

# Heading Synonym Map
SYNONYMS = {
    "документы": ["перед отъездом", "туристу при отъезде", "документы для поездки", "документов", "паспорта"],
    "дети": ["в случае путешествия с детьми", "путешествие с детьми", "дети", "ребенка"],
    "багаж": ["собирая багаж", "правила провоза багажа", "багаж", "чемоданы"],
    "прибытие": ["аэропорт рф", "в российском аэропорту", "прибытие"],
    "таможня": ["таможенный контроль", "таможня", "декларирование"],
    "регистрация": ["регистрация на рейс", "оформление багажа"],
    "контроль": ["пограничный контроль", "паспортный контроль", "санитарный контроль"],
}

def clean_header(text):
    if not text: return ""
    text = re.sub(r'\s+', ' ', text).strip().lower()
    return text.rstrip(':').rstrip('.')

def find_best_image(header_text, country_images, used_images):
    clean_h = clean_header(header_text)
    
    # 0. Force Mapping priority
    for img_filename, section_keyword in FORCE_MAPPING.items():
        if section_keyword in clean_h:
            for item in country_images:
                if img_filename in item['image']:
                    return item['image']

    # 1. Exact match
    for item in country_images:
        if item['image'] in used_images: continue
        if clean_header(item['section']) == clean_h:
            # Avoid grabbing forced images for wrong sections
            if any(f in item['image'] for f in FORCE_MAPPING.keys()): continue
            return item['image']
    
    # 2. Synonym match
    for standard, list_of_synonyms in SYNONYMS.items():
        if standard in clean_h or any(s in clean_h for s in list_of_synonyms):
            for item in country_images:
                if item['image'] in used_images: continue
                clean_sec = clean_header(item['section'])
                if clean_sec in list_of_synonyms or standard in clean_sec or any(s in clean_sec for s in list_of_synonyms):
                    # Check against FORCE_MAPPING keywords
                    is_forced = False
                    for f_img, f_kw in FORCE_MAPPING.items():
                        if f_img in item['image']:
                            is_forced = True
                            if f_kw in clean_h: return item['image']
                    if not is_forced:
                        return item['image']

    return None

def process_memo(file_path, country_name, all_images):
    if country_name not in all_images:
        print(f"Skipping {country_name}: No image data found.")
        return

    country_images = all_images[country_name]
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pre-clean broken or legacy images
    cleansed_content = re.sub(r'<imgsrc="[^"]+"[^>]*>', '', content)
    cleansed_content = re.sub(r'<img[^>]+src="[^"]*images/images/[^"]+"[^>]*>', '', cleansed_content)
    
    soup = BeautifulSoup(cleansed_content, 'html.parser')
    modified = (cleansed_content != content)

    # Remove duplicates or placeholders before re-inserting
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if '__empty__' in src or any(f in src for f in FORCE_MAPPING.keys()):
            img.decompose()
            modified = True

    headers = soup.find_all(['h2', 'h3'])
    used_images = set()

    for h in headers:
        header_text = h.get_text().strip()
        img_src = find_best_image(header_text, country_images, used_images)
        
        if img_src:
            new_img = soup.new_tag('img', src=f"../../{img_src}", alt=header_text)
            new_img['class'] = IMG_CLASSES
            new_img['loading'] = "lazy"
            
            # Smart Placement: Find top-level target (exit <li>, <ul>, etc.)
            target = h
            while target.parent and target.parent.name in ['li', 'ul', 'span', 'p', 'strong']:
                target = target.parent
            
            target.insert_after(new_img)
            used_images.add(img_src)
            modified = True
            print(f"  Placed {os.path.basename(img_src)} after: {header_text[:30]}...")

    if modified:
        # Prettify with minimal modification to preserve structure
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print(f"Saved {file_path}")

def main():
    if not os.path.exists(IMAGE_DATA_FILE):
        print(f"Error: {IMAGE_DATA_FILE} not found.")
        return

    with open(IMAGE_DATA_FILE, 'r', encoding='utf-8') as f:
        all_images = json.load(f)

    for country, filename in COUNTRY_FILE_MAP.items():
        file_path = os.path.join(PAGES_DIR, filename)
        if os.path.exists(file_path):
            print(f"Processing {country}...")
            process_memo(file_path, country, all_images)

if __name__ == "__main__":
    main()
