import urllib.request
import re

def check_account(region, name, tag):
    url = f"https://www.op.gg/summoners/{region}/{name}-{tag}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode('utf-8', errors='ignore')
            names = re.findall(r'"name":"([^"]+ - Ranked Solo/Duo|[^"]+ - Arena)"', html)
            kills = re.findall(r'"kills","value":(\d+)', html)
            deaths = re.findall(r'"deaths","value":(\d+)', html)
            assists = re.findall(r'"assists","value":(\d+)', html)
            times = re.findall(r'"startTime":"([^"]+)"', html)
            m_desc = re.search(r'content="([^"]*Win rate[^"]*)"', html)
            print(f"=== {name}#{tag} ({region.upper()}) ===")
            if m_desc:
                print(m_desc.group(1)[:200])
            for i in range(min(5, len(names))):
                print(f"  {times[i][:16]} | {names[i]} | {kills[i]}/{deaths[i]}/{assists[i]}")
    except Exception as e:
        print("Err:", e)

check_account("euw", "In%20the%20Dark", "CHALL")
