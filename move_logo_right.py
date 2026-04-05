import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update container class: change md:justify-center to md:justify-end
    orig_container = 'justify-between md:justify-center items-center'
    new_container = 'justify-between md:justify-end items-center'
    
    # 2. Update logo link class: remove mx-auto and md:mx-0
    # regex to handle potential whitespace variations
    orig_logo_link = re.compile(r'class="flex-shrink-0\s+mx-auto\s+md:mx-0"')
    new_logo_link = 'class="flex-shrink-0"'

    new_content = content.replace(orig_container, new_container)
    new_content = orig_logo_link.sub(new_logo_link, new_content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

# Directories to process
dirs = ['pages/countries', 'pages/memos', 'labs', 'templates']
updated_count = 0

for d in dirs:
    if os.path.exists(d):
        for root, _, files in os.walk(d):
            for file in files:
                if file.endswith('.html'):
                    if process_file(os.path.join(root, file)):
                        updated_count += 1

print(f"Successfully updated {updated_count} files.")
