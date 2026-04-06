import os

path = r"c:\Users\User\Downloads\tilda dododo\pages\countries\sri-lanka.html"

# Открываем файл с игнорированием ошибок кодировки для чтения
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Пытаемся также прочитать в другой кодировке если пуст или проблемы (на всякий случай)
if not content or 'west-coast' not in content:
    try:
        with open(path, 'r', encoding='utf-16', errors='ignore') as f:
            content = f.read()
    except:
        pass

sections = {
    'west-coast': '../../SHri-Lanka-1.jpg',
    'south-coast': '../../wpid-img_20141011_15.jpg',
    'east-coast': '../../IMG_8533.jpg'
}

for section_id, img_path in sections.items():
    img_tag = f'<img src="{img_path}" class="w-full h-auto rounded-3xl shadow-xl mb-14" loading="lazy">'
    marker = f'id="{section_id}"'
    if marker in content:
        # Ищем заголовок h2 после id секции
        start_search = content.find(marker)
        h2_end = content.find('</h2>', start_search)
        if h2_end != -1:
            # Вставляем после </h2>
            content = content[:h2_end+5] + "\n          " + img_tag + content[h2_end+5:]
            print(f"Добавлено фото в {section_id}")
    else:
        print(f"Секция {section_id} не найдена")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Готово!")
