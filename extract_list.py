with open(r'c:\Users\stepan.gajdacz\Documents\Gajdy_wdym\cimy.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

idx = text.find('ItemListElement')
if idx == -1:
    idx = text.find('itemListElement')

if idx != -1:
    print(text[idx:idx+4000])
