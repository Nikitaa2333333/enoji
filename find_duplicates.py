import os
import re
from collections import Counter

def find_duplicates(directory):
    duplicate_report = {}
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            path = os.path.join(directory, filename)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Find all img src attributes
                images = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
                # Count occurrences
                counts = Counter(images)
                duplicates = {src: count for src, count in counts.items() if count > 1 and "logo.png" not in src}
                if duplicates:
                    duplicate_report[filename] = duplicates
    return duplicate_report

report = find_duplicates(r'c:\Users\User\Downloads\tilda dododo\pages\memos')
for file, dups in report.items():
    print(f"File: {file}")
    for src, count in dups.items():
        print(f"  - {src}: {count} times")
