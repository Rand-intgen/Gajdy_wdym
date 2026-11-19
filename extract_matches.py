with open(r'c:\Users\stepan.gajdacz\Documents\Gajdy_wdym\cimy.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find the exact text describing the recent matches
idx = text.find("Across the 10 included recent matches")
if idx != -1:
    print(text[idx:idx+2500])
