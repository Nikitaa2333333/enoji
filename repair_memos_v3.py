import os
import re

memo_dir = 'pages/memos'

COUNTRY_MAP = {
    'cuba': 'Куба',
    'dominikana': 'Доминикана',
    'egypt': 'Египет',
    'egypt_new': 'Египет',
    'india': 'Индия',
    'indonesia': 'Индонезия',
    'israel': 'Израиль',
    'maldives': 'Мальдивы',
    'mauritius': 'Маврикий',
    'mexico': 'Мексика',
    'oae': 'ОАЭ',
    'ofcyprus': 'Кипр',
    'seychelles': 'Сейшелы',
    'seyshelles': 'Сейшелы',
    'sri-lanka': 'Шри-Ланка',
    'srilanka': 'Шри-Ланка',
    'tanzania': 'Танзания',
    'thailand': 'Таиланд',
    'touriststravelingtoturkey': 'Турция',
    'tunisia': 'Тунис',
    'turkey': 'Турция',
    'vietnam': 'Вьетнам'
}

def get_form_html(country):
    return f"""
    <div class="h-px bg-black/5 my-16"></div>

    <!-- СЕКЦИЯ: ФОРМА -->
    <section id="section-form" class="scroll-mt-32 py-12 max-w-4xl">
      <h2 class="text-3xl md:text-5xl font-black mb-10 tracking-tight text-black">Отправить заявку</h2>
      <form id="booking-form"
        class="bg-[#fffcf5] border border-black/5 rounded-3xl md:rounded-3xl p-6 sm:p-10 md:p-16 shadow-2xl shadow-[#5f531a]/10 space-y-10 md:space-y-12 relative overflow-hidden">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-6 md:gap-y-8 mt-2">
          <div class="space-y-2"> <label class="block text-sm font-bold text-black/80 ml-1">Имя и Фамилия</label> <input
              class="w-full bg-transparent border border-black/15 rounded-full p-4 hover:border-black/30 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all"
              name="userName" placeholder="Иван Иванов" type="text" required /> </div>
          <div class="space-y-2"> <label class="block text-sm font-bold text-black/80 ml-1">E-mail</label> <input
              class="w-full bg-transparent border border-black/15 rounded-full p-4 hover:border-black/30 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all"
              name="userEmail" placeholder="hello@example.com" type="email" required /> </div>
          <div class="space-y-2"> <label class="block text-sm font-bold text-black/80 ml-1">Телефон</label> <input
              class="w-full bg-transparent border border-black/15 rounded-full p-4 hover:border-black/30 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all"
              name="userPhone" placeholder="+7 (___) ___-__-__" type="tel" required /> </div>
          <div class="space-y-2"> <label class="block text-sm font-bold text-black/80 ml-1">Направление</label> <input
              class="w-full bg-transparent border border-black/15 rounded-full p-4 hover:border-black/30 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all"
              name="destination" value="{country}" type="text" /> </div>
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-2"> <label class="block text-sm font-bold text-black/80 ml-1">Взрослых</label> <input
                class="w-full bg-transparent border border-black/15 rounded-full p-4 hover:border-black/30 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all"
                name="adults" min="1" type="number" value="2" /> </div>
            <div class="space-y-2"> <label class="block text-sm font-bold text-black/80 ml-1">Детей (и возраст)</label>
              <input
                class="w-full bg-transparent border border-black/15 rounded-full p-4 hover:border-black/30 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all"
                name="children" placeholder="1 реб, 5 лет" type="text" /> </div>
          </div>
          <div class="space-y-2"> <label class="block text-sm font-bold text-black/80 ml-1">Бюджет (RUB)</label> <input
              class="w-full bg-transparent border border-black/15 rounded-full p-4 hover:border-black/30 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all"
              name="budget" placeholder="От 200 000" type="text" /> </div>
          <div class="space-y-2"> <label class="block text-sm font-bold text-black/80 ml-1">Количество ночей</label>
            <input
              class="w-full bg-transparent border border-black/15 rounded-full p-4 hover:border-black/30 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all"
              name="nights" min="1" type="number" value="7" /> </div>
          <div class="space-y-2"> <label class="block text-sm font-bold text-black/80 ml-1">Дата начала</label> <input
              class="w-full bg-transparent border border-black/15 rounded-full p-4 hover:border-black/30 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all"
              name="startDate" type="date" /> </div>
        </div>
        <div class="space-y-4"> <label class="block text-sm font-bold text-black/80 ml-1">Нужны ли экскурсии?</label>
          <div class="flex flex-wrap gap-8"> <label class="flex items-center gap-3 cursor-pointer group"> <input
                class="w-5 h-5 text-primary border-black/20 rounded-full transition-colors cursor-pointer"
                name="excursions" type="radio" value="Да" /> <span
                class="text-on-surface group-hover:text-primary transition-colors">Да, обязательно</span> </label> <label
              class="flex items-center gap-3 cursor-pointer group"> <input
                class="w-5 h-5 text-primary border-black/20 rounded-full transition-colors cursor-pointer"
                name="excursions" type="radio" value="Нет" /> <span
                class="text-on-surface group-hover:text-primary transition-colors">Нет, только отдых</span> </label>
            <label class="flex items-center gap-3 cursor-pointer group"> <input
                class="w-5 h-5 text-primary border-black/20 rounded-full transition-colors cursor-pointer"
                name="excursions" type="radio" value="Пока не знаю" /> <span
                class="text-on-surface group-hover:text-primary transition-colors">Пока не знаю</span> </label> </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
          <div class="space-y-2"> <label class="block text-sm font-bold text-black/80 ml-1">Предпочтения по отелю</label>
            <textarea
              class="w-full bg-transparent border border-black/15 rounded-full p-4 hover:border-black/30 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all"
              name="hotelPrefs" placeholder="Напр. первая линия, только 5*, наличие детского клуба..."
              rows="3"></textarea> </div>
          <div class="space-y-2"> <label class="block text-sm font-bold text-black/80 ml-1">Аэропорт вылета</label>
            <input
              class="w-full bg-transparent border border-black/15 rounded-full p-4 hover:border-black/30 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all"
              name="airport" placeholder="Шереметьево, Пулково..." type="text" /> </div>
        </div>
        <div class="pt-8 flex justify-center w-full"> <button
            class="w-full sm:w-auto bg-black text-white px-10 md:px-14 py-5 rounded-full text-lg md:text-xl font-bold shadow-xl shadow-black/15 hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center"
            type="submit">Отправить заявку</button> </div>
      </form>
    </section>
"""

def repair_file(filepath):
    filename_stem = os.path.splitext(os.path.basename(filepath))[0].lower()
    country = COUNTRY_MAP.get(filename_stem, "Направление")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Находим начало футера
    footer_idx = content.find('<!-- Footer -->')
    if footer_idx == -1:
        footer_idx = content.find('<footer')
    
    if footer_idx == -1:
        print(f"[SKIP] {filepath}: No footer found")
        return
    
    footer_part = content[footer_idx:]
    
    # 2. Ищем начало основного блока контента
    main_content_start = content.find('<div class="flex-1 py-10">')
    if main_content_start == -1:
        print(f"[SKIP] {filepath}: No content start found")
        return
    
    # Мы хотим сохранить верхнюю часть файла до начала секций
    # Но проще найти конец ПОСЛЕДНЕЙ полезной секции
    
    # Ищем последнюю секцию перед формой
    # Полезная информация или В случае потери паспорта
    target_sections = ['poleznaya-informatsiya', 'v-sluchae-poteri-pasporta', 'pravila-lichnoj-gigieny-i-bezopasnosti', 'bali']
    
    found_end = -1
    for sid in target_sections:
        s_match = re.search(f'<section id="{sid}"', content)
        if s_match:
            # Ищем закрывающий тег этой секции
            s_end = content.find('</section>', s_match.end())
            if s_end != -1:
                found_end = s_end + 10 # </section>
                # Но если после него есть </div> (от space-y-12 например), надо его тоже забрать
                # Или просто отрезать всё лишнее
    
    if found_end == -1:
        # Пытаемся найти последний </section> который не форма
        all_sections = list(re.finditer(r'</section>', content))
        for s in reversed(all_sections):
            if 'section-form' not in content[s.start()-200:s.start()]:
                found_end = s.end()
                break
    
    if found_end == -1:
        print(f"[SKIP] {filepath}: No section end found")
        return

    content_top = content[:found_end]
    # Очищаем конец контента от мусорных дивов
    content_top = re.sub(r'</section>[\s\S]*$', '</section>', content_top)
    
    # Собираем файл заново
    new_html = content_top + "\n"
    new_html += "        </div> <!-- closes main-content -->\n" # Закрываем id="main-content"
    new_html += "      </div> <!-- closes flex-1 -->\n" # Закрываем flex-1
    new_html += "    </div> <!-- closes flex container inside main -->\n" # Закрываем max-w-7xl
    new_html += get_form_html(country) + "\n"
    new_html += "  </main>\n"
    new_html += footer_part
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"[DONE] {filepath}")

for filename in os.listdir(memo_dir):
    if filename.endswith('.html'):
        repair_file(os.path.join(memo_dir, filename))
