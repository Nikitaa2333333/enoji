import os
import re

def replace_with_operator():
    directory = 'pages/memos/'
    
    if not os.path.exists(directory):
        print(f"Directory {directory} not found.")
        return

    # Replacements focusing on declensions and removing redundant "company"
    replacements = [
        # Match "компании Emoji Tours" -> "туроператора"
        (r'(?i)компании\s+Emoji\s+Tours', 'туроператора'),
        (r'(?i)компанией\s+Emoji\s+Tours', 'туроператором'),
        
        # Match declensions
        (r'(?i)Emoji\s+Toursми', 'туроператорами'),
        (r'(?i)Emoji\s+Toursом', 'туроператором'),
        (r'(?i)Emoji\s+Toursа', 'туроператора'),
        (r'(?i)Emoji\s+Toursу', 'туроператору'),
        (r'(?i)Emoji\s+Toursе', 'туроператоре'),
        
        # Base replacement (most common in memos text)
        (r'(?i)Emoji\s+Tours', 'туроператора')
    ]

    total_files = 0
    total_replacements = 0

    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            file_path = os.path.join(directory, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            new_content = content
            file_changes = 0
            
            for pattern, replacement in replacements:
                matches = len(re.findall(pattern, new_content))
                if matches > 0:
                    new_content = re.sub(pattern, replacement, new_content)
                    file_changes += matches

            if file_changes > 0:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {filename}: {file_changes} replacements.")
                total_replacements += file_changes
                total_files += 1

    print(f"\nDone! Replaced brand with 'туроператора' {total_replacements} times in {total_files} files.")

if __name__ == "__main__":
    replace_with_operator()
