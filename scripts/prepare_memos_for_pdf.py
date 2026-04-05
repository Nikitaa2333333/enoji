import os
import re

# Automation script to prepare all Travel Memos for PDF generation
# Туроператора - Professional Layout Standard
# UPDATED: Replaces dynamic download button with direct link to generated PDF
# LIMITED: Only for the 12 main countries on the homepage

MEMOS_DIR = r'c:\Users\User\Downloads\tilda dododo\pages\memos'
CSS_PATH = '../../css/print_styles.css'
LOGO_PATH = '../../images/logo.png'
PHONE = '+7 (963) 649-18-52'
EMAIL = 'trohin.zh@yandex.ru'

# Fixed list of 12 main countries
FILES_TO_PROCESS = [
    'egypt.html',
    'maldives.html',
    'turkey.html',
    'vietnam.html',
    'china.html',
    'mauritius.html',
    'thailand.html',
    'seychelles.html',
    'indonesia.html',
    'sri-lanka.html',
    'tanzania.html',
    'tunisia.html'
]

def process_file(filename):
    filepath = os.path.join(MEMOS_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Skipping {filename}: File not found")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Inject Print Stylesheet
    if CSS_PATH not in content:
        content = content.replace('</head>', f'  <link rel="stylesheet" href="{CSS_PATH}">\n</head>')

    # 2. Extract Country Name from <title>
    title_match = re.search(r'<title>Памятка: (.*?) — Туроператора</title>', content)
    country_name = title_match.group(1) if title_match else filename.replace('.html', '').capitalize()

    # 3. Inject Print Header (if not present)
    if 'print-header' not in content:
        print_header = f"""
  <!-- PRINT HEADER (Visible only in PDF) -->
  <div class="print-only print-header">
    <img src="{LOGO_PATH}" alt="Туроператора">
    <div class="print-header-title">
      <p style="font-size: 10pt; color: #888; margin-bottom: 4px; font-family: 'Manrope';">Памятка путешественника</p>
      <h1 style="margin: 0; font-size: 24pt; color: #f7941d; font-family: 'Manrope';">{country_name}</h1>
    </div>
  </div>
"""
        content = re.sub(r'(<body.*?>)', r'\1' + print_header, content, flags=re.IGNORECASE)

    # 4. Inject or Update Print Footer
    new_footer = f"""
  <!-- PRINT FOOTER (Visible only in PDF) -->
  <div class="print-only print-footer" style="position: fixed; bottom: 0; left: 0; right: 0; display: flex; justify-content: space-between; font-family: 'Manrope'; padding-top: 0; color: #888; font-size: 9pt;">
    <span>Туроператора — Путешествия с душой</span>
    <span>emojitours.ru | {PHONE} | {EMAIL}</span>
  </div>
"""
    if 'print-footer' in content:
        # Search for the old footer block and replace it
        content = re.sub(r'<!-- PRINT FOOTER.*?print-footer.*?</div>', new_footer.strip(), content, flags=re.DOTALL)
    else:
        content = content.replace('</body>', new_footer + '\n</body>')

    # 5. Replace PDF download button with direct link to the generated PDF
    # Normalize filename for Memo_ name (capitalized)
    base_name = filename.replace('.html', '').replace('-', '_')
    parts = base_name.split('_')
    pretty_name = "".join([p.capitalize() for p in parts])
    
    pdf_link = f'../../dist_pdf/Memo_{pretty_name}.pdf'
    
    # Pattern to find the existing PDF download button
    button_pattern = r'<button\s+[^>]*onclick="PDFDownload\.download\(.*?\)"[^>]*>.*?</button>'
    
    def repl_btn(match):
        btn_full_html = match.group(0)
        # Extract the content inside the button (icons, text)
        inner_html = re.sub(r'<(button|button\s+[^>]*)>', '', btn_full_html)
        inner_html = inner_html.replace('</button>', '')
        # Clean up any duplicated no-print classes that might be inside
        inner_html = inner_html.replace('class="no-print"', '')
        
        return f'<a href="{pdf_link}" target="_blank" class="no-print group flex items-center gap-2 text-black hover:opacity-70 transition-all font-medium ml-4">{inner_html}</a>'

    content = re.sub(button_pattern, repl_btn, content, flags=re.DOTALL)

    # 6. Global Cleanups and no-print injections (with deduplication)
    def add_no_print(tag_html):
        if 'no-print' in tag_html:
            return tag_html # Already has it
        return tag_html.replace('class="', 'class="no-print ')

    # Navigation tags
    content = re.sub(r'<nav class=".*?>', lambda m: add_no_print(m.group(0)), content)
    content = re.sub(r'<aside class=".*?>', lambda m: add_no_print(m.group(0)), content)
    
    # "Хочу туда", "О стране" buttons - add no-print if missing
    content = re.sub(r'(<a\s+[^>]*class=")(?!.*no-print\b)([^"]*inline-block[^"]*")', r'\1no-print \2', content)

    # NEW: Aggressively hide images in HTML for print
    # We add no-print to all img tags EXCEPT those inside print-header
    # First, protect print-header images by temporarily renaming them (hacky but safe for regex)
    content = content.replace('class="print-only print-header"', 'class="PROT-HEADER"')
    
    def img_no_print(match):
        img_tag = match.group(0)
        if 'no-print' in img_tag: return img_tag
        if 'class="' in img_tag:
            return img_tag.replace('class="', 'class="no-print ')
        else:
            return img_tag.replace('<img ', '<img class="no-print" ')
            
    content = re.sub(r'<img [^>]*>', img_no_print, content)
    content = content.replace('class="PROT-HEADER"', 'class="print-only print-header"')

    # Final cleanup: Remove double "no-print no-print" if any
    content = content.replace('no-print no-print', 'no-print')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Updated {filename} with direct PDF links")

if __name__ == "__main__":
    print("--- Updating Travel Memos (12 main countries) ---")
    for filename in FILES_TO_PROCESS:
        process_file(filename)
    print("Finished.")
