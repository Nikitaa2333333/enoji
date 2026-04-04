import os
import re

# Маппинг файлов на названия стран
country_map = {
    "china.html": "Китай",
    "cuba.html": "Куба",
    "dominikana.html": "Доминикана",
    "egypt.html": "Египет",
    "egypt_new.html": "Египет",
    "india.html": "Индия",
    "indonesia.html": "Индонезия",
    "israel.html": "Израиль",
    "maldives.html": "Мальдивы",
    "mauritius.html": "Маврикий",
    "memo.html": "Турция",
    "mexico.html": "Мексика",
    "oae.html": "ОАЭ",
    "ofcyprus.html": "Кипр",
    "seychelles.html": "Сейшелы",
    "seyshelles.html": "Сейшелы",
    "sri-lanka.html": "Шри-Ланка",
    "srilanka.html": "Шри-Ланка",
    "tanzania.html": "Танзания",
    "thailand.html": "Таиланд",
    "touriststravelingtoturkey.html": "Турция",
    "tunisia.html": "Тунис",
    "turkey.html": "Турция",
    "vietnam.html": "Вьетнам"
}

NEW_FORM_TEMPLATE = """    <section id="section-form" class="scroll-mt-32 py-12 max-w-4xl">
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
              name="destination" value="{COUNTRY}" type="text" /> </div>
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
    </section>"""

def update_file(filepath, country_name):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_form = NEW_FORM_TEMPLATE.replace("{COUNTRY}", country_name)
    
    # 1. Сначала пробуем найти <section id="section-form">...</section>
    pattern_section = re.compile(r'<section[^>]*id="section-form"[^>]*>.*?</section>', re.DOTALL)
    if pattern_section.search(content):
        new_content = pattern_section.sub(new_form, content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath} via ID section")
        return

    # 2. Если не нашли, ищем по комментарию и следующей за ним форме
    # Заменяя всё от комментария до конца тега </form>
    pattern_comment_form = re.compile(r'<!-- СЕКЦИЯ: ФОРМА -->.*?<form.*?</form>', re.DOTALL)
    if pattern_comment_form.search(content):
        new_content = pattern_comment_form.sub("<!-- СЕКЦИЯ: ФОРМА -->\n" + new_form, content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath} via comment+form")
        return

    print(f"Form NOT FOUND in {filepath}")

memos_dir = "pages/memos"
for filename in os.listdir(memos_dir):
    if filename in country_map:
        filepath = os.path.join(memos_dir, filename)
        update_file(filepath, country_map[filename])

print("All done!")
