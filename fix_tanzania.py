import os

path = r"c:\Users\User\Downloads\tilda dododo\pages\memos\tanzania.html"

with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Если файл в UTF-16
if not content or "Танзания" not in content:
    try:
        with open(path, 'r', encoding='utf-16', errors='ignore') as f:
            content = f.read()
    except:
        pass

def replace_img_after_text(html, text, new_img_path):
    pos = html.find(text)
    if pos == -1:
        print(f"Текст '{text}' не найден")
        return html
    img_start = html.find('<img', pos)
    if img_start != -1:
        img_end = html.find('>', img_start)
        new_tag = f'<img src="{new_img_path}" class="w-full h-auto rounded-3xl shadow-xl my-10" loading="lazy">'
        print(f"Заменено фото после '{text}'")
        return html[:img_start] + new_tag + html[img_end+1:]
    return html

# 1. Праздники и нерабочие дни
content = replace_img_after_text(content, "Праздники и нерабочие дни", "../../bpni4rxtb0y7lsgvp7yu7db74vrdjkgc.webp")

# 2. В отеле
content = replace_img_after_text(content, "В отеле", "../../oteli-tanzanii-15761465329474_w687h357.jpg")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Танзания полностью обновлена!")
