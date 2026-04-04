import os
import re

memo_dir = 'pages/memos'

def get_bottom_link_html(country):
    return f'''
        <!-- КНОПКА СКАЧИВАНИЯ PDF ВНИЗУ -->
        <div class="mt-20 flex justify-center no-pdf">
          <button onclick="PDFDownload.download('{country}')" 
            class="group flex items-center gap-3 text-black/60 hover:text-black transition-all font-bold py-3 px-6 rounded-xl bg-black/5 hover:bg-black/[0.08] border border-black/5">
            <span class="material-symbols-outlined text-[22px]">download_for_offline</span>
            <span class="border-b border-black/20 group-hover:border-black/40 transition-all">Скачать памятку {country} в PDF</span>
          </button>
        </div>
'''

for filename in os.listdir(memo_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(memo_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Extract country name first
        h1_match = re.search(r'<h1[^>]*>Памятка:\s*([^<]+)</h1>', content)
        if not h1_match:
            country = filename.replace('.html', '').capitalize()
        else:
            country = h1_match.group(1).strip()

        # 2. Remove the old button at the top (specifically the one with download_for_offline or PDF)
        # We'll match precisely the button structure we used before to avoid touching others
        old_button_regex = r'<button onclick="PDFDownload\.download\([^)]+\)"\s+class="[^"]*rounded-full[^"]*">.*?</button>'
        content = re.sub(old_button_regex, '', content, flags=re.DOTALL)
        
        # Additional cleanup for different classes if any
        content = re.sub(r'<button onclick="PDFDownload\.download\([^)]+\)"\s+class="[^"]*rounded-xl[^"]*">.*?</button>', '', content, flags=re.DOTALL)

        # 3. Insert the new link at the bottom of the content area
        # We look for the end of the content area which is usually </div>\s*</div>\s*</main>
        # We want it inside the main content container but at the very end
        insertion_point = r'(</div>\s*</div>\s*</main>)'
        if re.search(insertion_point, content):
            content = re.sub(insertion_point, get_bottom_link_html(country) + r'\1', content)
        else:
            # Fallback
            content = content.replace('</main>', get_bottom_link_html(country) + '</main>')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print("Done moving PDF buttons to bottom as links!")
