import os
import re
from bs4 import BeautifulSoup

tilda_dir = r"c:\Users\User\Downloads\tilda dododo\tilda_raw\emojitours.ru"
mapping = {}

for filename in os.listdir(tilda_dir):
    if filename.startswith("page") and filename.endswith(".html"):
        filepath = os.path.join(tilda_dir, filename)
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            soup = BeautifulSoup(content, "html.parser")
            title = soup.title.string if soup.title else ""
            h1 = soup.find("h1")
            h1_text = h1.get_text() if h1 else ""
            
            # Look for country names in title or h1
            mapping[filename] = {"title": title, "h1": h1_text}

for k, v in mapping.items():
    print(f"{k}: {v['title']} | {v['h1']}")
