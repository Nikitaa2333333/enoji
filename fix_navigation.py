import os
import re

MEMOS_DIR = r"pages\memos"

def update_navigation_text():
    # 1. Исправляем ссылки в навигации, где текст содержит "Полезная информация ..."
    # И заменяем его на "Полезная информация"
    # Также обрабатываем ссылки типа Посольство -> Полезная информация
    
    # 2. Обрабатываем ID секций
    # 3. Обрабатываем мобильное меню, если оно зашито статически (хотя обычно оно клонируется скриптом)
    
    files_updated = 0
    
    # Список слов-якорей, которые мы хотим заменить на "Полезная информация" в навигации
    nav_targets = [
        "Посольство",
        "Консульство",
        "Полезные контакты",
        "Embassy",
        "Useful Info"
    ]
    
    for filename in os.listdir(MEMOS_DIR):
        if not filename.endswith(".html"):
            continue
            
        filepath = os.path.join(MEMOS_DIR, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content
        
        # Шаг 1: Ищем ссылки, которые ведут на секции с полезной инфой или посольством
        # Сначала те, что явно называются poleznaya-informatsiya...
        pattern_poleznaya = re.compile(r'(<a\s+href="#poleznaya-informatsiya[^"]*"\s+class="nav-link">)(.*?)(</a>)', re.IGNORECASE | re.DOTALL)
        new_content = pattern_poleznaya.sub(r'\1Полезная информация\3', new_content)
        
        # Шаг 2: Ищем ссылки, которые ведут на #embassy (как в Мексике)
        pattern_embassy = re.compile(r'(<a\s+href="#embassy[^"]*"\s+class="nav-link">)(.*?)(</a>)', re.IGNORECASE | re.DOTALL)
        new_content = pattern_embassy.sub(r'\1Полезная информация\3', new_content)
        
        # Шаг 3: Сокращаем ID и href
        new_content = re.sub(r'id="poleznaya-informatsiya-[^"]+"', 'id="poleznaya-informatsiya"', new_content)
        new_content = re.sub(r'href="#poleznaya-informatsiya-[^"]+"', 'href="#poleznaya-informatsiya"', new_content)
        
        # Шаг 4: Если в навигации есть "Посольство" и это последняя или предпоследняя ссылка, 
        # то скорее всего это и есть наш блок
        # Но будем осторожны, заменим только если ссылка ведет на #embassy или #poleznaya...
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"[OK] {filename}: Navigation updated.")
            files_updated += 1
            
    print(f"\nTotal files updated: {files_updated}")

if __name__ == "__main__":
    update_navigation_text()
