# Arcade Hra s Ekonomickým Systémem

## Popis a cíl projektu

Cílem projektu je vytvoření hry v Pythonu pomocí knihovny Pygame, která kombinuje jednoduchou herní mechaniku (pohyb čtverce a nárazy do stěn) s komplexním systémem upgradů a prestiže. Hra je inspirována žánrem „idle/incremental game" – hráč vydělává body, které investuje do upgradů pro zrychlení dalšího příjmu.

Hra je určena komukoliv, kdo si chce zahrát jednoduchou, ale návykovou hru s hlubokým progresním systémem.

## Funkcionalita programu

Program se skládá z těchto hlavních technických částí:

- **Herní smyčka (game loop):** Nekonečná smyčka zpracovávající vstupy, aktualizující stav a překreslující okno při 60 FPS.
- **Pohyb a detekce kolizí:** Čtverec se pohybuje pomocí kláves WASD. Kolize se stěnou je detekována hraničními podmínkami souřadnic a spouští připsání bodů.
- **Systém upgradů (Shop):** Hráč nakupuje upgrady za získané body:
  - *Wall Bonus* – zvyšuje body za každý náraz (vzorec: `(1 + level) × 2^(level // 5)`)
  - *Multi Base Gain* – násobí veškerý příjem (vzorec: `1.2^level`)
- **Systém pasivního příjmu:** Po odemknutí prestiže se body generují automaticky každou sekundu (vzorec: `(score/100)^0.6 × 0.1 × (1.2^level) × (5^(level // 10))`).
- **Prestige & Rebirth systém:** Po nashromáždění rebirth bodů může hráč provedět „rebirth" – resetuje základní progres, ale odemyká stromové prestige upgrady, které trvale znásobují příjem.
- **Prestige Upgrade Tree:** Strom 15 upgradů rozdělených do 4 úrovní (Tier 1–4) s prerekvizitami. Každý upgrade má jiný efekt a maximální počet úrovní.
- **Prestige (Milestones) systém:** Nadstavba nad Rebirth systémem. Jakmile hráč získá 100 000 Rebirth bodů, může provést "Prestige". Tím se resetuje celý postup včetně Rebirth stromu, ale získá trvalé milníky (např. automatických 1 000 000 skóre, 100x globální násobič, pasivní boost), které masivně zrychlují další hraní.
- **Formátování velkých čísel:** Funkce `format_large_number()` zobrazuje čísla ve vědecké notaci, nebo při odemknutí „Break Infinity" upgradu v rozšířené Break Infinity notaci (`1ee12`).

## Technická část

### Použité knihovny

| Knihovna | Účel |
|---|---|
| `pygame` | Tvorba okna, vykreslování, zpracování vstupu |
| `sys` | Ukončení programu |
| `math` | Výpočty (sqrt, log10) pro prestige a notaci |
| `random` | Importován, připraven pro budoucí rozšíření |

### Klíčové algoritmy a datové struktury

**Detekce kolize:**
```python
def is_colliding_with_wall(x, y, size):
    return x <= 0 or (x + size) >= SIRKA or y <= 0 or (y + size) >= VYSKA
```
Skóre se přičítá pouze při přechodu z „ne-kolize" na „kolizi" (přes stavovou proměnnou `prev_colliding`), aby nedocházelo k vícenásobnému připsání za jedno dotýkání se stěny.

**Exponenciální cenové vzorce:**
- Wall Bonus cena: `5 × 1.4^level`
- Passive Gain cena: `10 × 1.5^level`
- Multi Base Gain cena: `20 × 1.6^level`

**Prestige Upgrade Tree:**  
Datová struktura slovníku – každý upgrade obsahuje `cost`, `prereq` (seznam prerekvizit), `level` a `max_level`. Dostupnost se dynamicky kontroluje při vykreslování a kliknutí.

**Break Infinity notace:**  
Pro čísla větší než `1e306` je použita dvojitá logaritmická notace: `1ee{log10(log10(num)):.1f}`.

### Struktura programu

```
hra.py
├── Import knihoven a inicializace Pygame
├── Konstanty (rozměry okna, barvy, písma)
├── Herní proměnné (čtverce, skóre, upgrade úrovně)
├── Prestige Upgrade Tree (slovník upgradů)
├── Výpočetní funkce
│   ├── calculate_*_cost()       – ceny upgradů
│   ├── calculate_*_damage()     – efekty
│   ├── calculate_passive_gain_per_second()
│   ├── calculate_prestige_multiplier()
│   └── format_large_number()    – notace čísel
├── Hlavní herní smyčka
│   ├── Zpracování událostí (klávesy, kliknutí, zavření)
│   ├── Pohyb čtverců a detekce kolizí
│   ├── Výpočet a přirčtení pasivního příjmu
│   └── Vykreslování (HUD, shop, rebirth tree, různá menu)
└── Ukončení (pygame.quit, sys.exit)
```
