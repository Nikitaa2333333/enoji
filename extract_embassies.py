import os
import re

def clean_html(raw_html):
    # Заменяем <br> на переносы строк
    text = re.sub(r'<br\s*/?>', '\n', raw_html, flags=re.IGNORECASE)
    # Форматируем жирный текст и курсив в markdown
    text = re.sub(r'</?(strong|b)>', '**', text, flags=re.IGNORECASE)
    text = re.sub(r'</?(em|i)>', '*', text, flags=re.IGNORECASE)
    # Удаляем все остальные HTML-теги
    text = re.sub(r'<[^>]+>', '', text)
    # Декодируем базовые HTML-сущности
    text = text.replace('&nbsp;', ' ').replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    # Убираем дублирующиеся пробелы
    text = re.sub(r'[ \t]+', ' ', text)
    # Убираем лишние пустые строки (более двух подряд)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Ошибка при чтении {filepath}: {e}")
        return []

    # Ищем начало блока (регистронезависимо)
    start_match = re.search(r'ПОЛЕЗНАЯ ИНФОРМАЦИЯ', content, flags=re.IGNORECASE)
    if not start_match:
        return []
    
    # Берем контент от "Полезная информация"
    useful_part = content[start_match.start():]
    
    # Ищем маркеры конца секции
    end_markers = [
        r'ЖЕЛАЕМ ВАМ ПРИЯТНОГО ПУТЕШЕСТВИЯ',
        r'id="section-form"',
        r'<footer',
        r'<!-- СЕКЦИЯ: ФОРМА -->',
        r'<!--/record' # Маркер конца блока в Тильде
    ]
    
    end_pos = len(useful_part)
    for marker in end_markers:
        m = re.search(marker, useful_part, flags=re.IGNORECASE)
        if m and m.start() < end_pos:
            end_pos = m.start()
            
    useful_part = useful_part[:end_pos]
    
    # Очистка
    text = clean_html(useful_part)
    
    # Если текста слишком много (скрипт зацепил лишнее), 
    # попробуем найти именно контактную информацию в этом блоке
    if len(text) > 5000:
        # Пытаемся ограничить блок только Контактами/Посольствами если он раздулся
        # Но пока оставим так, Танзания вроде не такая огромная
        pass

    if len(text) > 10:
        return [text]

    return []

def main():
    folders = ['pages/countries', 'pages/memos']
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    processed_countries = set()
    all_content = "# Полезная информация и посольства\n\n"
    
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        if not os.path.exists(folder_path):
            continue
            
        for filename in os.listdir(folder_path):
            if filename.endswith('.html'):
                country_key = filename.lower()
                if country_key in processed_countries:
                    continue
                    
                extracted = process_file(os.path.join(folder_path, filename))
                if extracted:
                    processed_countries.add(country_key)
                    country_name = filename.replace('.html', '').capitalize()
                    all_content += f"## {country_name}\n\n"
                    for text in extracted:
                        all_content += text + "\n\n"
                    all_content += "---\n\n"
                    
    output_file = os.path.join(base_dir, 'embassies.md')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(all_content)
        
    print(f"Готово! Извлечена информация для {len(processed_countries)} стран.")
    print(f"Файл обновлен: {output_file}")

if __name__ == "__main__":
    main()
