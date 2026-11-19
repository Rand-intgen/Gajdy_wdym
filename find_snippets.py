with open(r'c:\Users\stepan.gajdacz\Documents\Gajdy_wdym\cimy.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Look for where 'Twitch' or 'ČIMY' appears
print("Twitch count:", text.count("Twitch"))
print("ČIMY count:", text.count("ČIMY"))

matches = [m.start() for m in re.finditer(r'Twitch', text)]
for idx in matches[:5]:
    print("--- SNIPPET ---")
    print(text[max(0, idx-100):min(len(text), idx+200)])
