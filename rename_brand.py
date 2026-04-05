import os

def rename_brand():
    # Define replacements
    replacements = [
        ('ТУРОПЕРАТОРА', 'EMOJI TOURS'),
        ('Туроператора', 'Emoji Tours'),
        ('туроператора', 'emoji tours'),
        ('Эмоджи турс', 'Emoji Tours'),
        ('ЭМОДЖИ ТУРС', 'EMOJI TOURS'),
        ('эмоджи турс', 'emoji tours'),
    ]


    exclude_dirs = {'.git', '.venv', '__pycache__', 'tmp'} # Exclude tmp to be safe if it's large
    target_extensions = {'.html', '.txt'}

    count = 0
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if any(file.endswith(ext) for ext in target_extensions):
                if file == 'rename_brand.py':
                    continue
                
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = content
                    for old_text, new_text in replacements:
                        new_content = new_content.replace(old_text, new_text)
                    
                    if new_content != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Updated: {filepath}")
                        count += 1
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

    print(f"\nTotal files updated: {count}")

if __name__ == "__main__":
    rename_brand()
