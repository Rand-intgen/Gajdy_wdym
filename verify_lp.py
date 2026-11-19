import urllib.request, re, json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

url = "https://www.op.gg/summoners/euw/In%20the%20Dark-CHALL"
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
        # check exact tier and lp from html
        m = re.findall(r'(Platinum|Emerald|Gold)\s*([1-4])\s*(\d+)\s*LP', html, re.IGNORECASE)
        print("Tiers/LPs matched:", m)
        # also look for lp in json data
        m_lp = re.findall(r'"tier":"([^"]+)","division":(\d+),"lp":(\d+)', html)
        print("JSON LP matched:", m_lp)
        m_desc = re.search(r'content="([^"]*Platinum[^"]*)"', html)
        if m_desc:
            print("Meta desc:", m_desc.group(1)[:200])
except Exception as e:
    print("Err:", e)
