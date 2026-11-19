import urllib.request, re, json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

url = "https://www.op.gg/summoners/eune/Orbwalk-ONN"
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
        # find cs and stats for sivir
        idx = html.find("Sivir WIN")
        if idx != -1:
            print(html[idx-100:idx+600])
        else:
            print("Sivir WIN text not found directly")
except Exception as e:
    print("Err:", e)
