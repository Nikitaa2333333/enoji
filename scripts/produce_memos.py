# scripts/produce_memos.py
import os
import re
import html
import shutil
import zipfile

# --- НАСТРОЙКИ АВТОНОМНОГО ЗАВОДА ---
CWD = os.getcwd()
RAW_DIR = os.path.join(CWD, 'tilda_raw')
CONTENT_DIR = os.path.join(CWD, 'content')
DIST_DIR = os.path.join(CWD, 'dist_memos')
TEMPLATE_MEMO = os.path.join(CWD, 'templates/template_memo.html')
TEMPLATE_COUNTRY = os.path.join(CWD, 'templates/template.html')
IMAGES_SRC = os.path.join(CWD, 'images')
IMAGES_DIST = os.path.join(DIST_DIR, 'images')

def setup_folders():
    for d in [DIST_DIR, IMAGES_DIST, RAW_DIR]:
        if not os.path.exists(d): os.makedirs(d)

def extract_hero_image(raw_html):
    """Ищет главную картинку обложки (Cover)."""
    match = re.search(r'data-content-cover-bg="([^"]+)"', raw_html)
    if match: return match.group(1)
    match = re.search(r'background-image:url\(\'([^\']+)\'\)', raw_html)
    if match: return match.group(1)
    return ""

def clean_inner_text(raw_html_chunk):
    """Глубокая чистка контента внутри секции."""
    # 1. Убираем скрипты и стили внутри (на всякий случай)
    chunk = re.sub(r'(?s)<style.*?>.*?</style>', '', raw_html_chunk)
    chunk = re.sub(r'(?s)<script.*?>.*?</script>', '', chunk)
    
    # 2. ПОДЗАГОЛОВКИ H3: Тилда 24px или жирный текст с двоеточием
    chunk = re.sub(r'<(strong|b|span)[^>]*style="[^"]*font-size:\s*(2[1-9]|3[0-9])px\s*;?[^"]*"[^>]*>(.*?)</\1>', 
                   r'<h3 class="text-2xl font-black mb-6 mt-12 text-black">\3</h3>', 
                   chunk, flags=re.IGNORECASE | re.DOTALL)
    
    chunk = re.sub(r'<strong>\s*([^<]+:)\s*</strong>\s*<br\s*/?>',
                   r'<h3 class="text-2xl font-black mb-6 mt-12 text-black">\1</h3>',
                   chunk, flags=re.IGNORECASE)

    # 3. ЧИСТКА ТЕГОВ: Оставляем только каркас (strong, b, i, u, h3, li, ul, table, br, p, a, img)
    chunk = re.sub(r'<(?!/?(strong|b|i|u|h3|li|ul|table|tr|td|thead|tbody|img|br|p|a)\b)[^>]+>', '', chunk)
    
    # 4. ЧИСТКА АТРИБУТОВ (Убираем всё кроме src и href)
    def attr_cleaner(match):
        is_closing = match.group(1) 
        tag_name = match.group(2).lower()
        if tag_name in ['img', 'a']: return match.group(0) # Сохраняем ссылки и картинки полностью
        return f'<{is_closing}{tag_name}>'

    chunk = re.sub(r'<(/?)(\w+)([^>]*)>', attr_cleaner, chunk)
    chunk = re.sub(r'\s*(class|style|id|data-[a-z-]+|target|field|imgfield)\s*=\s*"[^"]*"\s*', '', chunk)
    chunk = chunk.replace('>', '>') # Нормализация
    chunk = re.sub(r'(^|\s+)[>]\s*', ' ', chunk) # Убираем висячие '>'

    # 5. СПИСКИ (Нормализуем буллиты и оборачиваем в <ul>)
    chunk = chunk.replace('●', '•').replace('·', '•').replace('&bull;', '•')
    chunk = re.sub(r'•\s*(.*?)(?=\s*•|$|<br|<p|</li>)', r'<li>\1</li>', chunk)
    
    def list_wrapper(m):
        inner = re.sub(r'<br\s*/?>|\n', '', m.group(0))
        return f'<ul class="check-list mb-12">{inner.strip()}</ul>'
    
    chunk = re.sub(r'(?s)(<li>.*?</li>\s*(<br\s*/?>\s*)*)+', list_wrapper, chunk)

    # 6. ЧИСТКА ЮРИДИЧЕСКОГО ФУТЕРА ТИЛЬДЫ (Убираем ИП Трохин и контакты)
    legal_patterns = [
        r"ЖЕЛАЕМ ВАМ ПРИЯТНОГО ПУТЕШЕСТВИЯ!",
        r"По всем вопросам свяжитесь с нами любым удобным способом.*",
        r"E-mail: trohin\.zh@yandex\.ru.*",
        r"Телефон: \+7 \(963\) 649-18-52.*",
        r"Соцсети: Вконтакте \|Telegram.*",
        r"Индивидуальный предприниматель Трохин Евгений Альбертович.*",
        r"ИНН 503613656680.*",
        r"ОГРН ИП 315507400016056.*"
    ]
    for pattern in legal_patterns:
        chunk = re.sub(pattern, "", chunk, flags=re.IGNORECASE)

    # 7. ФОРМАТИРОВАНИЕ: Абзацы и переносы
    chunk = chunk.replace('\n', ' ').strip()
    chunk = re.sub(r'(<br\s*/?>\s*)+(?=<ul)', '', chunk) # Убираем дыры перед списками
    chunk = re.sub(r'(<br\s*/?>\s*){3,}', '<br><br>', chunk) # Схлопываем лишнее
    chunk = re.sub(r'^(<br\s*/?>\s*)+', '', chunk) # Лишнее в начале
    
    # Оборачиваем в параграф, если не начинается со списка или заголовка
    if chunk and not chunk.startswith(('<ul', '<h3', '<table', '<img')):
        chunk = f'<p class="mb-4">{chunk}</p>'

    return chunk

def generate_page():
    setup_folders()
    
    # 1. Распаковка ZIP (если есть)
    for f in os.listdir(RAW_DIR):
        if f.endswith('.zip'):
            print(f"📦 Распаковка {f}...")
            with zipfile.ZipFile(os.path.join(RAW_DIR, f), 'r') as z:
                z.extractall(RAW_DIR)
            os.remove(os.path.join(RAW_DIR, f))

    # 2. Сканируем папку content (там лежат основные TXT) и RAW_DIR
    source_files = []
    # Сначала смотрим content (основное хранилище)
    if os.path.exists(CONTENT_DIR):
        for f in os.listdir(CONTENT_DIR):
            if f.endswith('.txt') and not f.startswith('тильда'):
                source_files.append((os.path.join(CONTENT_DIR, f), f))
    
    # Потом смотрим tilda_raw (рекурсивно для всех вложенных папок)
    for root, dirs, files in os.walk(RAW_DIR):
        for f in files:
            if f.endswith('.html') and 'template' not in f.lower():
                source_files.append((os.path.join(root, f), f))

    processed = 0
    for full_path, filename in source_files:
        if filename.endswith('body.html'):
            continue
            
        print(f"🔍 Обработка: {filename}")
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                html_raw = f.read()
        except UnicodeDecodeError:
            with open(full_path, 'r', encoding='windows-1251') as f:
                html_raw = f.read()

        # --- ОПРЕДЕЛЕНИЕ ТИПА И МЕТАДАННЫХ ---
        title_match = re.search(r'<title>(.*?)</title>', html_raw)
        raw_title = title_match.group(1) if title_match else ""
        
        alias_match = re.search(r'data-tilda-page-alias="(.*?)"', html_raw, re.IGNORECASE)
        page_alias = alias_match.group(1) if alias_match else ""

        # Тип страницы: по названию файла, по алиасу или по заголовку
        is_memo = ("памятка" in filename.lower() or 
                   "памятка" in raw_title.lower() or 
                   page_alias.startswith('memo') or
                   " m.txt" in filename.lower())
        template_file = TEMPLATE_MEMO if is_memo else TEMPLATE_COUNTRY

        with open(template_file, 'r', encoding='utf-8') as t:
            page_data = t.read()

        # Имена и Slug (Умное определение)
        title = raw_title.replace('Памятка:', '').replace('— Emoji Tours', '').replace('Emoji Tours', '').strip()
        if not title: title = filename.split('.')[0]
        
        slug = page_alias.replace('memo', '').strip('-')
        if not slug: slug = filename.replace('.html', '').replace('.txt', '').lower().replace('памятка_', '')
        
        # --- ТРАНСФОРМАЦИЯ КОНТЕНТА ---
        # 0. Ищем навигацию (якоря)
        id_to_title = {}
        links = re.findall(r'href="(#(?!submenu:)[^"]+)"[^>]*>(.*?)</a>', html_raw, re.IGNORECASE)
        for href, l_title in links:
            clean_l_title = re.sub(r'<[^>]*>', '', l_title).strip()
            if len(clean_l_title) > 2:
                id_to_title[href.replace('#', '')] = clean_l_title

        # 1. Режем на секции
        parts = re.split(r'<a name="([^"]+)"', html_raw)
        sections_html = ""
        menu_html = ""

        for i in range(1, len(parts), 2):
            anchor = parts[i]
            raw_sec_content = parts[i+1]
            sec_title = id_to_title.get(anchor, "")
            
            # Чистим внутренности
            final_text = clean_inner_text(raw_sec_content)

            # Обработка картинки в секции
            img_match = re.search(r'data-original="([^"]+)"', raw_sec_content)
            img_tag = ""
            if img_match:
                img_name = os.path.basename(img_match.group(1))
                img_tag = f'<img src="../../images/{img_name}" class="w-full h-auto rounded-[3.5rem] shadow-xl mb-14">'

            # Сборка секции (как в идеальном Египте)
            if final_text.strip() or img_tag:
                header_html = f'<h2 class="text-4xl font-black mb-14 tracking-tight text-black">{sec_title}</h2>' if sec_title else ""
                sections_html += f'''
                <section id="{anchor}" class="scroll-mt-32 mb-24">
                  {header_html}
                  {img_tag}
                  <div class="text-on-surface-variant font-medium text-xl leading-relaxed max-w-4xl">
                    {final_text}
                  </div>
                  <div class="h-px bg-black/[0.05] mt-12"></div>
                </section>'''
                
                if sec_title:
                    menu_html += f'<a href="#{anchor}" class="nav-link">{sec_title}</a>\n'

        # Hero Image
        hero_url = extract_hero_image(html_raw)
        
        # Сборка финальной страницы
        page_data = page_data.replace('██Название страны██', title)
        page_data = page_data.replace('██Название██', title)
        page_data = page_data.replace('██slug██', slug)
        page_data = page_data.replace('██hero.jpg██', hero_url)
        page_data = page_data.replace('<!-- Контент -->', sections_html)
        page_data = page_data.replace('<!-- Ссылки -->', menu_html)
        page_data = page_data.replace('<!-- Мобильные ссылки -->', menu_html)

        # Кнопки
        if is_memo:
            page_data = page_data.replace('../countries/██slug██.html', f'../countries/{slug}.html')
        else:
            page_data = page_data.replace('../memos/██slug██.html', f'../memos/{slug}.html')

        # Сохранение
        out_sub = 'memos' if is_memo else 'countries'
        out_dir = os.path.join(DIST_DIR, out_sub)
        if not os.path.exists(out_dir): os.makedirs(out_dir)
        
        out_path = os.path.join(out_dir, f"{slug}.html")
        with open(out_path, 'w', encoding='utf-8') as out:
            out.write(page_data)
        
        print(f"✨ Создано: {out_sub}/{slug}.html")
        processed += 1

    print(f"\n✅ ВСЕ СТРАНИЦЫ ОБНОВЛЕНЫ. Итого: {processed} в '{DIST_DIR}'")

if __name__ == "__main__":
    generate_page()
