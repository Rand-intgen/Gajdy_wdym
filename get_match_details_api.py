import urllib.request, re, json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# fetch the match history json api of op.gg directly
# https://op.gg/api/v1.0/internal/bypass/games/euw/summoners/<summoner_id>
# Or get puuid
puuid = "s0W6Zp-p3fI_33oVjG86kC4fM1F2sH5e27HjX8N8m9V5sA" # let's search in html
with open(r"c:\Users\stepan.gajdacz\Documents\Gajdy_wdym\cimy.html", "r", encoding="utf-8") as f:
    pass

url = "https://www.op.gg/summoners/euw/In%20the%20Dark-CHALL"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as r:
    html = r.read().decode('utf-8', errors='ignore')

m_puuid = re.search(r'"puuid","value":"([^"]+)"', html)
if m_puuid:
    p = m_puuid.group(1)
    print("Found PUUID:", p)
    api_url = f"https://op.gg/api/v1.0/internal/bypass/games/euw/summoners/{p}?&limit=5&hl=en_US&game_type=soloranked"
    try:
        req2 = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req2) as r2:
            data = json.loads(r2.read().decode('utf-8'))
            print("API games found:", len(data.get('data', [])))
            for g in data.get('data', [])[:1]:
                print("Game detail:", g.get('id'))
                participants = g.get('participants', [])
                for part in participants:
                    s_name = part.get('summoner', {}).get('name')
                    tag = part.get('summoner', {}).get('tagline')
                    c_name = part.get('champion_name')
                    st = part.get('stats', {})
                    k = st.get('kill')
                    d = st.get('death')
                    a = st.get('assist')
                    # check tier or winrate
                    tier = part.get('tier_info', {}).get('tier')
                    div = part.get('tier_info', {}).get('division')
                    lp = part.get('tier_info', {}).get('lp')
                    print(f"  {c_name} ({s_name}#{tag}) | {k}/{d}/{a} | {tier} {div} ({lp} LP)")
    except Exception as e:
        print("API Err:", e)
