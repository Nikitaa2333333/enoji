import os

filepath = r"pages\memos\vietnam.html"

new_section = r"""<section id="poleznaya-informatsiya" class="scroll-mt-32 mb-24">
  <div class="bg-black/5 rounded-[2.5rem] md:rounded-[4rem] p-8 md:p-16 border border-black/5">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-8 mb-16">
      <div>
        <p class="text-primary font-bold tracking-widest uppercase text-sm mb-3">Контакты</p>
        <h2 class="text-4xl md:text-6xl font-black tracking-tighter leading-none text-black">Полезная информация</h2>
      </div>
      <div class="hidden md:block">
        <span class="material-symbols-outlined text-6xl text-black/10">account_balance</span>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div class="bg-white rounded-[2rem] p-8 shadow-sm border border-black/5 hover:shadow-md transition-shadow">
        <div class="flex items-center gap-4 mb-6">
          <div class="w-12 h-12 bg-primary/20 rounded-full flex items-center justify-center">
            <span class="material-symbols-outlined text-black">flag</span>
          </div>
          <h3 class="text-xl font-black text-black">Посольство РФ в г. Ханой</h3>
        </div>
        <div class="space-y-4 text-black/70 font-medium">
          <p class="flex gap-3"><span class="material-symbols-outlined text-sm mt-1">location_on</span> г. Ханой, ул. Латхань, 191</p>
          <p class="flex gap-3"><span class="material-symbols-outlined text-sm mt-1">call</span> +84-4-3833-69-91/92 (из РФ)<br>(04) 3833-69-91/92 (по Вьетнаму)</p>
          <p class="flex gap-3"><span class="material-symbols-outlined text-sm mt-1">fax</span> +84-4-3833-69-95</p>
          <p class="flex gap-3"><span class="material-symbols-outlined text-sm mt-1">mail</span> rusemb.vietnam@gmail.com</p>
          <p class="text-sm pt-2 italic">Посол: Ковтун Андрей Григорьевич</p>
        </div>
      </div>

      <div class="bg-white rounded-[2rem] p-8 shadow-sm border border-black/5 hover:shadow-md transition-shadow">
        <div class="flex items-center gap-4 mb-6">
          <div class="w-12 h-12 bg-black/5 rounded-full flex items-center justify-center">
            <span class="material-symbols-outlined text-black">apartment</span>
          </div>
          <h3 class="text-xl font-black text-black">Генконсульство в г. Дананге</h3>
        </div>
        <div class="space-y-4 text-black/70 font-medium">
          <p class="flex gap-3"><span class="material-symbols-outlined text-sm mt-1">location_on</span> Чанфу, 22</p>
          <p class="flex gap-3"><span class="material-symbols-outlined text-sm mt-1">call</span> +84-511-382-23-80 (из РФ)<br>(0511) 382-23-80 (по Вьетнаму)</p>
          <p class="flex gap-3"><span class="material-symbols-outlined text-sm mt-1">language</span> www.rusconsdanang.mid.ru</p>
          <p class="flex gap-3"><span class="material-symbols-outlined text-sm mt-1">mail</span> consdanang@gmail.com</p>
          <p class="text-sm pt-2 italic">Генконсул: Дикушин Валентин Михайлович</p>
        </div>
      </div>

      <div class="bg-white rounded-[2rem] p-8 shadow-sm border border-black/5 hover:shadow-md transition-shadow md:col-span-2">
        <div class="flex items-center gap-4 mb-6">
          <div class="w-12 h-12 bg-primary/20 rounded-full flex items-center justify-center">
            <span class="material-symbols-outlined text-black">contact_support</span>
          </div>
          <h3 class="text-xl font-black text-black">Консульский отдел посольства</h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-black/70 font-medium">
          <div class="space-y-4">
            <p class="flex gap-3"><span class="material-symbols-outlined text-sm mt-1">location_on</span> г. Ханой, ул. Латхань, 191</p>
            <p class="flex gap-3"><span class="material-symbols-outlined text-sm mt-1">call</span> +84-4-3833-69-96 (из РФ)<br>(04) 3833-69-96 (по Вьетнаму)</p>
          </div>
          <div class="space-y-4">
            <p class="flex gap-3"><span class="material-symbols-outlined text-sm mt-1">mail</span> moscow-vietnam@yandex.ru<br>kons_hanoi@inbox.ru</p>
            <p class="text-sm pt-2 italic">Заведующий: Бабахин Сергей Викторович</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>"""

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Линии 584-602 (1-индексация) -> 583-602 в Python (0-индексация)
# Но мы видим в просмотре, что 602 это </div>
# Заменяем блок от 584 до 602 включительно.
start = 583
end = 602

new_lines = lines[:start] + [new_section + '\n'] + lines[end+1:]

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Vietnam Embassy Section properly updated via script.")
