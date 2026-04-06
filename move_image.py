
import sys

file_path = r'c:\Users\User\Downloads\tilda dododo\pages\memos\seychelles.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line 712 is the image (index 711)
img_line = lines[711]
if '<img alt="валюта"' in img_line or '<img' in img_line:
    lines.pop(711)
    
    # After pop, the indices shift.
    # Original line 727 was at index 726. 
    # Since 711 < 726, it is now at index 725.
    # To insert AFTER line 727, we use index 726.
    
    img_line = img_line.replace('alt="валюта"', 'alt="население"')
    lines.insert(726, img_line)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Successfully moved image.")
else:
    print("Could not find image at line 712. Current line: " + img_line)
