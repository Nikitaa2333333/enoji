import os
import asyncio
from playwright.async_api import async_playwright

ALLOWED_COUNTRIES = [
    'egypt', 'maldives', 'turkey', 'vietnam', 'china', 
    'mauritius', 'thailand', 'seychelles', 'indonesia', 
    'sri-lanka', 'tanzania', 'tunisia'
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMOS_DIR = os.path.join(BASE_DIR, 'pages', 'memos')
OUTPUT_DIR = os.path.join(BASE_DIR, 'dist_pdf')

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

async def generate_pdf(browser, html_file):
    page = await browser.new_page()
    file_path = os.path.join(MEMOS_DIR, html_file)
    normalized_path = file_path.replace(os.sep, '/')
    file_url = f"file:///{normalized_path}"
    
    print(f"--- Начинаю: {html_file} ---")
    try:
        # ИСПОЛЬЗУЕМ wait_until='load', чтобы не ждать бесконечно все картинки/скрипты
        # Это решит проблему с таймаутом на тяжелых страницах (Египет)
        await page.goto(file_url, wait_until="load", timeout=60000)
        
        # Даем 2 секунды на рендеринг шрифтов и базовых стилей
        await asyncio.sleep(2)
        
        output_filename = html_file.replace('.html', '.pdf')
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        await page.pdf(path=output_path, format="A4", print_background=True, 
                       margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
                       display_header_footer=False, scale=0.9)
        print(f"Готово: {output_filename}")
    except Exception as e:
        print(f"Ошибка при работе с {html_file}: {e}")
    finally:
        await page.close()

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        memos = [f for f in os.listdir(MEMOS_DIR) if f.endswith('.html')]
        target_memos = [f for f in memos if f.replace('.html', '') in ALLOWED_COUNTRIES]
        
        print(f"Найдено памяток для обработки (FINAL): {len(target_memos)}")
        for memo in target_memos:
            await generate_pdf(browser, memo)
        await browser.close()
        print("\\nВсе PDF успешно сгенерированы!")

if __name__ == "__main__":
    asyncio.run(main())
