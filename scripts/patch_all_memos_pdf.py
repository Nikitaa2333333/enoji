import os
import re

memo_dir = 'pages/memos'

# Button template
def get_button_html(country):
    return f'''          <button onclick="PDFDownload.download('{country}')"
            class="inline-block bg-white border-2 border-black text-black px-10 py-4 rounded-full text-lg font-bold shadow-lg hover:scale-105 active:scale-95 transition-all flex items-center gap-2">
            <span class="material-symbols-outlined">download_for_offline</span>
            Скачать PDF
          </button>'''

# Script tags
script_tags = '''  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
  <script src="../../scripts/pdf-download.js"></script>'''

for filename in os.listdir(memo_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(memo_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Skip if already patched
        if 'pdf-download.js' in content:
            print(f'Skipping {filename}: already patched')
            continue

        # 2. Extract country name from h1
        # Example: <h1 class="...">Памятка: Вьетнам</h1>
        h1_match = re.search(r'<h1[^>]*>Памятка:\s*([^<]+)</h1>', content)
        if not h1_match:
            print(f'Warning: Could not find country name in {filename}')
            country = filename.replace('.html', '').capitalize()
        else:
            country = h1_match.group(1).strip()

        print(f'Patching {filename} for {country}...')

        # 3. Inject scripts into head (after tailwind)
        content = content.replace(
            '<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>',
            '<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>\n' + script_tags
        )

        # 4. Inject button before the "Хочу туда" button or after "О стране"
        # We look for the "О стране" a tag end or similar
        search_pattern = r'(<a href="\.\./countries/[^"]+"[^>]*>О\s*стране</a>)'
        if re.search(search_pattern, content):
            content = re.sub(search_pattern, r'\1\n' + get_button_html(country), content)
        else:
            print(f'Warning: Could not find action buttons in {filename}')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print('Done patching all memos!')
