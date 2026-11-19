import urllib.request, re, json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

url = "https://www.op.gg/summoners/euw/In%20the%20Dark-CHALL"
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
        names = re.findall(r'"name":"([^"]+ - Ranked Solo/Duo)"', html)
        kills = re.findall(r'"kills","value":(\d+)', html)
        deaths = re.findall(r'"deaths","value":(\d+)', html)
        assists = re.findall(r'"assists","value":(\d+)', html)
        cs_list = re.findall(r'"cs","value":(\d+)', html)
        times = re.findall(r'"startTime":"([^"]+)"', html)
        for i in range(len(names)):
            if "Heimer" in names[i]:
                print(f"Heimer match: {names[i]} | {kills[i]}/{deaths[i]}/{assists[i]} | {times[i]}")
except Exception as e:
    print("Err:", e)
