import urllib.request
import urllib.parse
import json
import re

champs = {
    29: "Twitch",
    96: "Kog'Maw",
    119: "Draven",
    222: "Jinx",
    51: "Caitlyn",
    145: "Kai'Sa",
    110: "Varus",
    22: "Ashe",
    81: "Ezreal"
}

def check(region, name, tag):
    url = f"https://www.op.gg/summoners/{region}/{urllib.parse.quote(name)}-{urllib.parse.quote(tag)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode('utf-8', errors='ignore')
            m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
            if not m:
                print(name, "No NEXT_DATA")
                return
            data = json.loads(m.group(1))
            props = data.get('props', {}).get('pageProps', {}).get('data', {})
            stats = props.get('league_stats', [])
            tier_str = "Unranked"
            if stats:
                t = stats[0].get('tier_info', {})
                tier_str = f"{t.get('tier')} {t.get('division')} ({t.get('lp')} LP)"
            print(f"=== {name}#{tag} ({region.upper()}): {tier_str} ===")
            games = props.get('games', [])
            for g in games[:8]:
                my = g.get('myData', {})
                st = my.get('stats', {})
                res = "WIN" if st.get('result') == "WIN" else "LOSS"
                cid = my.get('champion_id')
                cname = champs.get(cid, str(cid))
                k = st.get('kill', 0)
                d = st.get('death', 0)
                a = st.get('assist', 0)
                cs = st.get('cs', 0)
                sec = g.get('game_length_second', 1)
                dur = sec / 60.0
                csm = cs / dur if dur > 0 else 0
                dt = g.get('created_at', '')[:16]
                q = g.get('queue_info', {}).get('game_type_name', '')
                print(f"  [{dt}] {q} | {cname} | {res} | {k}/{d}/{a} | CS: {cs} ({csm:.1f}/m) | {dur:.0f}m")
    except Exception as e:
        print(f"Error {name}: {e}")

check("eune", "ČIMY", "SUP")
check("eune", "Orbwalk", "ONN")
check("euw", "In the Dark", "CHALL")
