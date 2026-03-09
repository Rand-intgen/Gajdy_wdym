# Projekt: Gajdy_wdym - Interaktivní Arcade Hra s Ekonomickým Systémem

## Cíl Projektu

Vytvořit plně funkcční a zabavující arcade hru v Pythonu s použitím Pygame, která kombinuje jednoduchou herní mechaniku (pohyb a srážky) s komplexním ekonomickým systémem exponenciálních upgradů. Projekt slouží k demonstraci:

- Ovládání grafických herních prvků (Pygame)
- Implementace matematických vzorců pro ekonomické modelování
- Správy stavu hry a objektů v reálném čase
- Uživatelského rozhraní v herním prostředí

## Specifikace Projektu

### Funkční Požadavky

1. **Herní Mechanika**
   - Pohybující se čtverec, který hráč řídí klávesami WASD
   - Detekce kolizí se stěnami okna
   - Genství skóre za každý náraz do stěny
   - Zobrazování aktuálního skóre a dalších statistik v HUD

2. **Upgrade Systém**
   - Passive Gain upgrade - automatická tvorba bodů
   - Wall Bonus upgrade - zvýšení bodů za náraz
   - Exponenciální růst cen upgradů
   - Exponenciální zvyšování efektu upgradů
   - Správa úrovní a nákladů každého upgradu

3. **Numerická Robustnost**
   - Podpora velmi velkých čísel (až 1e300)
   - Automatické přepnutí na vědeckou notaci pro čitatelnost
   - Formátování s tisícovými oddělovači pro menší čísla

4. **Uživatelské Rozhraní**
   - Navigace v shopu s upgrady
   - Zobrazování cen a efektů upgradů
   - Zobrazování statistik (skóre, pasivní příjem, počet čtverců atd.)

### Architektura Systému

#### Hlavní Komponenty

```
hra.py
├── Inicializace (Pygame setup)
├── Definice konstant (rozměry, barvy)
├── Systém upgradů (kalkulace cen a efektů)
├── Herní smyčka
│   ├── Zpracování vstupů (WASD, myš)
│   ├── Aktualizace stavu
│   ├── Detekce kolizí
│   ├── Výpočet pasivního příjmu
│   └── Vykreslování
└── Event handling (QUIT, mouse clicks)
```

#### Klíčové Funkce

**calculate_passive_gain_cost(level)**
- Určuje cenu pro nákup pasivního příjmu na danou úroveň
- Vzorec: `10 × 1.5^level`
- Účel: Exponenciálně zvyšuje cenu s každou úrovní

**calculate_wall_bonus_cost(level)**
- Určuje cenu pro nákup wall bonusu na danou úroveň
- Vzorec: `5 × 1.4^level`
- Účel: Exponenciálně zvyšuje cenu s každou úrovní

**calculate_wall_bonus_damage(level)**
- Vypočítá počet bodů za náraz do stěny s danou úrovní wall bonusu
- Vzorec: `(1 + level) × 2^(level/5)`
- Logika: Základní zvyšování + mega-zvyšování každých 5 levelů

**calculate_passive_gain_per_second(current_score, level)**
- Vypočítá automatickou produkci bodů za sekundu
- Vzorec: `(score/100)^0.6 × 0.1 × (1.2^level) × (5^(level/10))`
- Logika: 
  - Spuští se až po dosáhnutí skóru 1000
  - Roste s mocninou 0.6 od skóre (pomalejší růst než kvadratický)
  - Multiplicita s úrovní upgradu (faktor 1.2)
  - Mega-faktor každých 10 levelů (5x zesílení)

### Vývoj a Iterace

#### Iterace 1: Základní Herní Smyčka
- Vytvoření okna s Pygame
- Implementace pohybu čtverce pomocí šipek
- Implementace detekce kolizí se stěnami
- Získávání bodů za nárazy

#### Iterace 2: Upgrade Systém
- Implementace Passive Gain upgradu
- Implementace Wall Bonus upgradu
- Vytvořte obchod (shop) s pořizovatelným rozhraním
- Správa úrovní upgradů a jejich cen

#### Iterace 3: Numerická Optimalizace
- Přidání vědecké notace pro velká čísla
- Rozšíření limitu pro vědeckou notaci na 1e300

#### Iterace 4: Game Balance
- Změna řízení z šipek na WASD (ergonomie)
- Pozdější spuštění Passive Gain (od 1000 místo 100)
- Pomalejší růst Passive Gain (exponent 0.6 místo 1.05)

### Technologické Rozhodnutí

1. **Pygame** - Zvoleno pro jednoduchost, portabilitu a dostupnost
2. **Slovníky pro objekty** - Místo tříd pro jednoduchost
3. **Exponenciální vzorce** - Pro adekvátní ekonomickou simulaci
4. **Vědecká notace** - Pro podporu astronomických čísel

### Testování

Projekt byl otestován na:
- ✅ Korektní detekce kolizí
- ✅ Správné výpočty upgradů
- ✅ Správné zobrazování velkých čísel
- ✅ Responzivní ovládání
- ✅ Generování nových čtverců po zničení

### Úrovně Náročnosti

Projekt odpovídá **Úrovni 4: Těžká**
- Obsahuje algoritmizaci (kolize, ekonomické výpočty)
- Implementuje externalní framework (Pygame)
- Používá strukturované datové struktury (slovníky, seznamy)
- Aplikuje matematické koncepty (exponenciální funkce)
- Má komplexní stav hry a event handling

### Budoucí Rozšíření

Možná vylepšení:
- Přidání více typů čtverců s různými vlastnostmi
- Systém dosahů (achievements)
- Uložení a načítání her
- Zvukové efekty aBackground Music
- Různé úrovně obtížnosti
- Leaderboard systém
- Animace a vizuální efekty

## Souhrn

Projekt "Gajdy_wdym" je komplexní arcade hra, která kombinuje jednoduché herní prvky s sofistikovaným ekonomickým systémem. Hra je plně funkcční a nabízí hodinově hraničitého zábavu s možností nekonečného progressu. Projekt demonstruje schopnost práce s herními frameworky, matematickými vzorci a správou komplexního stavu v reálném čase.
