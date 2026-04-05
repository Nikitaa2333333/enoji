import os
import re

def fix_duplicates_in_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    seen_images = set()
    new_lines = []
    
    # Регулярка для поиска тега img и его src
    img_re = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']')

    for line in lines:
        match = img_re.search(line)
        if match:
            src = match.group(1)
            # Игнорируем логотипы и маленькие иконки (если нужно)
            if "logo.png" in src or "favicon" in src:
                new_lines.append(line)
                continue
            
            if src in seen_images:
                # Если изображение уже было, пропускаем эту строку (удаляем тег)
                print(f"  - Removing duplicate image: {src}")
                continue
            else:
                seen_images.add(src)
                new_lines.append(line)
        else:
            new_lines.append(line)

    # Сохраняем изменения
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            print(f"Processing {filename}...")
            fix_duplicates_in_file(os.path.join(directory, filename))

if __name__ == "__main__":
    memo_dir = r"pages\memos"
    if os.path.exists(memo_dir):
        process_directory(memo_dir)
        print("\nAll files processed successfully!")
    else:
        print(f"Directory {memo_dir} not found!")
