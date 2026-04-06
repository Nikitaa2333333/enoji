import os
import re

def surgical_fix():
    directory = 'pages/memos/'
    
    if not os.path.exists(directory):
        print(f"Directory {directory} not found.")
        return

    # Fix specific branding locations back to English
    restorations = [
        # Fix copyright
        (r'© 2026\s+туроператора', '© 2026 Emoji Tours'),
        # Fix slogan
        (r'туроператора\s+—\s+Путешествия\s+с\s+душой', 'Emoji Tours — Путешествия с душой'),
        # Fix Title tag
        (r'—\s+туроператора(?=</title>)', '— Emoji Tours'),
        # Fix Alt attributes
        (r'alt="туроператора"', 'alt="Emoji Tours"'),
        # Fix mobile footer specifically (with dot)
        (r'© 2026\s+туроператора\.', '© 2026 Emoji Tours.')
    ]

    total_files = 0
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            path = os.path.join(directory, filename)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            new_content = content
            changed = False
            for pattern, replacement in restorations:
                if re.search(pattern, new_content):
                    new_content = re.sub(pattern, replacement, new_content)
                    changed = True

            if changed:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                total_files += 1
    
    print(f"Restored branding in {total_files} files. Footer and Title are fixed!")

if __name__ == "__main__":
    surgical_fix()
