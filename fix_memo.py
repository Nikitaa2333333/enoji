import os

path = r"c:\Users\User\Downloads\tilda dododo\pages\memos\sri-lanka.html"
new_img = "../../Sri_Lanka-Bandaranaike_International_Airport-flickr.com-anshu_si.jpg"

# Текст, после которого нужно искать картинку
marker_text = "Обращаем внимание на перевозку дронов"

with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Если файл в UTF-16
if not content or marker_text not in content:
    try:
        with open(path, 'r', encoding='utf-16', errors='ignore') as f:
            content = f.read()
    except:
        pass

if marker_text in content:
    # Ищем следующий тег <img после текста про дронов
    start_pos = content.find(marker_text)
    img_start = content.find('<img', start_pos)
    if img_start != -1:
        img_end = content.find('>', img_start)
        # Заменяем старый тег <img> на новый
        new_tag = f'<img src="{new_img}" class="w-full h-auto rounded-3xl shadow-xl my-10" loading="lazy">'
        content = content[:img_start] + new_tag + content[img_end+1:]
        print("Фото в памятке успешно заменено!")
    else:
        print("Тег img после текста про дронов не найден.")
else:
    print("Текст про дронов не найден в файле.")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Завершено.")
