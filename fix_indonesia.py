import os

path = r"c:\Users\User\Downloads\tilda dododo\pages\memos\indonesia.html"

with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Если файл в UTF-16
if not content or "Индонезия" not in content:
    try:
        with open(path, 'r', encoding='utf-16', errors='ignore') as f:
            content = f.read()
    except:
        pass

def replace_img_in_section(html, section_id, new_img_path):
    marker = f'id="{section_id}"'
    pos = html.find(marker)
    if pos == -1:
        print(f"Секция с ID '{section_id}' не найдена")
        return html
    
    # Ищем картинку в этой секции
    img_start = html.find('<img', pos)
    if img_start != -1:
        # Проверяем, что не ушли в следующую секцию
        next_section = html.find('id="', pos + len(marker))
        if next_section == -1 or img_start < next_section:
            img_end = html.find('>', img_start)
            # Сохраняем классы старой картинки, чтобы не поплыла верстка
            # Но если нужно заменить полностью - создаем новый тег
            new_tag = f'<img src="{new_img_path}" class="w-full h-auto rounded-3xl shadow-xl my-10" loading="lazy">'
            print(f"Успешно заменено фото в секции '{section_id}'")
            return html[:img_start] + new_tag + html[img_end+1:]
    
    print(f"Картинка в секции '{section_id}' не найдена")
    return html

# Заменяем по ID (как в вашем инспекторе)
content = replace_img_in_section(content, "pravila-lichnoj-gigieny-i-bezopasnosti", "../../67c80555103e525982394554_915 (1).jpg")

# На всякий случай оставляем и старые замены, если они нужны
# (Праздники и В отеле)
# Мы их уже сделали, но пусть будут в скрипте для целостности

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Индонезия обновлена!")
