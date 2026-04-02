import pdfplumber
import os

files = {
    "Maldives": r'c:\Users\User\Downloads\tilda dododo\Памятка туриста  Мальдивы.pdf',
    "Egypt": r'c:\Users\User\Downloads\tilda dododo\Памятка туриста  Египет.pdf'
}

def analyze_file(name, path):
    print(f"\n--- АНАЛИЗ {name.upper()} ---")
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return

    with pdfplumber.open(path) as pdf:
        for p_idx, page in enumerate(pdf.pages):
            h = page.height
            words = page.extract_words(extra_attrs=['fontname', 'size'])
            
            # Ищем фразу "Чтобы позвонить"
            for w in words:
                if "Чтобы" in w['text'] or "позвонить" in w['text']:
                    t_bot = w['bottom']
                    t_x0, t_x1 = w['x0'], w['x1']
                    
                    # Ищем любые графические объекты под текстом в радиусе 8 пикселей
                    # (как работал старый детектор)
                    found_objs = []
                    search_range = [t_bot - 2, t_bot + 8]
                    
                    for obj in (page.lines + page.rects + page.curves):
                        y0 = h - obj.get('y1', 0) if 'y1' in obj else obj.get('top', 0)
                        if search_range[0] <= y0 <= search_range[1]:
                            o_x0, o_x1 = obj.get('x0', 0), obj.get('x1', 0)
                            overlap = min(t_x1, o_x1) - max(t_x0, o_x0)
                            if overlap > 0:
                                found_objs.append(f"Type: {obj.get('type','?')}, Top: {y0:.2f}, Height: {obj.get('height',0):.2f}")
                    
                    if found_objs:
                        print(f"Found phrase '{w['text']}' on page {p_idx+1} at Y={t_bot:.2f}")
                        for o in set(found_objs): # Уникальные объекты
                            print(f"  [!] ПОД ТЕКСТОМ НАЙДЕНО: {o}")
                    else:
                        # Если ничего не нашли
                        pass

for name, path in files.items():
    analyze_file(name, path)
