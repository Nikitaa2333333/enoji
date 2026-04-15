import os
import re

mapping = {
    "china": "Memo_China.pdf",
    "egypt": "Memo_Egypt.pdf",
    "indonesia": "Memo_Indonesia.pdf",
    "maldives": "Memo_Maldives.pdf",
    "mauritius": "Memo_Mauritius.pdf",
    "seychelles": "Memo_Seychelles.pdf",
    "sri-lanka": "Memo_SriLanka.pdf",
    "tanzania": "Memo_Tanzania.pdf",
    "thailand": "Memo_Thailand.pdf",
    "tunisia": "Memo_Tunisia.pdf",
    "turkey": "Memo_Turkey.pdf",
    "vietnam": "Memo_Vietnam.pdf"
}

memos_dir = r"pages\memos"

for filename in os.listdir(memos_dir):
    if not filename.endswith(".html"):
        continue
    
    country_key = filename.replace(".html", "")
    if country_key not in mapping:
        continue
    
    target_pdf = mapping[country_key]
    filepath = os.path.join(memos_dir, filename)
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace broken links like "../../dist_pdf/egypt.pdf" with "../../dist_pdf/Memo_Egypt.pdf"
    # Note: re.escape might be needed if country_key has special chars, but here they are simple.
    pattern = r'href="\.\./\.\./dist_pdf/' + re.escape(country_key) + r'\.pdf"'
    replacement = r'href="../../dist_pdf/' + target_pdf + r'"'
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Patched links in {filename}")
    else:
        print(f"No changes needed in {filename}")
