import os
import re

def standardize_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Сначала исправляем порядок: Фото перед Заголовком -> Заголовок, затем Фото
    swap_pattern = re.compile(r'(<img[^>]+src=["\'][^"\']+["\'][^>]*>)\s*(<(h[23])[^>]*>.*?</\3>)', re.DOTALL)
    while True:
        new_content, count = swap_pattern.subn(r'\2\n\1', content)
        if count == 0:
            break
        content = new_content
        print(f"  - Swapping image with header ({count} times)")

    # 2. Удаляем абсолютно ВСЕ дубли (по src)
    seen_srcs = set()
    def remove_duplicates_src(match):
        full_tag = match.group(0)
        src = match.group(1)
        if "logo.png" in src: # Не трогаем логотип
            return full_tag
        if src in seen_srcs:
            return ""
        seen_srcs.add(src)
        return full_tag
    content = re.sub(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', remove_duplicates_src, content)

    # 3. Самое важное: Удаляем ИДУЩИЕ ПОДРЯД картинки
    # Ищем последовательность тегов img, разделенных только пробелами/переносами
    sequential_pattern = re.compile(r'(<img[^>]+src=["\'][^"\']+["\'][^>]*>)\s*(<img[^>]+src=["\'][^"\']+["\'][^>]*>)', re.DOTALL)
    while True:
        # Оставляем только ПЕРВУЮ картинку из последовательности
        new_content, count = sequential_pattern.subn(r'\1', content)
        if count == 0:
            break
        content = new_content
        print(f"  - Removing sequential images ({count} times)")

    # 4. Чистка лишних пустых строк
    content = re.sub(r'\n\s*\n', '\n\n', content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_all_memos(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            print(f"Final Standardization of {filename}...")
            standardize_file(os.path.join(directory, filename))

if __name__ == "__main__":
    memo_dir = r"pages\memos"
    if os.path.exists(memo_dir) :
        process_all_memos(memo_dir)
        print("\nAll memo pages standardized and sequential images removed!")
    else:
        print(f"Directory {memo_dir} not found!")
