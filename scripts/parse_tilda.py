import re
import os
import html

def build_final_memo_fix_split_logic(tilda_file, template_file, output_file):
    print(f"--- ИСПРАВЛЕНИЕ ЛОГИКИ РАЗДЕЛЕНИЯ (ЗАГОЛОВОК + ТЕКСТ) ---")
    
    with open(tilda_file, 'r', encoding='utf-8') as f:
        tilda_html = f.read()
    with open(template_file, 'r', encoding='utf-8') as f:
        template = f.read()

    # 1. МЕНЮ
    nav_links = re.findall(r'href="(#(?:submenu:|rec)[^"]+)"[^>]*>(.*?)</a>', tilda_html)
    id_to_title = {}
    for href, title in nav_links:
        clean_cat = re.sub(r'<[^>]*>', '', title).strip()
        if not clean_cat or len(clean_cat) < 2: continue
        if 'submenu:' in href:
            sub_m = re.search(fr'data-tooltip-hook="{href}"(.*?)</ul', tilda_html, re.DOTALL)
            if sub_m:
                for sid, stitle in re.findall(r'href="(#[^"]+)"[^>]*>(.*?)</a>', sub_m.group(1)):
                    id_to_title[sid.replace('#', '')] = re.sub(r"<[^>]*>", "", stitle).strip()
        elif href.startswith('#rec'):
            id_to_title[href.replace('#', '')] = clean_cat

    # 2. КОНТЕНТ
    parts = re.split(r'<a name="[^"]+"', tilda_html)
    names = re.findall(r'<a name="([^"]+)"', tilda_html)
    content_html = ""
    
    all_blocks = []
    if len(parts) > 1:
        pure_t = re.sub(r'<[^>]*>', '', parts[0]).strip()
        if len(pure_t) > 50 and "menu" not in parts[0].lower():
            all_blocks.append(('intro', parts[0]))
    for i, name in enumerate(names):
        all_blocks.append((name, parts[i+1]))

    for name, raw_content in all_blocks:
        title = id_to_title.get(name, "")
        
        raw_content = html.unescape(raw_content)
        def wrap_table(m):
            t = m.group(0)
            t = re.sub(r'<tr[^>]*>', '<tr>', t)
            t = re.sub(r'<td[^>]*>', '<td class="py-4">', t)
            return f'<div class="table-container">{t}</div>'
        raw_content = re.sub(r'<table[^>]*>.*?</table>', wrap_table, raw_content, flags=re.DOTALL)

        # ТЕПЕРЬ ФОРМИРУЕМ h3 С ПЕРЕНОСАМИ СТРОК (\n), чтобы они не слипались с текстом
        raw_content = re.sub(r'<([a-z0-9]+)[^>]*font-size:\s*(?:2[2-9]|[3-9][0-9])px[^>]*>(.*?)</\1>', r'\n<h3>\2</h3>\n', raw_content, flags=re.DOTALL | re.IGNORECASE)
        
        raw_content = re.sub(r'<br\s*/?>', '\n', raw_content, flags=re.IGNORECASE)
        
        # Очистка (Сохраняем h3 и strong)
        clean_text = re.sub(r'<(?!/?(strong|b|i|u|h3|li|table|tr|td|thead|tbody)\b)[^>]+>', '\n', raw_content, flags=re.DOTALL)
        
        lines = [l.strip() for l in clean_text.split('\n') if l.strip()]
        final_elements = []
        p_buffer = []
        list_buffer = []
        
        for line in lines:
            if 'style=' in line and len(line) < 50: continue
            
            # БУЛЛИТЫ
            pure_line = re.sub(r'<[^>]*>', '', line).strip('\u200b\ufeff\xa0 ')
            is_bullet = bool(re.match(r'^[•●·⁃−\-—∗\*▪]', pure_line))
            
            if is_bullet:
                if p_buffer:
                    final_elements.append(f'<p class="mb-8">{" ".join(p_buffer)}</p>')
                    p_buffer = []
                clean_item = re.sub(r'^[•●·⁃−\-—∗\*▪]\s*', '', pure_line)
                list_buffer.append(clean_item)
            else:
                if list_buffer:
                    items_html = "".join([f'<li>{item}</li>' for item in list_buffer])
                    final_elements.append(f'<ul class="check-list mb-12">{items_html}</ul>')
                    list_buffer = []
                
                # РАСПОЗНАВАНИЕ h3
                if line.startswith('<h3>'):
                    if p_buffer:
                        # ТЕПЕРЬ СТРОГО ВЫВОДИМ ПРЕДЫДУЩИЙ ТЕКСТ ПЕРЕД h3
                        final_elements.append(f'<p class="mb-8">{" ".join(p_buffer)}</p>')
                        p_buffer = []
                    
                    # ПРОВЕРКА: Если в одной строке и h3 и текст (например, "<h3>Title</h3> Text")
                    # Мы их разъединяем
                    h3_match = re.match(r'^(<h3>.*?</h3>)(.*)', line, re.DOTALL)
                    if h3_match:
                        h_tag, remaining = h3_match.groups()
                        txt_h = re.sub(r"<[^>]*>", "", h_tag).strip()
                        final_elements.append(f'<h3 class="text-2xl font-black mb-6 mt-16 text-black">{txt_h}</h3>')
                        if remaining.strip():
                            p_buffer.append(remaining.strip())
                    else:
                        txt_h = re.sub(r"<[^>]*>", "", line).strip()
                        final_elements.append(f'<h3 class="text-2xl font-black mb-6 mt-16 text-black">{txt_h}</h3>')
                elif '<table' in line:
                    if p_buffer:
                        final_elements.append(f'<p class="mb-8">{" ".join(p_buffer)}</p>')
                        p_buffer = []
                    final_elements.append(line)
                else:
                    p_buffer.append(line)
        
        if list_buffer:
            items_html = "".join([f'<li>{item}</li>' for item in list_buffer])
            final_elements.append(f'<ul class="check-list mb-12">{items_html}</ul>')
        if p_buffer: final_elements.append(f'<p class="mb-8">{" ".join(p_buffer)}</p>')

        img_match = re.search(r'data-original="([^"]+)"', raw_content)
        img_tag = f'<img src="{img_match.group(1)}" class="w-full h-auto rounded-[3.5rem] shadow-xl mb-14" alt="{title}">' if img_match else ""

        if final_elements:
            header_fin = f'<h2 class="text-4xl font-black mb-14 tracking-tight leading-none text-black">{title}</h2>' if title else ""
            content_html += f'''
            <section id="{name}" class="scroll-mt-32 mb-32">
                {header_fin}
                {img_tag}
                <div class="text-on-surface-variant font-medium text-xl leading-relaxed max-w-4xl">
                    {"".join(final_elements)}
                </div>
                <div class="h-px bg-black/[0.05] mt-28"></div>
            </section>'''

    # МЕНЮ
    menu_html = ""
    for cat_raw in re.findall(r'href="(#(?:submenu:|rec)[^"]+)"[^>]*>(.*?)</a>', tilda_html):
        t_clean = re.sub(r"<[^>]*>", "", cat_raw[1]).strip()
        if not t_clean or len(t_clean) < 2: continue
        menu_html += f'<div class="nav-group"><p class="nav-category">{t_clean}</p>'
        if 'submenu:' in cat_raw[0]:
            sub_m = re.search(fr'data-tooltip-hook="{cat_raw[0]}"(.*?)</ul', tilda_html, re.DOTALL)
            if sub_m:
                for sid, stitle in re.findall(r'href="(#[^"]+)"[^>]*>(.*?)</a>', sub_m.group(1)):
                    menu_html += f'<a href="{sid}" class="nav-link">{re.sub(r"<[^>]*>", "", stitle).strip()}</a>'
        menu_html += f'</div>'

    output_res = template.replace('██Название страны██', 'Египет').replace('██Название██', 'Египет').replace('██slug██', 'egypt')
    output_res = output_res.replace('<!-- Ссылки -->', menu_html).replace('<!-- Мобильные ссылки -->', menu_html).replace('<!-- Контент -->', content_html)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_res)
    print(f"--- УСПЕХ: Логика разделения заголовка и текста исправлена! ---")

if __name__ == "__main__":
    build_final_memo_fix_split_logic('content/тильда.txt', 'templates/template_memo.html', 'labs/egypt_final.html')
