import urllib.request, re, json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

url = "https://www.op.gg/summoners/euw/In%20the%20Dark-CHALL"
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
        # Find the participants of the latest match
        # Let's search for json blocks or match details in html
        print("HTML length:", len(html))
        # Look for the last match ID or participants
        m_ids = re.findall(r'"matchId","value":"([^"]+)"', html)
        print("Match IDs found:", m_ids[:5])
        # Look for participants names in the html
        # Often in next data or script tags
        # Let's search for champion names in the last match: Twitch, Nami, Pyke, Jinx
        idx = html.find("Pyke")
        if idx != -1:
            print("Snippet around Pyke:")
            print(html[max(0, idx-200):min(len(html), idx+800)])
        else:
            print("Pyke not found in raw html snippet")
except Exception as e:
    print("Err:", e)
