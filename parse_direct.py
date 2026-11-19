with open(r'c:\Users\stepan.gajdacz\Documents\Gajdy_wdym\cimy.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

names = re.findall(r'"name":"([^"]+ - Ranked Solo/Duo|[^"]+ - Arena)"', text)
print("Names:", names)
kills = re.findall(r'"kills","value":(\d+)', text)
deaths = re.findall(r'"deaths","value":(\d+)', text)
assists = re.findall(r'"assists","value":(\d+)', text)
cs_list = re.findall(r'"cs","value":(\d+)', text)
times = re.findall(r'"startTime":"([^"]+)"', text)

for i in range(len(names)):
    print(f"{i+1}. [{times[i][:16]}] {names[i]} | {kills[i]}/{deaths[i]}/{assists[i]} | CS: {cs_list[i]}")
