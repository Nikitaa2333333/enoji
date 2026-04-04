with open('pages/memos/egypt.html', 'r', encoding='utf-8') as f:
    egypt = f.read()

footer_part = egypt[egypt.find('<!-- Footer -->'):]

with open('pages/memos/tunisia.html', 'r', encoding='utf-8') as f:
    tunisia = f.read()

# Находим где заканчивается форма (или где она должна закончиться)
# В Тунисе форма обрывается или кривая.
# Я найду начало скриптов или модалки и вставлю туда закрывающие теги и футер.

success_modal_idx = tunisia.find('<!-- Success Modal -->')
if success_modal_idx == -1:
    success_modal_idx = tunisia.find('<div id="success-modal"')

if success_modal_idx != -1:
    # Отрезаем всё после контента, но перед модалкой
    # И вставляем: </div> </div> </div> </main> + footer_part
    
    # Но сначала убедимся, что форма там есть и она закрыта.
    # В Тунисе форма начинается на 556.
    
    content_before = tunisia[:success_modal_idx]
    
    # Убеждаемся что </section> есть в конце контента (для формы)
    if '</section>' not in content_before[success_modal_idx-100:]:
         # Если нет, значит форма не закрыта
         pass

    new_tunisia = content_before + "\n    </div>\n    </div>\n    </div>\n  </main>\n\n" + footer_part
    
    with open('pages/memos/tunisia.html', 'w', encoding='utf-8') as f:
        f.write(new_tunisia)
    print("Fixed tunisia.html structure and restored footer.")
else:
    print("Could not find insertion point in tunisia.html")
