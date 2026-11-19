import urllib.request, re, json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def refresh_and_check(region, name, tag):
    # Trigger renew/update on op.gg
    # First get summoner info to find id or trigger renew
    url = f"https://www.op.gg/summoners/{region}/{name}-{tag}"
    req = urllib.request.Request(url, headers=headers)
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
                print(m_desc.group(1)[:250])
            for i in range(min(7, len(names))):
                print(f"  {times[i][:16]} | {names[i]} | {kills[i]}/{deaths[i]}/{assists[i]}")
    except Exception as e:
        print("Err:", e)

refresh_and_check("eune", "Orbwalk", "ONN")
refresh_and_check("eune", "%C4%8CIMY", "SUP")
refresh_and_check("euw", "In%20the%20Dark", "CHALL")
