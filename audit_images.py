import re
import os

BASE = "c:/Users/User/Downloads/tilda dododo"

COUNTRIES = [
    ("pages/memochina.html",                    "pages/memos/china.html",       "Китай"),
    ("pages/memoegypt.html",                    "pages/memos/egypt.html",       "Египет"),
    ("pages/memoindonesia.html",                "pages/memos/indonesia.html",   "Индонезия"),
    ("pages/memomaldives.html",                 "pages/memos/maldives.html",    "Мальдивы"),
    ("pages/memomauritius.html",               "pages/memos/mauritius.html",   "Маврикий"),
    ("pages/memoseyshelles.html",              "pages/memos/seychelles.html",  "Сейшелы"),
    ("pages/memosrilanka.html",                "pages/memos/sri-lanka.html",   "Шри-Ланка"),
    ("pages/memotanzania.html",                "pages/memos/tanzania.html",    "Танзания"),
    ("pages/memothailand.html",                "pages/memos/thailand.html",    "Таиланд"),
    ("pages/memotunisia.html",                 "pages/memos/tunisia.html",     "Тунис"),
    ("pages/touriststravelingtoturkey.html",   "pages/memos/turkey.html",      "Турция"),
    ("pages/memovietnam.html",                 "pages/memos/vietnam.html",     "Вьетнам"),
]

# Tilda anchor → ключевые слова новой секции (substring match)
ANCHOR_MAP = {
    "BEFORELEAVING":                                        "pered-otezdom",
    "CollectingLuggage":                                    "sobiraya-bagazh",
    "Checkinbaggage":                                       "registratsiya",
    "CHECK-INANDBAGGAGE":                                   "registratsiya",
    "BORDERCONTROLattheairportRussianFederation":           "rossijskom-aeroportu",
    "CUSTOMSCONTROLONDEPARTUREFROMTHERUSSIANFEDERATION":    "tamozhennyj-kontrol",
    "CUSTOMSCONTROLONARRIVALINRUSSIA":                      "tamozhennyj-kontrol",
    "Currency":                                             "valyuta",
    "Customs":                                              "obychai",
    "INCASEOFLOSSOFPASSPORT":                              "poteri-pasporta",
    "THERULESOFPERSONALHYGIENEANDSAFETY":                  "gigieny",
    "Inhotel":                                              "v-otele",
    "Phone":                                                "telefon",
    "Transport":                                            "transport",
    "Excursions":                                           "ekskursii",
    "Language":                                             "yazyk",
    "Climate":                                              "klimat",
    "Holidays":                                             "prazdniki",
    "Purchases":                                            "magaziny",
    "Transferfeatures":                                     "transfer",
    "Mainsvoltage":                                         "napryazhenie",
    "USEFULINFORMATION":                                    "poleznaya",
    "Population":                                           "naselenie",
}
# Country-specific airport anchors (contain "airport" case-insensitive)
AIRPORT_KEYWORD = "airport"


def extract_tilda_mapping(filepath):
    """Возвращает список (anchor, img_filename) из Tilda HTML, без дублей."""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    tokens = re.findall(
        r'name="([A-Z][^"]*?)"|tild[a-f0-9\-]+__([^"\s]+\.jpg)',
        content
    )

    result = []
    seen_imgs = set()
    current_anchor = None
    for anchor, img in tokens:
        if anchor:
            current_anchor = anchor
        elif img and current_anchor:
            # Пропускаем empty-варианты и дубли
            if "-__empty__" in img or img in seen_imgs:
                continue
            seen_imgs.add(img)
            result.append((current_anchor, img))
    return result


SKIP_SECTIONS = {"form", "nav", "menu", "modal", "drawer", "booking", "success", "content", "dark", "overlay"}

def extract_memo_images(filepath):
    """Возвращает список (section_id, alt, img_filename) из нового HTML."""
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()

    results = []
    current_section = "unknown"

    for line in lines:
        # Ищем секцию
        sec = re.search(r'id="([a-z][a-z0-9\-]*)"', line)
        if sec:
            sid = sec.group(1)
            if not any(skip in sid for skip in SKIP_SECTIONS):
                current_section = sid

        # Ищем img — alt может быть до или после src
        if "tild" not in line or "<img" not in line:
            continue
        fname_m = re.search(r'src="[^"]*tild[^"]*__([^"]+\.jpg)"', line)
        alt_m   = re.search(r'alt="([^"]*)"', line)
        if fname_m and alt_m:
            fname = fname_m.group(1)
            alt   = alt_m.group(1)
            if "logo" not in fname.lower() and "svg" not in fname.lower():
                results.append((current_section, alt, fname))

    return results


def find_expected_section(anchor):
    """Возвращает ожидаемый section id (substring) для данного Tilda якоря."""
    # Прямое совпадение
    if anchor in ANCHOR_MAP:
        return ANCHOR_MAP[anchor]
    # Airport-якоря
    if AIRPORT_KEYWORD in anchor.lower():
        return "aeroportu"
    # Passport control (country-specific)
    if "PASSPORTCONTROL" in anchor or "PassportControl" in anchor.lower().replace("-", ""):
        return "pasportnyj-kontrol"
    if "CUSTOMCONTROL" in anchor or "CustomControl" in anchor.lower().replace("-", ""):
        return "tamozhennyj"
    return None


def audit_country(tilda_path, memo_path, name):
    if not os.path.exists(tilda_path):
        return f"\n{'='*50}\n{name}: Tilda-файл не найден\n"
    if not os.path.exists(memo_path):
        return f"\n{'='*50}\n{name}: Memo-файл не найден\n"

    tilda_map = extract_tilda_mapping(tilda_path)   # [(anchor, img), ...]
    memo_imgs = extract_memo_images(memo_path)       # [(section_id, alt, img), ...]

    # Строим словарь: img_filename → expected_section (из Tilda)
    img_to_expected = {}
    for anchor, img in tilda_map:
        expected = find_expected_section(anchor)
        if img not in img_to_expected:
            img_to_expected[img] = (anchor, expected)

    lines = [f"\n{'='*50}", f"  {name}", "="*50]
    problems = []
    ok_count = 0

    for section_id, alt, fname in memo_imgs:
        if fname not in img_to_expected:
            # Картинка не из Tilda-оригинала (добавлена вручную)
            continue

        anchor, expected_section = img_to_expected[fname]

        if expected_section is None:
            problems.append(f"  ⚠️  '{fname}'\n     Секция: {section_id}\n     Из Tilda-якоря '{anchor}' (нет маппинга, возможно лишняя)")
        elif expected_section not in section_id:
            problems.append(
                f"  ❌  '{fname}'\n"
                f"     Стоит в:    {section_id}\n"
                f"     Должна быть в: *{expected_section}* (из Tilda '{anchor}')"
            )
        else:
            ok_count += 1

    if problems:
        lines.append(f"  ✅ Правильных: {ok_count}  |  ❌ Проблемных: {len(problems)}\n")
        lines.extend(problems)
    else:
        lines.append(f"  ✅ Всё верно ({ok_count} картинок)")

    return "\n".join(lines)


print("АУДИТ КАРТИНОК В ПАМЯТКАХ (dry-run)\n")
for tilda_rel, memo_rel, name in COUNTRIES:
    tilda_path = os.path.join(BASE, tilda_rel)
    memo_path  = os.path.join(BASE, memo_rel)
    print(audit_country(tilda_path, memo_path, name))
