import os
import re

memo_dir = 'pages/memos'

def get_top_link_html(country):
    return f'''
          <button onclick="PDFDownload.download('{country}')" 
            class="group flex items-center gap-2 text-black/50 hover:text-black transition-all font-bold ml-2">
            <span class="material-symbols-outlined text-[22px]">download_for_offline</span>
            <span class="border-b border-black/10 group-hover:border-black/30 transition-all text-xs uppercase tracking-widest">Скачать PDF</span>
          </button>'''

for filename in os.listdir(memo_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(memo_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Extract country name
        h1_match = re.search(r'<h1[^>]*>Памятка:\s*([^<]+)</h1>', content)
        if not h1_match:
            country = filename.replace('.html', '').capitalize()
        else:
            country = h1_match.group(1).strip()

        # 2. Remove the link from the BOTTOM (cleanup the previous step)
        content = re.sub(r'<!-- КНОПКА СКАЧИВАНИЯ PDF ВНИЗУ -->.*?</div>\s*</div>\s*</div>\s*(?=</main>)', '</div>\n    </div>\n', content, flags=re.DOTALL)
        # More robust cleanup for the bottom link
        content = re.sub(r'<div class="mt-20 flex justify-center no-pdf">.*?</div>\n(?=\s*</div>\s*</div>\s*</main>)', '', content, flags=re.DOTALL)

        # 3. Add to the TOP, after the "Хочу туда" button
        # Target pattern: <a href="#section-form" ...>Хочу туда</a>
        action_pattern = r'(<a href="#section-form"[^>]*>Хочу\s*туда</a>)'
        if re.search(action_pattern, content):
            content = re.sub(action_pattern, r'\1\n' + get_top_link_html(country), content)
        else:
            # Fallback (maybe after the last button in the flex container)
            content = re.sub(r'(class="flex flex-wrap gap-4 mb-14">.*?)(\s*</div>)', r'\1' + get_top_link_html(country) + r'\2', content, flags=re.DOTALL)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print("Done moving PDF link back to top after the buttons!")
