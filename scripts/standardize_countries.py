import os
import re

# Пути
BASE_DIR = r"c:\Users\User\Downloads\tilda dododo"
COUNTRIES_DIR = os.path.join(BASE_DIR, "pages", "countries")

# Эталонные настройки из template_memo.html
STANDARD_TAILWIND_CONFIG = """
  <script id="tailwind-config">
    tailwind.config = {
      darkMode: "class",
      theme: {
        extend: {
          colors: {
            "background": "#fffcf5",
            "surface": "#fffcf5",
            "on-surface": "#000000",
            "primary": "#f5e2a1",
            "on-primary": "#000000",
            "on-surface-variant": "#000000",
            "surface-container-low": "#fffcf5",
            "surface-container-high": "#fffaf0",
            "primary-container": "#f5e2a1",
            "on-primary-container": "#000000",
          },
          fontFamily: { "headline": ["Manrope"], "body": ["Manrope"] },
          borderRadius: { "DEFAULT": "1rem", "lg": "2rem", "xl": "3rem", "3xl": "3rem", "full": "9999px" },
        },
      },
    }
  </script>
"""

STANDARD_STYLES = """
  <style>
    body {
      font-family: 'Manrope', sans-serif;
      opacity: 1 !important;
    }
    a { text-decoration: none !important; }
    html {
      scroll-behavior: smooth;
      scroll-padding-top: 110px;
    }
    p { line-height: 1.8; }
    .material-symbols-outlined {
      font-variation-settings: 'FILL' 0, 'wght' 300, 'GRAD' 0, 'opsz' 24;
      vertical-align: middle;
    }
    /* Навигация (Quick Links) - Оставляем как есть в шаблоне */
    #quick-links {
      max-height: calc(100vh - 220px);
      overflow-y: auto;
      scrollbar-width: none;
      -ms-overflow-style: none;
    }
    #quick-links::-webkit-scrollbar { display: none; }
    .nav-link {
      display: block;
      padding: 0.5rem 1.5rem;
      border-left: 2px solid transparent;
      font-size: 0.85rem;
      font-weight: 600;
      line-height: 1.4;
      color: #000000;
      transition: all 0.2s ease;
    }
    .nav-link:hover { color: #000; background: rgba(0, 0, 0, 0.02); }
    .nav-link.active {
      color: #000;
      font-weight: 800;
      border-left-color: #f5e2a1;
      background: rgba(245, 226, 161, 0.2);
    }
    .check-list {
      list-style-type: none !important;
      padding-left: 0 !important;
      margin: 1.5rem 0 !important;
    }
    .check-list li {
      position: relative;
      padding-left: 2.2rem;
      margin-bottom: 1rem;
      line-height: 1.6;
    }
    .check-list li::before {
      content: 'check_circle';
      font-family: 'Material Symbols Outlined';
      position: absolute;
      left: 0;
      top: 0.1rem;
      color: #f5e2a1;
      font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
      font-size: 1.4rem;
    }
  </style>
"""

def standardize_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Сначала чистим голову от старых стилей и конфига
    html = re.sub(r'<script id="tailwind-config">.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style>.*?</style>', '', html, flags=re.DOTALL)
    
    # Вставляем новые
    html = html.replace('</head>', STANDARD_TAILWIND_CONFIG + STANDARD_STYLES + '\n</head>')

    # 2. Чистим мусорные теги (битые </a>)
    html = html.replace('</a>         <strong>', ' <strong>')
    html = html.replace('</a>                 <img', ' <img')
    html = html.replace('</a>                 <imgsrc', ' <img src')
    
    # 3. Принудительные скругления для картинок
    html = re.sub(r'rounded-\[[^\]]+\]', 'rounded-3xl', html)
    
    # 4. Унификация начертаний и цветов текста (Font Weights & Colors)
    # Убираем font-medium, так как в памятке используется стандартный вес
    html = html.replace('font-medium', '')
    # Унифицируем цвет текста (с серого варианта на 80% черный как в памятке)
    html = html.replace('text-on-surface-variant', 'text-black/80')
    
    # 5. Убираем "двойные линии" (лишние разделители перед формой)
    html = html.replace('<div class="h-px bg-black/5 my-16"></div>', '')
    
    # 6. ЧИСТКА МУСОРА (Technical Junk)
    # Удаляем "(ТЕКСТ И ФОТО):" и подобные технические строки
    html = html.replace('(ТЕКСТ И ФОТО):', '')
    html = html.replace('(ТЕКСТ И ФОТО)', '')
    # Удаляем пустые заголовки, которые могли остаться после чистки
    html = re.sub(r'<h[1-6][^>]*>\s*</h[1-6]>', '', html)
    
    # 7. АГРЕССИВНЫЙ РЕМЕЙК ЗАГОЛОВКОВ (H1, H2)
    # Любой H1 станет нужного стиля
    html = re.sub(r'<h1[^>]*>(.*?)</h1>', r'<h1 class="text-6xl md:text-8xl font-black tracking-tighter leading-none mb-10">\1</h1>', html, flags=re.DOTALL)
    # Любой H2 станет нужного стиля
    html = re.sub(r'<h2[^>]*>(.*?)</h2>', r'<h2 class="text-3xl md:text-5xl font-black mb-10 tracking-tight text-black">\1</h2>', html, flags=re.DOTALL)

    # 8. Поля формы — только круглые
    html = html.replace('rounded-xl', 'rounded-full')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return os.path.basename(file_path)

if __name__ == "__main__":
    print(f"Began standardizing files in: {COUNTRIES_DIR}")
    if not os.path.exists(COUNTRIES_DIR):
        print(f"Error: Directory not found: {COUNTRIES_DIR}")
    else:
        for filename in os.listdir(COUNTRIES_DIR):
            if filename.endswith(".html"):
                try:
                    standardize_file(os.path.join(COUNTRIES_DIR, filename))
                    print(f" [OK] {filename}")
                except Exception as e:
                    print(f" [ERR] {filename}: {e}")
    print("Done!")
