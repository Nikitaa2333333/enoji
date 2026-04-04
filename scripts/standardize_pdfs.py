import os
import re

memo_dir = 'pages/memos'

def get_top_link_html(country):
    # Updated design: EXACT SAME WEIGHT (font-bold) and size (text-lg) as main buttons, black font, no caps
    return f'''
          <button onclick="PDFDownload.download('{country}')" 
            class="group flex items-center gap-2 text-on-surface hover:text-black transition-all font-bold ml-5">
            <span class="material-symbols-outlined text-[26px]">download_for_offline</span>
            <span class="border-b-2 border-black group-hover:border-black/40 transition-all text-lg">Скачать памятку PDF</span>
          </button>'''

for filename in os.listdir(memo_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(memo_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Extract country name
        h1_match = re.search(r'<h1[^>]*>Памятка:\s*([^<]+)</h1>', content)
        if not h1_match:
            country_name = filename.replace('.html', '').capitalize()
            if country_name.lower() == 'oae': country_name = 'ОАЭ'
        else:
            country_name = h1_match.group(1).strip()

        # 2. Add/Correct scripts in <head>
        if '<script src="../../scripts/pdf-download.js"></script>' not in content:
            head_end = content.find('</head>')
            if head_end != -1:
                script_block = '  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>\n  <script src="../../scripts/pdf-download.js"></script>\n'
                content = content[:head_end] + script_block + content[head_end:]

        # 3. Ensure id="main-content"
        if 'id="main-content"' not in content:
            content = content.replace('class="space-y-16"', 'id="main-content" class="space-y-16"')

        # 4. Remove any existing PDF buttons/links
        content = re.sub(r'<!-- КНОПКА СКАЧИВАНИЯ PDF ВНИЗУ -->.*?</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<div class="mt-20 flex justify-center no-pdf">.*?</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<button onclick="PDFDownload\.download\(.*?</button>', '', content, flags=re.DOTALL)

        # 5. Inject the new link (BOLD & LARGE)
        action_pattern = r'(<a href="#section-form"[^>]*>Хочу\s*туда</a>)'
        if re.search(action_pattern, content):
            content = re.sub(action_pattern, r'\1\n' + get_top_link_html(country_name), content)
        else:
            content = re.sub(r'(class="flex flex-wrap gap-4 mb-14">.*?)(\s*</div>)', r'\1' + get_top_link_html(country_name) + r'\2', content, flags=re.DOTALL)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print("Standardized all 12 memos with EXACT weight and size as buttons (BOLD and LARGE)!")
