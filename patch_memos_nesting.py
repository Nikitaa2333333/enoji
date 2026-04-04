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

FORM_TEMPLATE = """
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
              name="destination" value="{{COUNTRY}}" type="text" /> </div>
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

def patch_file(filepath):
    filename_stem = os.path.splitext(os.path.basename(filepath))[0].lower()
    country = COUNTRY_MAP.get(filename_stem, "Направление")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Сначала удаляем все старые вхождения формы (и ее комментариев)
    # Удаляем блок от разделителя или комментария до конца секции формы
    content = re.sub(r'<div class="h-px bg-black/5 my-16"></div>\s*<!-- СЕКЦИЯ: ФОРМА -->[\s\S]*?</section>', '', content)
    content = re.sub(r'<!-- СЕКЦИЯ: ФОРМА -->[\s\S]*?</section>', '', content)
    content = re.sub(r'<section id="section-form"[\s\S]*?</section>', '', content)
    
    # 2. Ищем тег </main>
    main_end_match = re.search(r'</main>', content)
    if not main_end_match:
        print(f"[SKIP] {filepath}: No </main> tag found")
        return

    # 3. Идем назад от </main> и ищем закрывающие </div>
    # Нам нужно найти теги div непосредственно перед </main>
    # Обычно это: </div> (flex-1) \n </div> (flex/max-3xl) \n </main>
    # Мы хотим вставить форму ПЕРЕД предпоследним </div>
    
    divs_match = list(re.finditer(r'</div>', content[:main_end_match.start()]))
    if len(divs_match) < 2:
        print(f"[WARN] {filepath}: Fewer than 2 </div> tags before </main>")
        return
    
    # Индекс предпоследнего </div>
    target_idx = divs_match[-2].start()
    
    # 4. Вставляем форму
    form_html = FORM_TEMPLATE.replace('{{COUNTRY}}', country)
    new_content = content[:target_idx] + form_html + "\n" + content[target_idx:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"[OK] Patched {filepath} (inside content div)")

for filename in os.listdir(memo_dir):
    if filename.endswith('.html'):
        patch_file(os.path.join(memo_dir, filename))

print("\nAll tasks completed.")
