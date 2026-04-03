import pdfplumber
import os
import re
import json

# Настройки путей
BASE_DIR = r"c:\Users\User\Downloads\tilda dododo"
OUTPUT_DIR = os.path.join(BASE_DIR, "pages", "memos")
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "template_memo.html")

SLUG_MAP = {
    "Египет": "egypt", "Индонезия": "indonesia", "Китай": "china", "Маврикий": "mauritius",
    "Мальдивы": "maldives", "Сейшелы": "seychelles", "Тайланд": "thailand", "Таиланд": "thailand",
    "Танзания": "tanzania", "Тунис": "tunisia", "Турция": "turkey", "Шри-Ланка": "sri-lanka", 
    "Вьетнам": "vietnam", "ОАЭ": "uae"
}

# Подготовка маппинга для JSON (названия стран в memo_images.json часто в другом падеже)
JSON_COUNTRY_MAP = {
    "Танзания": "Танзанию",
    "Индонезия": "Индонезию",
    "Шри-Ланка": "Шри-ланку",
    "Турция": "Турцию",
    "Таиланд": "Таиланд",
    "Тайланд": "Таиланд",
    "Египет": "Египет",
    "Китай": "Китай",
    "Маврикий": "Маврикий",
    "Мальдивы": "Мальдивы",
    "Сейшелы": "Сейшелы",
    "Тунис": "Тунис",
    "ОАЭ": "Оаэ",
    "Вьетнам": "Вьетнам",
    "Кипр": "Республику кипр",
    "Доминикана": "Доминиканскую республику",
    "Израиль": "Государство израиль",
    "Куба": "Республику куба",
    "Индия": "Индию",
    "Мексика": "Мексику",
}

# ЧЕРНЫЙ СПИСОК
BLACK_LIST = ["Приятного путешествия!", "2025 год", "ПАМЯТКА ТУРИСТУ", "ПАМЯТКА ТУРИСТА"]
STOP_PHRASES = ["Краткий разговорник", "Фраза По-арабски Произношение"]

# Правильная транслитерация для ID
def slugify_latin(text):
    trans_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
        'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
        'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
    }
    text = text.lower()
    for cyr, lat in trans_map.items():
        text = text.replace(cyr, lat)
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text if text else "section"

def get_obj_top(obj, h):
    return obj['top'] if 'top' in obj else h - obj['y1']

def has_underline(page, line_words):
    if not line_words: return False
    h = page.height
    t_top = min(w['top'] for w in line_words)
    t_bottom = max(w['bottom'] for w in line_words)
    t_x0 = min(w['x0'] for w in line_words)
    t_x1 = max(w['x1'] for w in line_words)
    search_min_y = t_top + (t_bottom - t_top) / 2
    search_max_y = t_bottom + 8
    objs = page.lines + page.rects + page.curves
    for obj in objs:
        o_top = get_obj_top(obj, h)
        if o_top is None: continue
        if search_min_y <= o_top <= search_max_y:
            o_x0 = obj.get('x0', 0); o_x1 = obj.get('x1', 0)
            overlap_x0 = max(t_x0, o_x0); overlap_x1 = min(t_x1, o_x1)
            if overlap_x1 > overlap_x0 and (overlap_x1 - overlap_x0) / (t_x1 - t_x0) > 0.4:
                return True
    return False

def find_column_divider(page):
    h = page.height
    v_lines = []
    for obj in (page.lines + page.rects):
        top = get_obj_top(obj, h); height = obj.get('height', abs(obj.get('bottom', 0) - obj.get('top', 0)))
        if top < 80 or (top + height) > (h - 80): continue
        is_v = False
        if 'width' in obj and obj['width'] < 2 and height > (h * 0.1): is_v, x = True, obj['x0']
        elif obj.get('x0') == obj.get('x1') and height > (h * 0.1): is_v, x = True, obj['x0']
        if is_v and 200 < x < 400: v_lines.append(x)
    return max(set(v_lines), key=v_lines.count) if v_lines else 300 

def extract_pdf(pdf_path):
    structure, h1_found, stop_parsing = [], False, False
    is_embassy_section = False
    is_vietnam = "вьетнам" in pdf_path.lower()
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            if stop_parsing: break
            divider_x = find_column_divider(page)
            words = page.extract_words(extra_attrs=["fontname", "size"])
            if not words: continue
            
            words.sort(key=lambda x: (x['top'], x['x0']))
            lines_data = []
            curr_l = [words[0]]
            for i in range(1, len(words)):
                if abs(words[i]['top'] - words[i-1]['top']) < 3: curr_l.append(words[i])
                else: lines_data.append(curr_l); curr_l = [words[i]]
            lines_data.append(curr_l)
            
            curr_b, curr_t, last_bot = [], None, 0
            for line in lines_data:
                plain = " ".join([w['text'] for w in line]).strip()
                if not plain: continue
                if any(sp in plain for sp in STOP_PHRASES): stop_parsing = True; break
                if any(bl.lower() in plain.lower() for bl in BLACK_LIST): continue
                
                avg_s = sum([w['size'] for w in line]) / len(line)
                is_bold_f = any(k in line[0]['fontname'].lower() for k in ["bold", "heavy", "700", "800"])
                gap = line[0]['top'] - last_bot if last_bot else 0
                
                if is_bold_f and avg_s >= 11.4:
                    is_embassy_section = "полезная информация" in plain.lower() or "посольства" in plain.lower()
                    if curr_b: structure.append((f"{curr_t} " if curr_t else "") + " ".join(curr_b))
                    curr_t = "[H1]" if not h1_found else "[H2]"; h1_found = True; curr_b = [plain]
                elif is_embassy_section and divider_x:
                    tab_in, new_l = False, [line[0]]
                    for i in range(1, len(line)):
                        if line[i-1]['x1'] < divider_x and line[i]['x0'] > divider_x: new_l.append({"text":"[TAB]"}); tab_in = True
                        new_l.append(line[i])
                    if line[0]['x0'] > divider_x + 10: new_l.insert(0, {"text":"[TAB]"}); tab_in = True
                    raw_p = []
                    for w in new_l:
                        if w['text'] == "[TAB]": raw_p.append("[TAB]")
                        else:
                            is_b = any(k in w.get('fontname','').lower() for k in ["bold", "heavy", "700", "800"])
                            raw_p.append(f"<b>{w['text']}</b>" if is_b else w['text'])
                    raw_text = " ".join(raw_p).replace(" [TAB] ", "[TAB]").replace("[TAB] ", "[TAB]").replace(" [TAB]", "[TAB]")
                    if tab_in:
                        if curr_b: structure.append((f"{curr_t} " if curr_t else "") + " ".join(curr_b))
                        curr_t, curr_b = "[TABLE]", [raw_text]
                    else: curr_b.append(raw_text)
                elif is_bold_f and (has_underline(page, line) or (is_vietnam and avg_s > 9.5 and gap > 15)):
                    if curr_b: structure.append((f"{curr_t} " if curr_t else "") + " ".join(curr_b))
                    curr_t, curr_b = "[H3]", [plain]
                elif plain.startswith(("-", "•", "—", "●")):
                    if curr_b: structure.append((f"{curr_t} " if curr_t else "") + " ".join(curr_b))
                    curr_t, curr_b = "[BULLET]", [re.sub(r'^[\-•—●]\s*', '', plain)]
                elif gap < 5 and curr_b and curr_t not in ["[H1]", "[H2]", "[H3]"]:
                    curr_b.append(f"<b>{plain}</b>" if is_bold_f else plain)
                else:
                    if curr_b: structure.append((f"{curr_t} " if curr_t else "") + " ".join(curr_b))
                    curr_t, curr_b = None, [f"<b>{plain}</b>" if is_bold_f else plain]
                last_bot = line[0]['bottom']
            if curr_b and not stop_parsing: structure.append((f"{curr_t} " if curr_t else "") + " ".join(curr_b))
    return structure

def render_html(lines, country_name, slug, memo_images=None):
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f: template = f.read()
    main_c, nav_l, in_list, table_buf = "", "", False, []
    
    # Подготовка изображений для этой страны
    json_key = JSON_COUNTRY_MAP.get(country_name, country_name)
    country_imgs = memo_images.get(json_key, {}) if memo_images else {}
    used_images = set()

    def get_image_html(text):
        nonlocal used_images
        clean_text = re.sub(r'</?b>', '', text).lower().strip()
        for img_key, img_path in country_imgs.items():
            if img_key.lower().strip() in clean_text and img_path not in used_images:
                used_images.add(img_path)
                return f'<img src="../../{img_path}" class="w-full h-auto rounded-[2rem] md:rounded-[3.5rem] shadow-2xl my-16 object-cover" alt="{img_key}">\n'
        return ""

    def flush_table():
        nonlocal main_c, table_buf
        if table_buf:
            try:
                import scripts.embassy_overrides as overrides
                if slug in overrides.EMBASSY_OVERRIDES:
                    main_c += '<div class="space-y-12 my-10">\n'
                    for item in overrides.EMBASSY_OVERRIDES[slug]:
                        hdr = item['name']
                        bdy = item['body'].replace("\n", "<br>\n")
                        main_c += f'  <div>\n'
                        main_c += f'    <h3 class="text-2xl font-black mb-4 text-black">{hdr}</h3>\n'
                        main_c += f'    <p class="text-lg text-black/80 leading-relaxed font-manrope">{bdy}</p>\n'
                        main_c += f'  </div>\n'
                    main_c += '</div>\n'; table_buf = []
                    return
            except ImportError: pass

            c1, c2 = [], []
            for lb in table_buf:
                pts = lb.replace("[TABLE]", "").strip().split("[TAB]")
                if len(pts) == 1:
                    txt = pts[0]; split_idx = -1
                    for kw in ["Посольство", "Адрес:", "Тел.:", "E-mail:", "Сайт:"]:
                        first = txt.find(kw)
                        if first != -1:
                            second = txt.find(kw, first + 1)
                            if second != -1: split_idx = second; break
                    if split_idx != -1: c1.append(txt[:split_idx].strip()); c2.append(txt[split_idx:].strip())
                    else: c1.append(txt); c2.append("")
                else:
                    c1.append(pts[0] if len(pts)>0 else ""); c2.append(pts[1] if len(pts)>1 else "")
            
            main_c += '<div class="space-y-12 my-10">\n'
            for col in [c1, c2]:
                cl = [p for p in col if p.strip()]
                if not cl: continue
                hdr = re.sub(r'</?b>', '', cl[0]).strip()
                bdy_lines = []
                for p in cl[1:]:
                    p = p.replace("<b>", '<span class="font-bold text-black">').replace("</b>", '</span>')
                    bdy_lines.append(p)
                bdy = "<br>\n".join(bdy_lines)
                main_c += f'  <div>\n'
                main_c += f'    <h3 class="text-2xl font-black mb-4 text-black">{hdr}</h3>\n'
                main_c += f'    <p class="text-lg text-black/80 leading-relaxed font-manrope">{bdy}</p>\n'
                main_c += f'  </div>\n'
            main_c += '</div>\n'; table_buf = []

    for line in lines:
        line = line.strip()
        if not line: continue
        if not line.startswith("[TABLE]") and table_buf: flush_table()
        
        img_html = get_image_html(line)
        if img_html: main_c += img_html

        line = re.sub(r'<b>(.*?)</b>', r'<span class="font-bold text-black">\1</span>', line)
        if line.startswith("[H2]"):
            if in_list: main_c += "</ul>\n"; in_list = False
            txt = line.replace("[H2]", "").strip(); slg = slugify_latin(txt)
            main_c += f'<section id="{slg}" class="scroll-mt-32 mb-20">\n'
            main_c += f'  <h2 class="text-3xl md:text-5xl font-black mb-10 tracking-tight text-black">{txt}</h2>\n'
            nav_l += f'<a href="#{slg}" class="nav-link">{txt}</a>\n'
        elif line.startswith("[H3]"):
            if in_list: main_c += "</ul>\n"; in_list = False
            txt = line.replace("[H3]", "").strip()
            main_c += f'  <h3 class="text-2xl font-bold mt-12 mb-6 underline decoration-primary underline-offset-8 text-black">{txt}</h3>\n'
        elif line.startswith("[BULLET]"):
            if not in_list: main_c += '  <ul class="check-list mb-8">\n'; in_list = True
            main_c += f'    <li>{line.replace("[BULLET]", "").strip()}</li>\n'
        elif line.startswith("[TABLE]"):
            if in_list: main_c += "</ul>\n"; in_list = False
            table_buf.append(line)
        elif not line.startswith("[H1]"):
            if in_list: main_c += "</ul>\n"; in_list = False
            main_c += f'  <p class="mb-6 text-xl text-black/80 leading-relaxed font-manrope">{line}</p>\n'
    
    flush_table()
    if in_list: main_c += "</ul>\n"
    res = template.replace("██Название страны██", country_name).replace("██Название██", country_name).replace("██slug██", slug)
    res = res.replace("<!-- Контент -->", main_c).replace("<!-- Ссылки -->", nav_l)
    return res

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    
    images_db_path = os.path.join(BASE_DIR, "scripts", "memo_images.json")
    memo_images = {}
    if os.path.exists(images_db_path):
        try:
            with open(images_db_path, "r", encoding="utf-8") as f:
                memo_images = json.load(f)
            print(f"База картинок загружена: {len(memo_images)} стран")
        except Exception as e: print(f"Ошибка загрузки memo_images.json: {e}")

    pdf_files = [f for f in os.listdir(BASE_DIR) if f.startswith("Памятка туриста") and f.endswith(".pdf")]
    for pdf_file in pdf_files:
        c_name = re.sub(r'Памятка туриста\s+', '', pdf_file).replace('.pdf', '').strip()
        slug = SLUG_MAP.get(c_name, "memo")
        print(f"--- Обработка: {c_name} ---")
        try:
            lines = extract_pdf(os.path.join(BASE_DIR, pdf_file))
            html = render_html(lines, c_name, slug, memo_images)
            filename = os.path.join(OUTPUT_DIR, f"{slug}.html")
            with open(filename, "w", encoding="utf-8") as f: f.write(html)
            print(f"Успех: {slug}.html")
        except Exception as e: 
            print(f"Ошибка {c_name}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__": main()
