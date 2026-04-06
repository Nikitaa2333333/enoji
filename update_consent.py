import os
import re

def update_html_files(root_dir):
    privacy_url = "http://127.0.0.1:5500/privacy.html"
    # Добавляем !important через синтаксис Tailwind (!underline), 
    # чтобы перекрыть глобальное правило "a { text-decoration: none !important; }"
    consent_html = f"""
        <div class="flex items-center gap-3 px-1 mb-6">
          <input type="checkbox" id="privacy-consent" name="privacy-consent" required class="w-5 h-5 text-black border-black/20 rounded transition-colors cursor-pointer" />
          <label for="privacy-consent" class="text-sm font-medium text-black cursor-pointer">
            Согласен на <a href="{privacy_url}" target="_blank" class="!text-black !underline underline-offset-4 decoration-black/40 hover:decoration-black transition-all">обработку персональных данных</a>
          </label>
        </div>"""

    targets = []
    for root, dirs, files in os.walk(root_dir):
        if any(d in root.lower() for d in ['.git', '.venv', 'tilda_raw', 'images', 'css']):
            continue
        for file in files:
            if file.endswith('.html'):
                targets.append(os.path.join(root, file))

    updated_count = 0
    for file_path in targets:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Перезаписываем блок privacy-consent новым стилем с !important
            if 'id="privacy-consent"' in content:
                old_block_pattern = r'<div class="flex items-center gap-3 px-1 mb-6">.*?id="privacy-consent".*?</div>'
                new_content = re.sub(old_block_pattern, consent_html.strip(), content, flags=re.DOTALL)
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    updated_count += 1
                continue

            # На случай новых файлов
            btn_pattern = r'(<button[^>]*type="submit"[^>]*>)'
            if re.search(btn_pattern, content):
                new_content = re.sub(btn_pattern, consent_html.strip() + r'\n\1', content)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_count += 1

        except Exception as e:
            print(f"Ошибка {file_path}: {e}")

    print(f"\nГотово! Форсированное подчеркивание применено в {updated_count} файлах.")

if __name__ == "__main__":
    update_html_files(".")
