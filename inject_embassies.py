import os
import re

MD_FILE = "embassies.md"
MEMOS_DIR = r"pages\memos"

COUNTRY_MAP = {
    'Dominikana': 'dominikana.html',
    'Touriststravelingtoturkey': 'turkey.html',
    'Turkey': 'turkey.html',
    'China': 'china.html',
    'Cuba': 'cuba.html',
    'Egypt': 'egypt.html',
    'Indonesia': 'indonesia.html',
    'Israel': 'israel.html',
    'Maldives': 'maldives.html',
    'Mauritius': 'mauritius.html',
    'Oae': 'oae.html',
    'Seychelles': 'seychelles.html',
    'Sri-lanka': 'sri-lanka.html',
    'Tanzania': 'tanzania.html',
    'Thailand': 'thailand.html',
    'Vietnam': 'vietnam.html'
}

def parse_md():
    if not os.path.exists(MD_FILE):
        return {}
    with open(MD_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    countries = {}
    parts = re.split(r'^##\s+(.+)$', content, flags=re.MULTILINE)
    
    for i in range(1, len(parts), 2):
        name = parts[i].strip()
        text = parts[i+1]
        
        paragraphs = text.split('\n\n')
        unique_paras = []
        for p in paragraphs:
            p_strip = p.strip()
            if not p_strip or p_strip == '---' or 'ПОЛЕЗНАЯ ИНФОРМАЦИЯ' in p_strip or 'Полезная информация' in p_strip:
                continue
            if p_strip not in unique_paras:
                unique_paras.append(p_strip)
                
        countries[name] = unique_paras
        
    return countries

def generate_html_for_country(paragraphs):
    if not paragraphs:
        return ""
    
    html = []
    html.append('  <h2 class="text-3xl md:text-5xl font-black mb-10 tracking-tight text-black">Полезная информация</h2>\n')
    
    cards = []
    texts = []
    
    for p in paragraphs:
        # Мы ищем только те блоки, которые похожи на контактную информацию посольств
        if any(keyword in p for keyword in ["Адрес", "Тел", "Факс", "E-mail", "Посольство", "Консульство", "Линия"]):
             # Но если текста слишком много (больше 1000 символов), это скорее всего общая инфа, которую мы выкачали лишней
             if len(p) < 1500:
                cards.append(p)
             else:
                pass # Пропускаем лишний текст (таможню, правила и т.д.)
        else:
            # Текстовые блоки пропускаем, так как они в Танзании и др. и так есть выше
            pass
    
    def process_cards():
        if not cards:
            return ""
        
        res = []
        if len(cards) == 1:
             res.append('  <div class="max-w-3xl mb-10">')
        else:
             res.append('  <div class="grid grid-cols-1 xl:grid-cols-2 gap-8 mb-10">')
            
        for card in cards:
            lines = [l.strip() for l in card.split('\n') if l.strip()]
            header = ""
            body = []
            
            if lines:
                if lines[0].startswith('**') and lines[0].endswith('**'):
                    header = lines[0].strip('*')
                    body = lines[1:]
                elif '**' in lines[0]:
                    header_match = re.search(r'\*\*(.*?)\*\*', lines[0])
                    if header_match:
                        header = header_match.group(1).strip()
                        body_start = lines[0].replace('**' + header + '**', '').strip()
                        if body_start:
                            body.append(body_start)
                        body.extend(lines[1:])
                    else:
                        header = "Полезная информация"
                        body = lines
                else:
                    header = "Полезные контакты"
                    body = lines
            
            fmt_body = []
            for b in body:
                b = re.sub(r'\*\*(.*?)\*\*', r'<span class="font-bold text-black">\1</span>', b)
                b = b.replace('<br>', '').replace('</br>', '')
                fmt_body.append(f'<p class="mb-2 text-lg text-black/80 font-medium leading-relaxed">{b}</p>')
            
            icon = "account_balance" if any(k in header for k in ["Посольство", "Консульство"]) else "support_agent"
            
            card_html = f'''    <div class="bg-black/5 p-8 rounded-[2.5rem] border border-black/5 hover:bg-black/[0.07] transition-all duration-300">
      <div class="flex items-start gap-5 mb-8">
        <div class="w-12 h-12 bg-primary rounded-2xl flex items-center justify-center flex-shrink-0">
          <span class="material-symbols-outlined text-black text-2xl">{icon}</span>
        </div>
        <h3 class="text-2xl font-extrabold leading-tight tracking-normal">{header}</h3>
      </div>
      <div class="space-y-4">
        {''.join(fmt_body)}
      </div>
    </div>'''
            res.append(card_html)
            
        res.append('  </div>')
        return '\n'.join(res)

    cards_html = process_cards()
    if cards_html:
        html.append(cards_html)
        
    return '\n'.join(html)

def update_memos():
    countries_data = parse_md()
    
    for md_name, paragraphs in countries_data.items():
        if md_name not in COUNTRY_MAP:
            continue
            
        filename = COUNTRY_MAP[md_name]
        filepath = os.path.join(MEMOS_DIR, filename)
        
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_html = generate_html_for_country(paragraphs)
        
        # Полностью защищенный метод замены через индексы (без re.sub)
        section_search = re.search(r'(<section\s+id="poleznaya-[^>]*>)', content)
        if section_search:
            tag_str = section_search.group(1)
            start_pos = content.find(tag_str)
            end_pos = content.find('</section>', start_pos)
            if start_pos != -1 and end_pos != -1:
                content = content[:start_pos + len(tag_str)] + "\n" + new_html + "\n" + content[end_pos:]
                print(f"[OK] {filename}: Updated via splice.")
        else:
            p_search = re.search(r'(<p[^>]*>.*?ПОЛЕЗНАЯ ИНФОРМАЦИЯ.*?</p>)', content, re.IGNORECASE)
            if p_search:
                end_search = re.search(r'(?=<div class="h-px bg-black/5|<div class="h-px.*|<!-- СЕКЦИЯ: ФОРМА)', content)
                if end_search:
                    start_idx = p_search.start()
                    end_idx = end_search.start()
                    new_block = f'<section id="poleznaya-informatsiya" class="scroll-mt-32 mb-20">\n{new_html}\n</section>\n'
                    content = content[:start_idx] + new_block + content[end_idx:]
                    print(f"[OK] {filename}: Created new section via splice.")
            else:
                print(f"[SKIP] {filename}: No anchor found.")
                continue
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    update_memos()
