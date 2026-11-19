import urllib.request
import re

req = urllib.request.Request(
    'https://www.op.gg/summoners/eune/%C4%8CIMY-SUP',
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)
with urllib.request.urlopen(req) as r:
    html = r.read().decode('utf-8', errors='ignore')

# Save part to analyze
with open(r'c:\Users\stepan.gajdacz\Documents\Gajdy_wdym\cimy.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved cimy.html, size:", len(html))
