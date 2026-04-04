import os
import re

memo_dir = 'pages/memos'

def flatten_sections(content):
    # 1. Identify the main-content block
    main_match = re.search(r'(<div[^>]*id="main-content"[^>]*>)(.*?)(</div>\s*</div>\s*</div>)', content, flags=re.DOTALL)
    if not main_match:
        return content
    
    start_tag = main_match.group(1)
    inner_block = main_match.group(2)
    end_tag = main_match.group(3)
    
    # 2. Extract and sanitize inner content
    # Remove all existing section tags first to start from a clean slate
    flat_content = re.sub(r'<section\s+id="[^"]*"[^>]*>', '', inner_block)
    flat_content = re.sub(r'</section>', '', flat_content)
    
    sections_config = [
        ('pered-otezdom', 'Перед отъездом'),
        ('sobiraya-bagazh', 'Собирая багаж'),
        ('v-rossijskom-aeroportu-vyleta-prileta', 'В российском аэропорту вылета/прилета'),
        ('tamozhennyj-kontrol-v-indonezii', 'Таможенный контроль в Индонезии'),
        ('tamozhennyj-v-egipte', 'Таможенный контроль в Египте'),
        ('registratsiya-na-rejs-i-oformlenie-bagazha', 'Регистрация на рейс и оформление багажа'),
        ('pasportnyj-kontrol', 'Паспортный контроль'),
        ('sanitarnyj-kontrol', 'Санитарный контроль'),
        ('veterinarnyj-kontrol', 'Ветеринарный контроль'),
        ('v-aeroportu-prileta-vyleta-indonezii', 'В аэропорту прилета/вылета Индонезии'),
        ('v-aeroportu-prileta-vyleta-egipta', 'В аэропорту прилета/вылета Египта'),
        ('pasportnyj-kontrol-viza', 'Паспортный контроль. Виза'),
        ('pasportnyj-kontrol-i-bezvizovyj-rezhim', 'Паспортный контроль и безвизовый режим'),
        ('bali', 'Бали'),
        ('kurorty-egipta', 'Курорты Египта'),
        ('pravila-lichnoj-gigieny-i-bezopasnosti', 'Правила личной гигиены и безопасности'),
        ('v-sluchae-poteri-pasporta', 'В случае потери паспорта'),
        ('poleznaya-informatsiya', 'Полезная информация')
    ]
    
    # 3. Find and wrap headers
    # More permissive regex for headers
    header_pattern = r'(<(h[12])\s+class="text-3xl md:text-5xl font-black[^>]*>)([\s\S]*?)(</\2>)'
    
    def repl_header(m):
        header_text = m.group(3).strip()
        match_id = 'section-' + str(m.start())
        for sid, stext in sections_config:
            if stext.lower() in header_text.lower() or header_text.lower() in stext.lower():
                match_id = sid
                break
        return f'\n</section>\n<section id="{match_id}" class="scroll-mt-32 mb-20">\n{m.group(0)}'

    processed_inner = re.sub(header_pattern, repl_header, flat_content)
    
    # Handle the very first content before the first header
    if not processed_inner.strip().startswith('</section>'):
        processed_inner = '<section id="intro" class="scroll-mt-32 mb-20">\n' + processed_inner
    else:
        processed_inner = re.sub(r'^\s*</section>\s*', '', processed_inner)
    
    processed_inner += '\n</section>'
    
    # Final cleanup of double newlines and closing tags
    processed_inner = re.sub(r'</section>\s*</section>', '</section>', processed_inner)
    
    return content[:main_match.start(2)] + processed_inner + content[main_match.end(2):]

for filename in os.listdir(memo_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(memo_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = flatten_sections(content)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
                print(f"Flattened {filename}")

print("All memo structures flattened.")
