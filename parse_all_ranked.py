import urllib.request, re, json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# Let's inspect u.gg directly or fetch more games from op.gg
url = "https://www.op.gg/summoners/euw/In%20the%20Dark-CHALL"
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
        # check current lp and tier
        m = re.findall(r'(Platinum|Emerald|Gold)\s*([1-4])\s*(\d+)\s*LP', html, re.IGNORECASE)
        print("Tiers/LPs:", m[:5])
        # look for games from Nov 7, 8, 9
        names = re.findall(r'"name":"([^"]+ - Ranked Solo/Duo)"', html)
        kills = re.findall(r'"kills","value":(\d+)', html)
        deaths = re.findall(r'"deaths","value":(\d+)', html)
        assists = re.findall(r'"assists","value":(\d+)', html)
        cs_list = re.findall(r'"cs","value":(\d+)', html)
        times = re.findall(r'"startTime":"([^"]+)"', html)
        print("Recent ranked games:")
        for i in range(len(names)):
            print(f"  {times[i][:16]} | {names[i]} | {kills[i]}/{deaths[i]}/{assists[i]} | CS: {cs_list[i]}")
except Exception as e:
    print("Err:", e)
