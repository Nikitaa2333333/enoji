# scripts/test_memos.py
# --- !!! ЭТО ТЕСТОВЫЙ СКРИПТ (TEECT) !!! ---
import os
import re
import html
import shutil

# Пути
CWD = os.getcwd()
CONTENT_DIR = os.path.join(CWD, 'content')
TEMPLATE_MEMO = os.path.join(CWD, 'templates/template_memo.html')
TEMPLATE_COUNTRY = os.path.join(CWD, 'templates/template.html')
IMAGES_SRC = os.path.join(CWD, 'images')
IMAGES_DIST = os.path.join(CWD, 'images') # Кладем прямо в корень/images

def extract_hero_image(raw_html):
    """Ищет главную картинку обложки (Cover)."""
    match = re.search(r'data-content-cover-bg="([^"]+)"', raw_html)
    if match: return match.group(1)
    match = re.search(r'background-image:url\(\'([^\']+)\'\)', raw_html)
    if match: return match.group(1)
    return ""

def clean_content_smart(raw_html, is_memo=True):
    """Финальная версия: берет только то, что нужно, и ничего не теряет."""
    
    # 0. Убираем скрипты и стили
    html_no_scripts = re.sub(r'(?s)<style.*?>.*?</style>', '', raw_html)
    html_no_scripts = re.sub(r'(?s)<script.*?>.*?</script>', '', html_no_scripts)

    # 1. Собираем структуру МЕНЮ (избавляемся от дублей)
    menu_structure = []
    top_menu_matches = re.findall(r'href="(#submenu:[^"]+|#[^"]+)"[^>]*>(.*?)</a>', raw_html, re.IGNORECASE)
    
    all_anchors = []
    anchor_to_title = {}
    seen_anchors = set() # ДЛЯ БОРЬБЫ С ДУБЛЯМИ

    for href, title in top_menu_matches:
        clean_title = re.sub(r'<[^>]*>', '', title).replace('·', '').strip()
        if not clean_title or len(clean_title) < 2: continue
        
        if '#submenu:' in href:
            children = []
            sub_block_match = re.search(rf'data-tooltip-hook="{href}".*?>(.*?)</ul>', raw_html, re.DOTALL)
            if sub_block_match:
                sub_links = re.findall(r'href="(#[^"]+)"[^>]*>(.*?)</a>', sub_block_match.group(1), re.IGNORECASE)
                for s_href, s_title in sub_links:
                    anchor = s_href.replace('#', '')
                    if anchor in seen_anchors: continue # ПРОПУСКАЕМ ДУБЛЬ
                    
                    c_title = re.sub(r'<[^>]*>', '', s_title).strip()
                    children.append({'id': anchor, 'title': c_title})
                    all_anchors.append(anchor)
                    anchor_to_title[anchor] = c_title
                    seen_anchors.add(anchor)
            if children:
                menu_structure.append({'type': 'category', 'title': clean_title, 'links': children})
        else:
            anchor = href.replace('#', '')
            if anchor in seen_anchors or 'submenu' in anchor: continue # ПРОПУСКАЕМ ДУБЛЬ
            
            menu_structure.append({'type': 'link', 'id': anchor, 'title': clean_title})
            all_anchors.append(anchor)
            anchor_to_title[anchor] = clean_title
            seen_anchors.add(anchor)

    if not all_anchors: return "", ""

    # 2. ДЕЛИМ КОНТЕНТ
    # Очистим список якорей от дублей
    all_anchors = list(set(all_anchors))
    if not all_anchors: return "", ""

    # Сплитуем по всем ID и name из меню (добавляем \s+ для гибкости)
    regex_split = r'<(?:a\s+name|div\s+id|section\s+id)="(?:' + '|'.join(map(re.escape, all_anchors)) + r')"'
    parts = re.split(regex_split, html_no_scripts)
    tags = re.findall(regex_split, html_no_scripts)

    sections_html = ""
    for i in range(len(tags)):
        # Достаем ID из совпавшего тега
        anchor_match = re.search(r'="(rec\d+|[^"]+)"', tags[i])
        if not anchor_match: continue
        anchor = anchor_match.group(1)
        
        raw_content = parts[i+1]
        title = anchor_to_title.get(anchor, "")

        # Картинка
        img_match = re.search(r'data-original="([^"]+)"', raw_content)
        img_tag = ""
        if img_match:
            img_name = os.path.basename(img_match.group(1))
            if any(img_name.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                img_tag = f'<img src="images/{img_name}" class="w-full h-auto rounded-[3.5rem] shadow-xl mb-14">'

        # Текст
        # Заголовки H3: это ПОДЗАГОЛОВКИ внутри разделов (из Тильды 24px)
        raw_content = re.sub(r'<(strong|b|span)[^>]*style="[^"]*font-size:\s*(2[1-9]|3[0-9])px\s*;?[^"]*"[^>]*>(.*?)</\1>', 
                            r'<h3 class="text-2xl font-black mb-6 mt-12 text-black">\3</h3>', 
                            raw_content, flags=re.IGNORECASE | re.DOTALL)
        
        # 1. ЧИСТКА: Удаляем технический мусор Тильды в начале
        raw_content = re.sub(r'^[>\s]+', '', raw_content).strip()

        # 2. УДАЛЯЕМ НЕЖЕЛАТЕЛЬНЫЕ ТЕГИ целиком (div, span и прочее)
        # Оставляем только каркас
        text_content = re.sub(r'<(?!/?(strong|b|i|u|h3|li|ul|table|tr|td|thead|tbody|img|br|p|a)\b)[^>]+>', '', raw_content)
        
        # 3. ЧИСТИМ АТРИБУТЫ в оставшихся тегах (strong, li и т.д.)
        # Но оставляем важные для картинок и ссылок
        def clean_attributes(match):
            is_closing = match.group(1) # Это '/' если тег закрывающий
            tag_name = match.group(2).lower()
            if tag_name in ['img', 'a']:
                # Для картинок и ссылок оставляем всё
                return match.group(0)
            # Для всех остальных (strong, li, ul, h3) — убираем все атрибуты
            return f'<{is_closing}{tag_name}>'

        text_content = re.sub(r'<(/?)(\w+)([^>]*)>', clean_attributes, text_content)

        # 4. УДАЛЯЕМ ОШМЁТКИ И ГРЯЗЬ
        text_content = re.sub(r'\s*(class|style|id|data-[a-z-]+|target|field|imgfield)\s*=\s*"[^"]*"\s*', '', text_content)
        text_content = re.sub(r'(^|\s+)[>]\s*', ' ', text_content) # Удаляем висячие '>'
        text_content = re.sub(r'\s*>\s*$', '', text_content) # Хвосты в конце

        # 4. СПИСКИ: Теперь делаем списки из того, что осталось
        # Нормализуем буллиты
        text_content = text_content.replace('●', '•').replace('·', '•').replace('&bull;', '•').replace('&#8226;', '•')
        
        # Превращаем каждый буллит в <li>
        # Ищем '• текст' до конца строки или до следующего буллита/тега
        text_content = re.sub(r'•\s*(.*?)(?=\s*•|$|<br|<p|</li>)', r'<li>\1</li>', text_content)
        
        # Группируем идущие подряд <li> в один <ul> с нашим классом
        # Внутри <ul> чистим всё от лишних <br> и пробелов, чтобы не было гигантских отступов
        def list_wrapper(m):
            inner = m.group(0)
            inner = re.sub(r'<br\s*/?>', '', inner)
            inner = re.sub(r'\n', '', inner)
            return f'<ul class="check-list mb-12">{inner.strip()}</ul>'
            
        text_content = re.sub(r'(?s)(<li>.*?</li>\s*(<br\s*/?>\s*)*)+', list_wrapper, text_content)
        
        # 5. Финальные штрихи
        text_content = text_content.replace('\n', ' ').strip()
        
        # УДАЛЯЕМ ДЫРЫ только перед списками
        text_content = re.sub(r'(<br\s*/?>\s*)+(?=<ul)', '', text_content)
        
        # Схлопываем 3+ переноса в два (чтобы был отступ абзаца), но не в один!
        text_content = re.sub(r'(<br\s*/?>\s*){3,}', '<br><br>', text_content)
        
        # Если текст начинается без тега, оборачиваем в параграф
        # Но сначала чистим возможные висячие <br> в самом начале
        text_content = re.sub(r'^(<br\s*/?>\s*)+', '', text_content)
        
        if text_content and not text_content.startswith(('<ul', '<h3', '<h2', '<table', '<img')):
            text_content = f'<p class="mb-4">{text_content}</p>'

        if text_content.strip() or img_tag:
            header = f'<h2 class="text-4xl font-black mb-14 tracking-tight text-black">{title}</h2>'
            sections_html += f'<section id="{anchor}" class="scroll-mt-32 mb-24">{header}{img_tag}<div class="text-on-surface-variant font-medium text-xl leading-relaxed max-w-4xl">{text_content}</div><div class="h-px bg-black/[0.05] mt-12"></div></section>\n'

    # 3. МЕНЮ
    menu_html = ""
    for item in menu_structure:
        if item['type'] == 'category':
            menu_html += f'<div class="nav-category">{item["title"]}</div>\n'
            for link in item['links']:
                menu_html += f'<a href="#{link["id"]}" class="nav-link">{link["title"]}</a>\n'
        else:
            menu_html += f'<a href="#{item["id"]}" class="nav-link">{item["title"]}</a>\n'

    return sections_html, menu_html

def test_convert(input_file, output_name, is_memo):
    filepath = os.path.join(CONTENT_DIR, input_file)
    if not os.path.exists(filepath):
        print(f"❌ ОШИБКА: Файл {input_file} не найден!")
        return

    print(f"🚀 ТЕСТ: Конвертация {input_file}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        html_raw = f.read()

    template_file = TEMPLATE_MEMO if is_memo else TEMPLATE_COUNTRY
    with open(template_file, 'r', encoding='utf-8') as t:
        final_code = t.read()

    title = "Мальдивы"
    slug = "maldives"
    hero_url = extract_hero_image(html_raw) if not is_memo else ""
    
    content, menu = clean_content_smart(html_raw, is_memo)
    
    final_code = final_code.replace('██Название страны██', title)
    final_code = final_code.replace('██Название██', title)
    final_code = final_code.replace('██slug██', slug)
    final_code = final_code.replace('██hero.jpg██', hero_url)
    final_code = final_code.replace('<!-- Контент -->', content)
    final_code = final_code.replace('<!-- Ссылки -->', menu)
    final_code = final_code.replace('<!-- Мобильные ссылки -->', menu)

    if is_memo:
         final_code = final_code.replace('../countries/maldives.html', 'maldives_country_TEST.html')
    else:
         final_code = final_code.replace('../memos/maldives.html', 'maldives_memo_TEST.html')

    with open(os.path.join(CWD, output_name), 'w', encoding='utf-8') as out:
        out.write(final_code)
    print(f"✅ ТЕСТ ГОТОВ: {output_name}")

if __name__ == "__main__":
    print("\n--- ЗАПУСК ТЕСТОВОГО СКРИПТА ---")
    test_convert('m.txt', 'maldives_memo_TEST.html', True)
    test_convert('mm.txt', 'maldives_country_TEST.html', False)
    print("--- ТЕСТ ЗАВЕРШЕН ---\n")
