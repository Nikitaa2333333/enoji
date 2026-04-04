import os
import re

# Папка с памятками
directory = r'c:\Users\User\Downloads\tilda dododo\pages\memos'
files = [f for f in os.listdir(directory) if f.endswith('.html')]

# Шаблон нижней части (форма, футер, скрипты + закрывающие теги контейнеров)
bottom_template_raw = \"\"\"        </div>
      </div>
    </main>

    <div class="h-px bg-black/5 my-16"></div>

    <!-- СЕКЦИЯ: ФОРМА -->
    <section id="section-form" class="scroll-mt-32 py-12 max-w-4xl mx-auto">
      <h2 class="text-3xl md:text-4xl font-black mb-8 tracking-tight">Отправить заявку</h2>
      <form id="booking-form"
        class="bg-[#fffcf5] border border-black/5 rounded-[2rem] md:rounded-[3rem] p-6 sm:p-10 md:p-16 shadow-2xl shadow-[#5f531a]/10 space-y-10 md:space-y-12 relative overflow-hidden">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-6 md:gap-y-8 mt-2">
          <div class="space-y-2">
            <label class="block text-sm font-bold text-on-surface-variant ml-1">Имя и Фамилия</label>
            <input class="w-full bg-transparent border border-black/15 rounded-full p-4 hover:border-black/30 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all" name="userName" placeholder="Иван Иванов" type="text" required />
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-bold text-on-surface-variant ml-1">E-mail</label>
            <input class="w-full bg-transparent border border-black/15 rounded-full p-4 hover:border-black/30 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all" name="userEmail" placeholder="hello@example.com" type="email" required />
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-bold text-on-surface-variant ml-1">Телефон</label>
            <input class="w-full bg-transparent border border-black/15 rounded-full p-4 hover:border-black/30 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all" name="userPhone" placeholder="+7 (___) ___-__-__" type="tel" required />
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-bold text-on-surface-variant ml-1">Направление</label>
            <input class="w-full bg-transparent border border-black/15 rounded-full p-4 hover:border-black/30 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all" name="destination" value="{COUNTRY}" type="text" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-2">
              <label class="block text-sm font-bold text-on-surface-variant ml-1">Взрослых</label>
              <input class="w-full bg-transparent border border-black/15 rounded-full p-4 hover:border-black/30 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all" name="adults" min="1" type="number" value="2" />
            </div>
            <div class="space-y-2">
              <label class="block text-sm font-bold text-on-surface-variant ml-1">Детей (и возраст)</label>
              <input class="w-full bg-transparent border border-black/15 rounded-full p-4 hover:border-black/30 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all" name="children" placeholder="1 реб, 5 лет" type="text" />
            </div>
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-bold text-on-surface-variant ml-1">Бюджет (RUB)</label>
            <input class="w-full bg-transparent border border-black/15 rounded-full p-4 hover:border-black/30 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all" name="budget" placeholder="От 200 000" type="text" />
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-bold text-on-surface-variant ml-1">Количество ночей</label>
            <input class="w-full bg-transparent border border-black/15 rounded-full p-4 hover:border-black/30 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all" name="nights" min="1" type="number" value="7" />
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-bold text-on-surface-variant ml-1">Дата начала</label>
            <input class="w-full bg-transparent border border-black/15 rounded-full p-4 hover:border-black/30 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all" name="startDate" type="date" />
          </div>
        </div>
        <div class="space-y-4">
          <label class="block text-sm font-bold text-on-surface-variant ml-1">Нужны ли экскурсии?</label>
          <div class="flex flex-wrap gap-8">
            <label class="flex items-center gap-3 cursor-pointer group">
              <input class="w-5 h-5 text-primary border-black/20 rounded-full transition-colors cursor-pointer" name="excursions" type="radio" value="Да" />
              <span class="text-on-surface group-hover:text-primary transition-colors">Да, обязательно</span>
            </label>
            <label class="flex items-center gap-3 cursor-pointer group">
              <input class="w-5 h-5 text-primary border-black/20 rounded-full transition-colors cursor-pointer" name="excursions" type="radio" value="Нет" />
              <span class="text-on-surface group-hover:text-primary transition-colors">Нет, только отдых</span>
            </label>
            <label class="flex items-center gap-3 cursor-pointer group">
              <input class="w-5 h-5 text-primary border-black/20 rounded-full transition-colors cursor-pointer" name="excursions" type="radio" value="Пока не знаю" />
              <span class="text-on-surface group-hover:text-primary transition-colors">Пока не знаю</span>
            </label>
          </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
          <div class="space-y-2">
            <label class="block text-sm font-bold text-on-surface-variant ml-1">Предпочтения по отелю</label>
            <textarea class="w-full bg-transparent border border-black/15 rounded-full p-4 hover:border-black/30 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all" name="hotelPrefs" placeholder="Напр. первая линия, только 5*, наличие детского клуба..." rows="3"></textarea>
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-bold text-on-surface-variant ml-1">Аэропорт вылета</label>
            <input class="w-full bg-transparent border border-black/15 rounded-xl p-4 hover:border-black/30 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all" name="airport" placeholder="Шереметьево, Пулково..." type="text" />
          </div>
        </div>
        <div class="pt-8 flex justify-center w-full">
          <button class="w-full sm:w-auto bg-black text-white px-10 md:px-14 py-5 rounded-full text-lg md:text-xl font-bold shadow-xl shadow-black/15 hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center" type="submit">Отправить заявку</button>
        </div>
      </form>
    </section>

    <!-- Footer -->
    <footer class="bg-surface-container-low w-full border-t border-black/5 pt-16 pb-10 px-4 md:px-8 mt-8">
      <div class="max-w-7xl mx-auto flex flex-col gap-12 md:gap-16">
        <div class="flex flex-col md:flex-row justify-between items-start gap-12">
          <div class="space-y-6 max-w-sm text-center md:text-left mx-auto md:mx-0">
            <img src="../../images/logo.png" alt="Emoji Tours" class="h-12 md:h-14 mx-auto md:mx-0">
            <p class="text-on-surface-variant font-medium text-sm leading-relaxed px-4 md:px-0">
              Мы верим, что путешествия — это лучший способ познать себя и окружающий мир.
            </p>
            <div class="flex gap-4 justify-center md:justify-start">
              <a href="https://max.ru/join/0haRr-rt5CMasX93mYrj_DuaLtUNy7gLfKyjXIdKFys" target="_blank"
                class="w-10 h-10 bg-white rounded-full flex items-center justify-center hover:scale-110 shadow-sm transition-transform group">
                <img src="../../images/Логотип_MAX.svg" alt="MAX"
                  class="w-5 h-5 object-contain grayscale group-hover:grayscale-0 transition-all">
              </a>
              <a href="https://vk.com/emoji_tours" target="_blank"
                class="w-10 h-10 bg-white rounded-full flex items-center justify-center hover:scale-110 shadow-sm transition-transform group">
                <img src="../../images/VK_Compact_Logo_(2021-present).svg.png" alt="VK"
                  class="w-5 h-5 object-contain grayscale group-hover:grayscale-0 transition-all">
              </a>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-10 md:gap-16 w-full md:w-auto text-center md:text-left">
            <div class="space-y-4">
              <h4 class="font-bold text-on-surface-variant text-sm">Связаться с нами</h4>
              <div class="space-y-3 text-lg">
                <a href="tel:+79636491852"
                  class="block font-black text-on-surface hover:text-primary transition-colors">+7 963-649-18-52</a>
                <a href="mailto:trohin.zh@yandex.ru"
                  class="block text-on-surface-variant hover:text-black transition-colors text-sm font-medium">trohin.zh@yandex.ru</a>
              </div>
            </div>
          </div>
        </div>
        <div class="pt-8 md:pt-10 border-t border-black/5 flex flex-col md:flex-row justify-between items-center gap-6">
          <div class="text-on-surface-variant font-medium text-[11px] md:text-xs text-center md:text-left w-full md:w-auto">© 2026 Emoji Tours. Путешествия с душой.</div>
          <div class="flex flex-wrap justify-center md:justify-end gap-6 text-sm font-bold text-on-surface-variant">
            <a href="../../index.html#countries" class="hover:text-black transition-colors">Страны</a>
            <a href="../../index.html#calendar" class="hover:text-black transition-colors">Календарь</a>
            <a href="../../index.html#testimonials" class="hover:text-black transition-colors">Отзывы</a>
            <a href="../../index.html#journey" class="hover:text-black transition-colors">Начать путешествие</a>
          </div>
        </div>
      </div>
    </footer>

    <!-- Success Modal -->
    <div id="success-modal"
      class="fixed inset-0 z-[200] flex items-center justify-center opacity-0 pointer-events-none transition-opacity duration-500">
      <div class="absolute inset-0 bg-black/30 backdrop-blur-sm"></div>
      <div
        class="bg-white p-8 md:p-12 rounded-[3rem] shadow-2xl relative z-10 max-w-sm w-full text-center space-y-6 transform scale-90 transition-transform duration-500"
        id="success-card">
        <div class="w-24 h-24 bg-primary rounded-full flex items-center justify-center mx-auto mb-4">
          <span class="material-symbols-outlined text-5xl">check</span>
        </div>
        <h3 class="text-3xl font-black tracking-tight">Заявка принята!</h3>
        <p class="text-on-surface-variant font-medium leading-relaxed">
          Мы уже получили ваши данные и начали подбор идеального тура. Наш эксперт свяжется с вами в ближайшее время!
        </p>
        <button onclick="closeModal()"
          class="w-full bg-black text-white py-5 rounded-full text-xl font-bold hover:scale-105 active:scale-95 transition-all shadow-xl shadow-black/10 mt-4">
          Супер!
        </button>
      </div>
    </div>

    <script src="https://unpkg.com/imask"></script>
    <script>
      // ScrollSpy
      const sections = document.querySelectorAll('section[id]');
      const navLinks = document.querySelectorAll('.nav-link');
      const quickLinksContainer = document.getElementById('quick-links');

      let isScrolling = false;

      window.addEventListener('scroll', () => {
        if (isScrolling) return;

        let current = "";
        const scrollPos = window.pageYOffset + 160;

        sections.forEach(section => {
          const sectionTop = section.offsetTop;
          if (scrollPos >= sectionTop) {
            current = section.getAttribute('id');
          }
        });

        if (current) {
          navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === "#" + current) {
              link.classList.add('active');

              // АВТО-СКРОЛЛ БОКОВОГО МЕНЮ
              if (link.scrollIntoView) {
                link.scrollIntoView({
                  behavior: 'smooth',
                  block: 'nearest',
                  inline: 'start'
                });
              }
            }
          });
        }
      });

      // Плавный скролл при клике
      document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
          e.preventDefault();
          const targetId = this.getAttribute('href');
          const target = document.querySelector(targetId);

          if (target) {
            isScrolling = true;
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');

            window.scrollTo({
              top: target.offsetTop - 120,
              behavior: 'smooth'
            });

            setTimeout(() => { isScrolling = false; }, 800);
          }
        });
      });

      // Form logic
      document.addEventListener('DOMContentLoaded', () => {
        // Mobile menu population
        const mobileQuickLinks = document.getElementById('mobile-quick-links');
        const desktopLinksSource = document.querySelectorAll('#quick-links .nav-link');

        if (mobileQuickLinks && desktopLinksSource.length > 0) {
          mobileQuickLinks.innerHTML = '';
          desktopLinksSource.forEach(link => {
            const mobileLink = link.cloneNode(true);
            mobileLink.className = 'text-[22px] font-black py-2 hover:text-primary transition-colors';
            mobileLink.onclick = () => {
              toggleMenu();
            };
            mobileQuickLinks.appendChild(mobileLink);
          });
        }

        const phoneInput = document.querySelector('input[name="userPhone"]');
        if (phoneInput) IMask(phoneInput, { mask: '+7 (000) 000-00-00' });

        const form = document.getElementById('booking-form');
        const modal = document.getElementById('success-modal');
        const card = document.getElementById('success-card');

        if (form) {
          form.addEventListener('submit', function (e) {
            e.preventDefault();
            const btn = form.querySelector('button[type="submit"]');
            const originalText = btn.innerHTML;
            btn.disabled = true;
            btn.innerHTML = '<span class="material-symbols-outlined animate-spin mr-3">progress_activity</span>Отправляем...';

            const formData = new FormData(form);
            const params = new URLSearchParams();
            for (const [key, value] of formData.entries()) params.append(key, value);

            const GOOGLE_URL = 'https://script.google.com/macros/s/AKfycbwi0-K7Jqf86nWEyit6OB7DgiBlHEjhQF7SvlDcl0BUEnTl8WGMjrM5nGx5wSUoAk-7/exec';

            fetch(GOOGLE_URL, {
              method: 'POST',
              mode: 'no-cors',
              headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
              body: params.toString()
            })
              .then(() => {
                modal.classList.add('opacity-100', 'pointer-events-auto');
                card.style.transform = 'scale(1)';
                form.reset();
              })
              .finally(() => {
                btn.disabled = false;
                btn.innerHTML = originalText;
              });
          });
        }
      });

      function toggleMenu() {
        const drw = document.getElementById('mobile-drawer');
        const ovl = document.getElementById('drawer-overlay');
        if (!drw || !ovl) return;
        drw.classList.toggle('translate-x-full');
        ovl.classList.toggle('opacity-0');
        ovl.classList.toggle('pointer-events-none');
        document.body.style.overflow = drw.classList.contains('translate-x-full') ? '' : 'hidden';
      }

      function closeModal() {
        const modal = document.getElementById('success-modal');
        const card = document.getElementById('success-card');
        modal.classList.remove('opacity-100', 'pointer-events-auto');
        card.style.transform = 'scale(0.9)';
      }
    </script>
  </body>
</html>
\"\"\"

def standardize_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Получаем название страны (из Title или H1)
    match = re.search(r'<title>Памятка:\s*([^<]+)</title>', content)
    if not match:
        match = re.search(r'Памятка:\s*([^<]+)', content)
    country = match.group(1).strip() if match else "Неизвестно"
    # Исправляем частые опечатки в названии (для destination поля)
    if country == "Тайланд": country = "Таиланд"

    # 2. Исправляем цвет метки Направление
    content = re.sub(r'text-primary font-bold tracking-widest uppercase text-xs mb-2">Направление', 
                     r'text-black/40 font-bold tracking-widest uppercase text-xs mb-2">Направление', content)

    # 3. Исправляем ширину основного контента
    content = re.sub(r'id="main-content" class="space-y-16"', 
                     r'id="main-content" class="space-y-16 max-w-4xl mx-auto"', content)
    content = re.sub(r'class="space-y-16" id="main-content"', 
                     r'id="main-content" class="space-y-16 max-w-4xl mx-auto"', content)
    
    # 4. Находим точку разреза (разделитель или начало формы)
    # Ищем разделитель или начало секции формы
    divider_regex = r'<div class="h-px bg-black/5 my-16"></div>|<!-- СЕКЦИЯ: ФОРМА -->'
    match_div = re.search(divider_regex, content)
    
    if match_div:
        split_pos = match_div.start()
        top_part = content[:split_pos].rstrip()
        
        # Находим ПОСЛЕДНЮЮ открытую секцию в контенте, чтобы убедиться, что она закрыта?
        # На самом деле, файлы обычно заканчиваются на </section> </div> </div> </main>
        
        # Чтобы не гадать, мы просто откатываемся до последнего </section>
        last_section_end = top_part.rfind('</section>')
        if last_section_end != -1:
            clean_top = top_part[:last_section_end + 10] # + length of </section>
            
            # Наш шаблон добавит закрывающие дивы для main-content, max-w-7xl и main
            final_content = clean_top + "\\n\\n" + bottom_template_raw.replace("{COUNTRY}", country)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(final_content)
            print(f"Готово: {os.path.basename(filepath)} ({country})")
        else:
            print(f"ОШИБКА {os.path.basename(filepath)}: Не найден </section>")
    else:
        print(f"ПРОПУЩЕНО {os.path.basename(filepath)}: Не найден разделитель формы")

for filename in files:
    standardize_file(os.path.join(directory, filename))
