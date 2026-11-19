import re

with open(r'c:\Users\stepan.gajdacz\Documents\Gajdy_wdym\cimy.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Tier matches
tiers = re.findall(r'"tier":"([^"]+)","division":(\d+),"lp":(\d+)', text)
print("Tier matches:", tiers)

# Let's inspect some occurrences of Twitch (id 29) or champion_id
# Find JSON objects or fragments with stats
pattern = r'"kill":(\d+),"death":(\d+),"assist":(\d+).*?"cs":(\d+).*?"result":"([^"]+)"'
stats = re.findall(pattern, text)
print("Stats found:", len(stats))
for s in stats[:10]:
    print(s)

# Also check date or created_at
dates = re.findall(r'"created_at":"([^"]+)"', text)
print("Dates found:", dates[:10])

# Check champions
champs = re.findall(r'"champion_id":(\d+)', text)
print("Champs:", champs[:10])
