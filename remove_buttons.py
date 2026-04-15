import os
import re

memos_dir = r"pages\memos"

for filename in os.listdir(memos_dir):
    if not filename.endswith(".html"):
        continue
    
    filepath = os.path.join(memos_dir, filename)
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Удаляем белую кнопку (rounded-full), оставляем только текстовую ссылку
    # Регулярка ищет иконку picture_as_pdf и текст Скачать PDF внутри ссылки с классом rounded-full
    pattern = r'<a\s+href="[^"]+"\s+target="_blank"\s+class="[^"]*rounded-full[^"]*">.*?\s+Скачать\s+PDF\s+</a>'
    
    new_content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Removed button from {filename}")
    else:
        # Пытаемся найти сокращенный вариант если первый не сработал
        pattern2 = r'<a\s+href="[^"]+"\s+target="_blank"\s+class="[^"]*rounded-full[^"]*">.*?Скачать\s+PDF.*?</a>'
        new_content2 = re.sub(pattern2, '', content, flags=re.DOTALL)
        if new_content2 != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content2)
            print(f"Removed button from {filename} (v2)")
