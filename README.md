# Gajdy_wdym

**Popis a cíl projektu:**
Arkadová hra s ekonomickým „idle/incremental“ systémem. Cílem je procházet herním polem, získávat body narážením do stěn a utrácet je za upgrady, které dále zrychlují zisk bodů. 

**Popis funkcionality programu:**
- Klávesami WASD hráč pohybuje čtvercem po hrací ploše.
- Za každý náraz do stěny okna se hráči přičte skóre.
- Menu **Upgrades** umožňuje nákup okamžitých vylepšení (např. body za náraz, základní násobič).
- Menu **Rebirth** nabízí systém prvního resetu: za nashromážděné skóre získá hráč „Rebirth body“, které investuje do mocného stromu schopností (Rebirth Upgrade Tree) generujícího pasivní příjmy a násobiče.
- Menu **Prestige** je ultimátní vrstvou: za 100 000 Rebirth bodů hráč navždy odemyká milníky (Milestones) poskytující masivní výhody napříč následnými hrami.

**Technická část:**
- **Použité knihovny:** `pygame` (okno, hlavní 60 FPS smyčka, detekce kolizí a klávesnice), `math` (exponenciální a logaritmické výpočty pro herní ekonomiku). Nepoužívá se žádné externí API.
- **Algoritmy:** Exponenciální vzorce cen a vlivu upgradů (`base * multiplier^level`). Zvláštní algoritmus ošetřující kolize používá stavové pole `prev_colliding`, aby byl jeden náraz započten jen jednou za přechod.
- **Datové struktury:** Vlastní hierarchický vnořený slovník `prestige_upgrades` uchovávající cenu, prerekvizity a úroveň každého skillu ve stromu prestiže.
- **Zpracování dat:** Funkce `format_large_number` pro plynulý přechod herních hodnot od základních čísel, přes vědeckou notaci až po proprietární Break Infinity notaci (`1eeX`) pro čísla přesahující limit `float` (1e306).
