#!/usr/bin/env python3
"""
Replace Tailwind CDN + blocking fonts with compiled CSS + async fonts
in all HTML pages (except index.html which was already updated).
"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NEW_RESOURCES = (
    '\n  <!-- Compiled Tailwind CSS (replaces ~350KB CDN runtime) -->\n'
    '  <link rel="stylesheet" href="/css/tailwind.min.css">\n'
    '  <!-- Fonts: combined single request, non-blocking async load -->\n'
    '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" media="print" onload="this.media=\'all\'">\n'
    '  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"></noscript>'
)

REMOVALS = [
    re.compile(r'\s*<script\s+src="https://cdn\.tailwindcss\.com[^"]*"[^>]*>\s*</script>', re.DOTALL | re.IGNORECASE),
    re.compile(r'\s*<script\s+id="tailwind-config"[^>]*>.*?</script>', re.DOTALL | re.IGNORECASE),
    re.compile(r'\s*<link\s+href="https://fonts\.googleapis\.com/css2\?family=Manrope[^"]*"\s*\n?\s*rel="stylesheet"\s*/>', re.IGNORECASE),
    re.compile(r'\s*<link\s+href="https://fonts\.googleapis\.com/css2\?family=Manrope[^"]*"\s*\n?\s*rel="stylesheet"\s*>', re.IGNORECASE),
    re.compile(r'\s*<link\s+href="https://fonts\.googleapis\.com/css2\?family=Manrope[^"]*"[^>]*>', re.IGNORECASE),
    re.compile(r'\s*<link\s+href="https://fonts\.googleapis\.com/css2\?family=Material\+Symbols[^"]*"[^>]*>', re.IGNORECASE),
    # Guard: remove already-injected block on re-run
    re.compile(r'\s*<!-- Compiled Tailwind CSS.*?</noscript>', re.DOTALL),
]

def patch_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    original = html
    for pattern in REMOVALS:
        html = pattern.sub('', html)
    html = re.sub(r'(</title>)', r'\1' + NEW_RESOURCES, html, count=1)
    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  Patched: {os.path.relpath(path, ROOT)}')
    else:
        print(f'  Skipped: {os.path.relpath(path, ROOT)}')

skip = {os.path.join(ROOT, 'index.html')}
html_files = glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)

for path in sorted(html_files):
    if path in skip:
        continue
    patch_file(path)

print('\nDone.')
