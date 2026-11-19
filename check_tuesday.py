import urllib.request, re, json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

url = "https://www.op.gg/summoners/euw/In%20the%20Dark-CHALL"
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
        m_desc = re.search(r'content="([^"]*Win rate[^"]*)"', html)
        if m_desc:
            print("Summary:", m_desc.group(1))
        names = re.findall(r'"name":"([^"]+ - Ranked Solo/Duo|[^"]+ - Arena)"', html)
        kills = re.findall(r'"kills","value":(\d+)', html)
        deaths = re.findall(r'"deaths","value":(\d+)', html)
        assists = re.findall(r'"assists","value":(\d+)', html)
        cs_list = re.findall(r'"cs","value":(\d+)', html)
        times = re.findall(r'"startTime":"([^"]+)"', html)
        print("Matches found:", len(names))
        for i in range(min(6, len(names))):
            t = times[i][:16] if i < len(times) else "?"
            cs = cs_list[i] if i < len(cs_list) else "?"
            print(f"{i+1}. [{t}] {names[i]} | {kills[i]}/{deaths[i]}/{assists[i]} | CS: {cs}")
except Exception as e:
    print("Err:", e)
