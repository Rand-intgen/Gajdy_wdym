import urllib.request, re, json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# Let's inspect the match via leagueofgraphs or op.gg internal API/json
url = "https://www.leagueofgraphs.com/summoner/euw/In+the+Dark-CHALL"
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
        # find recent games
        print("LeagueOfGraphs length:", len(html))
        # Look for the match row
        idx = html.find("Twitch")
        if idx != -1:
            print("LOG Snippet:")
            # find player names or champion icons
            lines = [l.strip() for l in html[idx:idx+3000].splitlines() if len(l.strip()) > 0]
            for l in lines[:25]:
                print(l[:100])
except Exception as e:
    print("Err LOG:", e)
