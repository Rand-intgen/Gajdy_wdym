with open(r'c:\Users\stepan.gajdacz\Documents\Gajdy_wdym\cimy.html', 'r', encoding='utf-8') as f:
    text = f.read()

import json, re

idx = text.find('itemListElement')
if idx != -1:
    end = text.find(']}]', idx)
    raw = text[idx-1:end+3]
    # parse manually items
    items = re.findall(r'\{"@type":"ListItem".*?\}\}\}', text)
    print("Items found:", len(items))
    for it in items:
        champ = re.search(r'"champion","value":"([^"]+)"', it)
        res = re.search(r'"result","value":"([^"]+)"', it)
        k = re.search(r'"kills","value":(\d+)', it)
        d = re.search(r'"deaths","value":(\d+)', it)
        a = re.search(r'"assists","value":(\d+)', it)
        cs = re.search(r'"cs","value":(\d+)', it)
        q = re.search(r'"queueType","value":"([^"]+)"', it)
        time = re.search(r'"startTime":"([^"]+)"', it)
        c = champ.group(1) if champ else "?"
        r = res.group(1) if res else "?"
        k_v = k.group(1) if k else "0"
        d_v = d.group(1) if d else "0"
        a_v = a.group(1) if a else "0"
        cs_v = cs.group(1) if cs else "0"
        q_v = q.group(1) if q else "?"
        t_v = time.group(1)[:16] if time else "?"
        print(f"[{t_v}] {q_v} | {c} | {r} | {k_v}/{d_v}/{a_v} | CS: {cs_v}")
