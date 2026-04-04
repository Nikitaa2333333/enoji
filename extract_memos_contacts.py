import os
import re
from bs4 import BeautifulSoup

# Define the directory and the target files
BASE_DIR = r"c:\Users\User\Downloads\tilda dododo"
MEMOS_DIR = os.path.join(BASE_DIR, "pages", "memos")

COUNTRIES = [
    "egypt", "maldives", "turkey", "vietnam", "china", 
    "mauritius", "thailand", "seychelles", "indonesia", 
    "sri-lanka", "tanzania", "tunisia"
]

COUNTRY_NAMES = {
    "egypt": "Египет",
    "maldives": "Мальдивы",
    "turkey": "Турция",
    "vietnam": "Вьетнам",
    "china": "Китай",
    "mauritius": "Маврикий",
    "thailand": "Таиланд",
    "seychelles": "Сейшелы",
    "indonesia": "Индонезия",
    "sri-lanka": "Шри-Ланка",
    "tanzania": "Танзания",
    "tunisia": "Тунис"
}

output_lines = []

for country_id in COUNTRIES:
    file_path = os.path.join(MEMOS_DIR, f"{country_id}.html")
    
    if not os.path.exists(file_path):
        print(f"Файл не найден: {file_path}")
        continue
        
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Пытаемся найти по id
    section = soup.find(id="poleznaya-informatsiya")
    
    # Если нет id, ищем по заголовку
    if not section:
        headers = soup.find_all(["h2", "h3", "h4", "div", "p"], string=re.compile(r"Полезная информация|Контакты", re.IGNORECASE))
        if headers:
            # Берем первый найденный и пытаемся взять его родителя (например, section или div)
            header = headers[-1] # Последний обычно более релевантен, если их несколько, но давайте первый
            header = headers[0]
            section = header.find_parent("section")
            if not section:
                # Если нет section, берем родительский div, который содержит больше элементов
                section = header.find_parent("div")
    
    if section:
        output_lines.append("=" * 60)
        output_lines.append(f"СТРАНА: {COUNTRY_NAMES.get(country_id, country_id).upper()}")
        output_lines.append("=" * 60)
        
        # Удаляем иконки, чтобы их текст (например, 'account_balance') не попадал в txt
        for icon in section.find_all(class_=re.compile(r"material-symbols-outlined|icon|svg")):
            icon.decompose()
            
        # Удаляем скрытые элементы
        for hidden in section.find_all(style=re.compile(r"display:\s*none")):
            hidden.decompose()
            
        # Заменяем все теги br на переносы строк
        for br in section.find_all("br"):
            br.replace_with("\n")
            
        # Извлекаем текст
        text_content = section.get_text(separator="\n", strip=True)
        
        # Очищаем лишние пустые строки (более двух)
        clean_text = re.sub(r'\n{3,}', '\n\n', text_content)
        
        output_lines.append(clean_text)
        output_lines.append("\n\n")
    else:
        print(f"Блок 'Полезная информация' не найден в {country_id}.html")

output_file = os.path.join(BASE_DIR, "embassy_contacts.txt")
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))
    
print(f"\nГотово! Все контакты и посольства успешно сохранены в файл: {output_file}")
