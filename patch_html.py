import re
import os

def patch_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Deep patching {file_path}...")

    # 1. Fonts and preconnects
    if '<link rel="preconnect"' not in content:
        head_match = re.search(r'<head>', content, re.IGNORECASE)
        if head_match:
            tags = """
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="dns-prefetch" href="https://unpkg.com">
"""
            content = content[:head_match.end()] + tags + content[head_match.end():]

    # 2. Non-blocking Google Fonts
    font_pattern = r'(<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2?[^"]+")>'
    content = re.sub(font_pattern, r'\1 media="print" onload="this.media=\'all\'">', content)

    # 3. Add defer to ALL external scripts
    content = re.sub(r'<script src="([^"]+)"(?!.*?defer)', r'\1" defer', content)

    # 4. Smart image patching
    lcp_image = "tild3762-6537-4136-a532-303036666635__photo.webp"
    
    def img_replacer(match):
        tag = match.group(0)
        # Handle LCP image
        if lcp_image in tag:
            if 'fetchpriority' not in tag:
                tag = tag.replace('<img', '<img fetchpriority="high" loading="eager" decoding="async"')
        else:
            # Handle all other images
            if 'loading="lazy"' not in tag:
                # Add lazy and low priority
                tag = tag.replace('<img', '<img loading="lazy" fetchpriority="low" decoding="async"')
            elif 'decoding="async"' not in tag:
                tag = tag.replace('loading="lazy"', 'loading="lazy" decoding="async"')
        return tag

    content = re.sub(r'<img[^>]+>', img_replacer, content)

    # 5. Fix for Tilda hidden elements
    content = content.replace('style="display:none;"', 'style="display:none;" aria-hidden="true"')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def walk_and_patch(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.html'):
                patch_html_file(os.path.join(root, file))

if __name__ == "__main__":
    if os.path.exists("index.html"):
        patch_html_file("index.html")
    for folder in ["pages", "templates"]:
        if os.path.exists(folder):
            walk_and_patch(folder)
    print("Done! All files have been deeply optimized.")
