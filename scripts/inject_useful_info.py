#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Вставляет блок "Полезная информация" (посольства, горячие линии)
в HTML-памятки. Без разговорника.

Для файлов с существующим блоком — заменяет содержимое.
Для файлов без блока — вставляет перед section#section-form и добавляет nav-ссылку.
"""

import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMOS = os.path.join(BASE, "pages", "memos")

# Данные по каждой стране: список блоков
# Тип блока: 'embassy' или 'hotline'
COUNTRY_DATA = {

    "egypt.html": [
        {"type": "embassy", "title": "Посольство Арабской Республики Египет в РФ", "lines": [
            "Адрес: г. Москва, Кропоткинский пер., 12.",
            "Тел.: (499) 246-02-34, 246-30-96.",
            "Факс: (499) 246-30-80.",
        ]},
        {"type": "embassy", "title": "Посольство России в Арабской Республике Египет", "lines": [
            "Адрес: Giza st. 95, Dokki, Cairo, Egypt.",
            "Тел.: (8-10-2-023) 748-93-53, 748-93-54, 748-93-55.",
            "Факс: (8-10-2-023) 760-90-74.",
            "E-mail: ruemeg@tedata.net.eg, rus.egypt@mail.ru",
            "Сайт: www.egypt.mid.ru",
        ]},
    ],

    "indonesia.html": [
        {"type": "embassy", "title": "Посольство РФ в Индонезии", "lines": [
            "Адрес: 12940, Jakarta, H.R. Rasuna Said, Kav. Х-7, 1-2.",
            "Тел.: (62-21) 522-29-12/14.",
            "Факс: (62-21) 522-29-16.",
            "E-mail: rusemb.indonesia@mid.ru",
        ]},
        {"type": "embassy", "title": "Почётный консул на Бали (г-н Нуку Камка)", "lines": [
            "Адрес: Perumahan Bali Kencana Resort II, Block Merpati No. 10, Ungasan 80364, Bali, Indonesia.",
            "Тел.: (+62) 851 0079 1560.",
            "Факс: (+62361) 279-1561.",
            "E-mail: bali@russiaconsul.com",
        ]},
        {"type": "embassy", "title": "Посольство Республики Индонезия в РФ", "lines": [
            "Адрес: г. Москва, Новокузнецкая ул., 12.",
            "Тел.: +7 (495) 951-95-49/50.",
            "Факс: +7 (495) 735-44-31.",
            "E-mail: moscow.kbri@kemlu.go.id",
        ]},
    ],

    "china.html": [
        {"type": "embassy", "title": "Посольство КНР в Москве", "lines": [
            "Консульский отдел: 007-499-951-8435 (пн–пт, 15:30–18:00).",
            "Факс: 007-499-951-84-36.",
            "E-mail: chinaemb_ru@mfa.gov.cn",
        ]},
        {"type": "embassy", "title": "Посольство РФ в Пекине", "lines": [
            "Адрес: 100600, Beijing, Dongzhimennei Beizhong str. 4.",
            "Тел.: +86 (10) 6532-1381, 6532-2051.",
            "Факс: +86 (10) 6532-4851.",
            "E-mail: embassybeijing@mid.ru",
        ]},
        {"type": "embassy", "title": "Генеральное консульство России в Шанхае", "lines": [
            "Адрес: Shanghai, Hongkou District.",
            "Тел.: +86 (21) 632-42-682, 632-48-383.",
            "Факс: +86 (21) 630-69-982.",
            "E-mail: shanghai@mid.ru",
        ]},
        {"type": "embassy", "title": "Генеральное консульство России в Гонконге", "lines": [
            "Адрес: 2106, 21/Fl., Sun Hung Kai Centre, 30 Harbour Road, Wanchai, Hong Kong.",
            "Тел.: (852) 287-771-88.",
            "Факс: (852) 287-771-66.",
            "E-mail: cghongkong@mid.ru",
        ]},
    ],

    "mauritius.html": [
        {"type": "embassy", "title": "Посольство России на Маврикии", "lines": [
            "Адрес: P.O. Box 10, Queen Mary Avenue, Floreal.",
            "Тел.: (230) 696-1545, (230) 696-5533.",
            "Экстренный тел. (консульский отдел): (230) 5729-4036.",
            "E-mail: rusemb.mu@intnet.mu",
        ]},
        {"type": "embassy", "title": "Посольство Маврикия в Москве", "lines": [
            "Адрес: 109240, г. Москва, ул. Николямская, 8.",
            "Тел.: +7 (495) 915-76-17.",
        ]},
    ],

    "maldives.html": [
        {"type": "embassy", "title": "Посольство России на Мальдивах (при посольстве в Коломбо)", "lines": [
            "Адрес: 62 Sir Ernest de Silva Mawatha, Colombo 7, Sri Lanka.",
            "Тел.: (9411) 257-35-55, 257-49-59.",
            "Консульский отдел: (9411) 269-70-42.",
            "E-mail: rusemb@itmin.net",
        ]},
        {"type": "embassy", "title": "Посольство Мальдив в Москве", "lines": [
            "Адрес: г. Москва, ул. Щепкина, 24.",
            "Тел.: +7 (095) 688-16-20, 688-14-63, 688-16-51.",
            "Режим работы: пн–пт, 9:00–17:00.",
            "E-mail: moscow@srilankaembassy.org",
        ]},
    ],

    "seychelles.html": [
        {"type": "embassy", "title": "Посольство РФ на Сейшелах", "lines": [
            "Адрес: о. Маэ, р-н Ле Ниоль, P.O. Box 632, Le Niole, Mahé, Seychelles.",
            "Тел.: +248 426-65-90, 426-61-22.",
            "Факс: +248 426-66-53.",
            "Сайт: www.seychelles.mid.ru",
            "E-mail: rusemb.seychelles@mid.ru",
        ]},
        {"type": "embassy", "title": "Посольство Сейшел в РФ", "lines": [
            "Адрес: 199016, г. Санкт-Петербург, Детская ул., 30.",
            "Тел.: (812) 322-3811, 322-3816, 322-3807.",
            "E-mail: headoffice@seychelles-consular.sp.ru",
        ]},
    ],

    "thailand.html": [
        {"type": "hotline", "label": "Горячая линия принимающей компании", "value": "+90 850 549 07 07"},
    ],

    "tanzania.html": [
        {"type": "embassy", "title": "Посольство РФ в Танзании", "lines": [
            "Адрес: P.O. Box 1905, Dar es Salaam, Ali Hassan Mwinyi Road, Plot 3&5.",
            "Тел.: +255-22-2666006/05.",
            "Экстренный тел.: +255-76-7919756.",
            "Факс: +255-22-2666818.",
            "E-mail: embrusstanz@mid.ru",
        ]},
        {"type": "embassy", "title": "Посольство Танзании в РФ", "lines": [
            "Адрес: г. Москва, ул. Большая Никитская, 51.",
            "Тел.: +7 (495) 690-25-21, 690-25-17.",
            "Факс: +7 (495) 690-22-51.",
            "E-mail: info@tanzania.ru",
            "Сайт: www.tanzania.ru",
        ]},
    ],

    "tunisia.html": [
        {"type": "embassy", "title": "Посольство России в Тунисе", "lines": [
            "Адрес: 16, Rue des Bergamottes, B.P. 48, El Manar 1, Tunis 2092, Tunisie.",
            "Тел./факс: +216 71 882 757.",
            "Экстренные вопросы: +216 28 400 094.",
            "Факс: +216 71 886 453.",
            "E-mail: tunconsul@mail.ru",
            "Приём по консульским вопросам: вт, ср, пт — с 9:00 до 11:00.",
        ]},
        {"type": "embassy", "title": "Посольство Туниса в Москве", "lines": [
            "Адрес: 121069, г. Москва, ул. Малая Никитская, д. 28/1.",
            "Тел.: +7 (495) 691-28-58, +7 (495) 691-28-69.",
            "Факс: +7 (495) 691-75-88.",
            "E-mail: ambatunis@mail.ru",
            "Режим работы: пн–пт, 09:00–16:30 (перерыв 13:00–14:00).",
        ]},
        {"type": "hotline", "label": "Горячая линия принимающей компании", "value": "+90 850 549 07 07"},
    ],

    "turkey.html": [
        {"type": "hotline", "label": "Служба поддержки туристов", "value": "+90 242 324 00 95 (круглосуточно)"},
        {"type": "hotline", "label": "Горячая линия в Анталии для иностранных туристов", "value": "179 (бесплатно, рус./англ./нем.)"},
        {"type": "hotline", "label": "Страховая сервисная служба", "value": "+90 242 310 28 44"},
        {"type": "embassy", "title": "Посольство Турции в Москве", "lines": [
            "Адрес: 119121, г. Москва, 7-й Ростовский пер., 12.",
            "Тел.: +7 (495) 956-55-95.",
            "Факс: +7 (495) 956-55-97.",
            "E-mail: turemb@dol.ru",
        ]},
        {"type": "embassy", "title": "Посольство России в Анкаре", "lines": [
            "Адрес: Karyagdi Sok. 5, Ayranci, Ankara, Turkey.",
            "Тел.: +90 (312) 440-94-85.",
            "Факс: +90 (312) 440-14-85.",
            "E-mail: rus-ankara@yandex.ru",
            "Сайт: www.turkey.mid.ru",
        ]},
        {"type": "embassy", "title": "Генеральное консульство России в Анталии", "lines": [
            "Адрес: Park sok, 30, Jenikapi, Antalya, Turkey.",
            "Тел.: +90 (242) 248-32-02.",
            "Факс: +90 (242) 248-44-68.",
            "E-mail: rfconsulate@ttmail.com",
            "Сайт: www.antalya.mid.ru",
        ]},
        {"type": "embassy", "title": "Генеральное консульство России в Стамбуле", "lines": [
            "Адрес: Istiklal Caddesi 443, Beyoglu, Istanbul, Turkey.",
            "Тел.: +90 (212) 292-51-01/02/03.",
            "Факс: +90 (212) 293-23-58.",
            "E-mail: visavi@turk.net",
            "Сайт: www.istanbul.turkey.mid.ru",
        ]},
        {"type": "embassy", "title": "Генеральное консульство России в Трабзоне", "lines": [
            "Адрес: Ortahisar mahalesi, Refik Cesur sok. 6, Trabzon.",
            "Тел.: +90 (462) 326-26-00.",
            "Факс: +90 (462) 326-26-01.",
            "E-mail: rusconsultrb@rftrabzon.com",
            "Сайт: www.rftrabzon.com",
        ]},
        {"type": "embassy", "title": "Почётное консульство России в Измире", "lines": [
            "Адрес: Fatih Caddesi No. 69, Camdibi, Izmir.",
            "Тел.: +90 (232) 461-51-86/87.",
            "Факс: +90 (232) 461-51-88.",
        ]},
    ],

    "touriststravelingtoturkey.html": [
        {"type": "hotline", "label": "Служба поддержки туристов", "value": "+90 242 324 00 95 (круглосуточно)"},
        {"type": "hotline", "label": "Горячая линия в Анталии для иностранных туристов", "value": "179 (бесплатно, рус./англ./нем.)"},
        {"type": "hotline", "label": "Страховая сервисная служба", "value": "+90 242 310 28 44"},
        {"type": "embassy", "title": "Посольство Турции в Москве", "lines": [
            "Адрес: 119121, г. Москва, 7-й Ростовский пер., 12.",
            "Тел.: +7 (495) 956-55-95.",
            "Факс: +7 (495) 956-55-97.",
            "E-mail: turemb@dol.ru",
        ]},
        {"type": "embassy", "title": "Посольство России в Анкаре", "lines": [
            "Адрес: Karyagdi Sok. 5, Ayranci, Ankara, Turkey.",
            "Тел.: +90 (312) 440-94-85.",
            "Факс: +90 (312) 440-14-85.",
            "E-mail: rus-ankara@yandex.ru",
            "Сайт: www.turkey.mid.ru",
        ]},
        {"type": "embassy", "title": "Генеральное консульство России в Анталии", "lines": [
            "Адрес: Park sok, 30, Jenikapi, Antalya, Turkey.",
            "Тел.: +90 (242) 248-32-02.",
            "Факс: +90 (242) 248-44-68.",
            "E-mail: rfconsulate@ttmail.com",
            "Сайт: www.antalya.mid.ru",
        ]},
        {"type": "embassy", "title": "Генеральное консульство России в Стамбуле", "lines": [
            "Адрес: Istiklal Caddesi 443, Beyoglu, Istanbul, Turkey.",
            "Тел.: +90 (212) 292-51-01/02/03.",
            "Факс: +90 (212) 293-23-58.",
            "E-mail: visavi@turk.net",
            "Сайт: www.istanbul.turkey.mid.ru",
        ]},
        {"type": "embassy", "title": "Генеральное консульство России в Трабзоне", "lines": [
            "Адрес: Ortahisar mahalesi, Refik Cesur sok. 6, Trabzon.",
            "Тел.: +90 (462) 326-26-00.",
            "Факс: +90 (462) 326-26-01.",
            "E-mail: rusconsultrb@rftrabzon.com",
            "Сайт: www.rftrabzon.com",
        ]},
        {"type": "embassy", "title": "Почётное консульство России в Измире", "lines": [
            "Адрес: Fatih Caddesi No. 69, Camdibi, Izmir.",
            "Тел.: +90 (232) 461-51-86/87.",
            "Факс: +90 (232) 461-51-88.",
        ]},
    ],

    "sri-lanka.html": [
        {"type": "embassy", "title": "Посольство России в Коломбо", "lines": [
            "Адрес: 62, Sir Ernest de Silva Mawatha, Colombo 7, Sri Lanka.",
            "Тел.: +94 (11) 257-35-55, 257-49-59.",
            "Факс: +94 (11) 257-49-57.",
            "Экстренный мобильный: +94 (77) 665-44-15.",
            "Режим работы: пн 08:00–14:30, 16:00–19:00; вт–пт 08:00–14:30.",
            "E-mail: rusemb@itmin.net",
            "Сайт: www.sri-lanka.mid.ru",
            "Горячая линия: +94775547327, +94779199806, +94769042664.",
        ]},
        {"type": "embassy", "title": "Посольство Демократической Социалистической Республики Шри-Ланка в РФ", "lines": [
            "Адрес: 129090, г. Москва, ул. Щепкина, 24.",
            "Тел.: +7 (495) 688-16-20, 688-16-51, 688-14-63.",
            "Факс: +7 (495) 688-17-57.",
            "E-mail: moscow@srilankaembassy.org",
            "Сайт: www.srilankaembassy.org",
        ]},
        {"type": "hotline", "label": "Горячая линия принимающей компании", "value": "+90 850 549 07 07"},
    ],

    "vietnam.html": [
        {"type": "embassy", "title": "Посольство РФ в Ханое", "lines": [
            "Адрес: г. Ханой, ул. Латхань, 191.",
            "Тел.: +84-4-3833-69-91/92 (из России), 04-3833-69-91/92 (по Вьетнаму).",
            "Факс: +84-4-3833-69-95.",
            "E-mail: moscow-vietnam@yandex.ru, rusemb.vietnam@gmail.com",
        ]},
        {"type": "embassy", "title": "Генеральное консульство России в Дананге", "lines": [
            "Адрес: г. Дананг, ул. Чанфу, 22.",
            "Тел.: +84-511-382-23-80/381-85-28 (из России), 0511-382-23-80/381-85-28 (по Вьетнаму).",
            "Факс: +84-511-381-85-27.",
            "E-mail: consdanang@gmail.com",
            "Сайт: www.rusconsdanang.mid.ru",
        ]},
        {"type": "embassy", "title": "Консульский отдел посольства (Ханой)", "lines": [
            "Адрес: г. Ханой, ул. Латхань, 191.",
            "Тел.: 04-3833-69-96 (по Вьетнаму).",
            "Факс: +84-4-3833-69-96.",
            "E-mail: kons_hanoi@inbox.ru, kons_hanoi@hn.vnn.vn",
        ]},
    ],
}

# Файлы, где секция имеет нестандартный id
CUSTOM_SECTION_IDS = {
    "touriststravelingtoturkey.html": "USEFULINFORMATION",
}

NAV_LINK_NEEDED = {"tunisia.html"}


def build_section_html(blocks, section_id="poleznaya-informatsiya"):
    """Генерирует HTML-код секции 'Полезная информация'."""
    embassy_blocks_html = []

    for block in blocks:
        if block["type"] == "embassy":
            lines_html = "<br>\n              ".join(block["lines"])
            embassy_blocks_html.append(f"""        <div>
          <h3 class="text-2xl font-black mb-4 text-black">{block['title']}</h3>
          <p class="text-lg text-black/80 leading-relaxed">
              {lines_html}
          </p>
        </div>""")
        elif block["type"] == "hotline":
            embassy_blocks_html.append(f"""        <div class="bg-primary/20 rounded-2xl p-6">
          <p class="text-xl font-bold text-black">
            {block['label']}: <span class="font-black">{block['value']}</span>
          </p>
        </div>""")

    inner = "\n".join(embassy_blocks_html)
    return f"""      <section class="scroll-mt-32 mb-20" id="{section_id}">
        <h2 class="text-3xl md:text-5xl font-black mb-10 tracking-tight text-black">
          Полезная информация
        </h2>
        <div class="space-y-10 my-10">
{inner}
        </div>
      </section>"""


def replace_section_by_id(content, section_id, new_section_html):
    """
    Заменяет <section ... id="section_id">...</section> в строке content.
    Учитывает вложенные теги.
    """
    pattern = re.compile(
        r'(<section\b[^>]*\bid=["\']' + re.escape(section_id) + r'["\'][^>]*>)',
        re.IGNORECASE
    )
    match = pattern.search(content)
    if not match:
        return None, content  # not found

    start = match.start()
    tag_start = match.end()

    # Считаем вложенность тегов чтобы найти закрывающий </section>
    depth = 1
    pos = tag_start
    open_tag = re.compile(r'<section\b', re.IGNORECASE)
    close_tag = re.compile(r'</section\s*>', re.IGNORECASE)

    while depth > 0 and pos < len(content):
        next_open = open_tag.search(content, pos)
        next_close = close_tag.search(content, pos)

        if next_close is None:
            break

        if next_open and next_open.start() < next_close.start():
            depth += 1
            pos = next_open.end()
        else:
            depth -= 1
            pos = next_close.end()

    end = pos
    return (start, end), content[:start] + new_section_html + content[end:]


def insert_before_section_form(content, new_section_html):
    """Вставляет секцию перед <section ... id="section-form">."""
    patterns = [
        r'(<section\b[^>]*\bid=["\']section-form["\'])',
        r'(<!--\s*СЕКЦИЯ:\s*ФОРМА\s*-->)',
    ]
    for pat in patterns:
        m = re.search(pat, content, re.IGNORECASE)
        if m:
            insert_pos = m.start()
            return content[:insert_pos] + new_section_html + "\n      \n      " + content[insert_pos:]
    return None


def add_nav_link(content):
    """Добавляет nav-ссылку на #poleznaya-informatsiya перед закрывающим тегом </nav> в #quick-links."""
    # Ищем последнюю nav-link перед </nav> в блоке quick-links
    nav_block_match = re.search(r'id=["\']quick-links["\'].*?</nav>', content, re.DOTALL)
    if not nav_block_match:
        return content

    nav_block = nav_block_match.group(0)
    # Проверяем, что ссылки ещё нет
    if 'poleznaya-informatsiya' in nav_block:
        return content

    new_link = '\n       <a class="nav-link" href="#poleznaya-informatsiya">\n        Полезная информация\n       </a>'
    new_nav_block = nav_block.replace('</nav>', new_link + '\n      </nav>', 1)
    return content[:nav_block_match.start()] + new_nav_block + content[nav_block_match.end():]


def process_file(filename, blocks):
    filepath = os.path.join(MEMOS, filename)
    if not os.path.exists(filepath):
        print(f"  ⚠ Файл не найден: {filepath}")
        return

    # Некоторые файлы могут иметь смешанную кодировку — читаем с заменой
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        print(f"  ⚠ Файл прочитан с заменой невалидных байт (смешанная кодировка)")

    section_id = CUSTOM_SECTION_IDS.get(filename, "poleznaya-informatsiya")
    new_html = build_section_html(blocks, section_id)

    result, new_content = replace_section_by_id(content, section_id, new_html)

    if result:
        print(f"  ✔ Заменена секция #{section_id}")
    else:
        # Нет секции — вставляем
        inserted = insert_before_section_form(content, new_html)
        if inserted is None:
            print(f"  ✘ Не удалось найти точку вставки в {filename}")
            return
        new_content = inserted
        print(f"  ✔ Вставлена новая секция #{section_id}")

    # Добавляем nav-ссылку если нужно
    if filename in NAV_LINK_NEEDED:
        new_content = add_nav_link(new_content)
        print(f"  ✔ Добавлена nav-ссылка")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"  ✔ Сохранено: {filename}")


def main():
    print(f"Базовая директория: {BASE}")
    print(f"Папка с памятками: {MEMOS}\n")

    for filename, blocks in COUNTRY_DATA.items():
        print(f"▶ {filename}")
        process_file(filename, blocks)
        print()

    print("Готово!")


if __name__ == "__main__":
    main()
