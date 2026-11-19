with open(r'c:\Users\stepan.gajdacz\Documents\Gajdy_wdym\cimy.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

matches = re.findall(r'"champion":"([^"]+)","result":"([^"]+)","kills":(\d+),"deaths":(\d+),"assists":(\d+).*?"cs":(\d+).*?"queueType":"([^"]+)"', text)
print("Total parsed matches:", len(matches))
for i, m in enumerate(matches[:10]):
    print(f"{i+1}. {m[6]} | {m[0]} | {m[1]} | {m[2]}/{m[3]}/{m[4]} | CS: {m[5]}")
