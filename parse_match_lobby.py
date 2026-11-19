import urllib.request, re, json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

url = "https://www.op.gg/summoners/euw/In%20the%20Dark-CHALL"
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
        # Search for summoner names or next data chunks
        chunks = re.findall(r'self\.__next_f\.push\(\[1,\s*\"(.*?)\"\]\)', html)
        print("Found next chunks:", len(chunks))
        full = "".join(chunks).replace('\\"', '"').replace('\\\\', '\\')
        # Find the game with 14 kills and 12 deaths
        idx = full.find('"kill":14,"death":12')
        if idx == -1:
            idx = full.find('"kills":14,"deaths":12')
        if idx != -1:
            print("Found game with 14/12!")
            snippet = full[max(0, idx-500):min(len(full), idx+2500)]
            # extract participant names and champions
            names = re.findall(r'"summoner_name":"([^"]+)"', snippet)
            winrates = re.findall(r'"win":(\d+),"lose":(\d+)', snippet)
            print("Names found:", names)
            print("Winrates found:", winrates)
        else:
            print("14/12 pattern not found directly, looking for participants...")
            parts = re.findall(r'"name":"([^"]+#[^"]+)"', full)
            print("Tags found:", parts[:15])
except Exception as e:
    print("Err:", e)
