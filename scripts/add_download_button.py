import os
import re

# Список стран с главной страницы
ALLOWED_COUNTRIES = [
    'egypt', 'maldives', 'turkey', 'vietnam', 'china', 
    'mauritius', 'thailand', 'seychelles', 'indonesia', 
    'sri-lanka', 'tanzania', 'tunisia'
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMOS_DIR = os.path.join(BASE_DIR, 'pages', 'memos')

def add_button(filepath):
    filename = os.path.basename(filepath)
    country_slug = filename.replace('.html', '')
    
    # ФИЛЬТР: только страны с главной страницы
    if country_slug not in ALLOWED_COUNTRIES:
        print(f"Prop Filtered (not on home): {filename}")
        return

    pdf_path = f"../../dist_pdf/{country_slug}.pdf"
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'Скачать PDF' in content:
        print(f"Skip: {filename} (button already exists)")
        return

    button_html = f"""
          <a href="{pdf_path}" target="_blank" 
            class="no-print inline-flex items-center gap-3 bg-white text-black px-8 py-4 rounded-full text-lg font-bold shadow-lg hover:scale-105 active:scale-95 transition-all border border-black/10">
            <span class="material-symbols-outlined" style="font-size: 24px;">picture_as_pdf</span>
            Скачать PDF
          </a>"""

    pattern = r'(<div class="flex flex-wrap gap-4 mb-14">.*?)(</div>)'
    
    if re.search(pattern, content, flags=re.DOTALL):
        new_content = re.sub(pattern, r'\1' + button_html + r'\n          \2', content, flags=re.DOTALL, count=1)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Added button to: {filename}")
    else:
        print(f"Could not find button container in: {filename}")

if __name__ == "__main__":
    for filename in os.listdir(MEMOS_DIR):
        if filename.endswith('.html'):
            add_button(os.path.join(MEMOS_DIR, filename))
