import pygame # Importuje knihovnu Pygame
import sys # Importuje systémový modul
import random

# Inicializace Pygame
pygame.init() # Inicializuje Pygame

# Nastavení okna
SIRKA = 1080 # Nastaví šířku okna
VYSKA = 920 # Nastaví výšku okna
okno = pygame.display.set_mode((SIRKA, VYSKA)) # Vytvoří okno
pygame.display.set_caption("Souřadnicový systém - Fáze 2") # Nastaví titulek okna

# Barvy
CERNA = (0, 0, 0) # Definuje černou barvu
BILA = (255, 255, 255) # Definuje bílou barvu
CERVENA = (255, 0, 0) # Definuje červenou barvu

# Nastavení objektu (čtverec)
velikost_ctverce = 50 # Nastaví velikost čtverce
start_x = SIRKA // 2 - velikost_ctverce // 2 # Vycentruje X souřadnici
start_y = VYSKA // 2 - velikost_ctverce // 2 # Vycentruje Y souřadnici
rychlost = 5 # Nastaví rychlost pohybu

# Seznam čtverců (každý čtverec je slovník s pozicí a velikostí)
squares = [{'x': start_x, 'y': start_y, 'size': velikost_ctverce}]
# Track previous-collision state per square, aby se skóre přičetlo jen jednou při nárazu
prev_colliding = [False]

# Skóre
score = 0

# Nastavení písma pro zobrazení souřadnic a skóre
pismo = pygame.font.SysFont("Arial", 24) # Nastaví písmo Arial velikost 24
# Menší písmo pro settings popisky
small_pismo = pygame.font.SysFont("Arial", 16)
# Velmi malé písmo pro upgrade tree tlačítka
tiny_pismo = pygame.font.SysFont("Arial", 10)

# Hlavní smyčka
bezi = True # Nastaví pro smyčku
hodiny = pygame.time.Clock() # Vytvoří hodiny pro řízení FPS

# Shop / upgrades
shop_open = False
shop_button_rect = pygame.Rect(SIRKA - 110, 10, 100, 30)
points_per_hit = 1  # základní body za náraz (bude se zvyšovat upgrady)

# Settings menu
settings_open = False
settings_button_rect = pygame.Rect(SIRKA - 220, 10, 100, 30)
# In-code flag: enable automatic scientific formatting for very large numbers
eternitynum = True

# Rebirth / Prestige systém
rebirth_open = False
rebirth_button_rect = pygame.Rect(SIRKA - 330, 10, 100, 30)
rebirth_points = 0  # Měna pro rebirth - kumuluje se a resetuje skóre/upgrady
prestige_points = 0  # Měna pro prestige upgradů
prestige_multiplier = 1.0  # Bonusový multiplikátor skóre z prestige upgradů
break_infinity_unlocked = False  # Zda je odemknut Break Infinity upgrade

# Prestige Upgrade Tree - komplexní systém inspirovaný The Ultimate Upgrade Tree
# Struktura: "upgrade_name": {"cost": cena, "prereq": [], "unlocked": False, "effect": funkce}
prestige_upgrades = {
    # Základní upgrady (Tier 1) - bez prerekvizit
    "Automation (Passive Gain)": {"cost": 1, "prereq": ["Score Booster"], "unlocked": False, "level": 0, "max_level": 20},
    "Score Booster": {"cost": 2, "prereq": [], "unlocked": False, "level": 0, "max_level": 15},
    "Point Multiplier": {"cost": 3, "prereq": ["Score Booster"], "unlocked": False, "level": 0, "max_level": 10},
    
    # Mid-game upgrady (Tier 2) - vyžadují základní
    "Passive Amplifier": {"cost": 5, "prereq": ["Automation (Passive Gain)"], "unlocked": False, "level": 0, "max_level": 12},
    "Efficiency Boost": {"cost": 4, "prereq": ["Point Multiplier"], "unlocked": False, "level": 0, "max_level": 15},
    "Greater Infinity I": {"cost": 6, "prereq": ["Automation (Passive Gain)"], "unlocked": False, "level": 0, "max_level": 8},
    
    # Pokročilé upgrady (Tier 3) - vyžadují mid-game
    "Super Charge": {"cost": 8, "prereq": ["Passive Amplifier", "Efficiency Boost"], "unlocked": False, "level": 0, "max_level": 10},
    "Infinity Engine": {"cost": 10, "prereq": ["Greater Infinity I"], "unlocked": False, "level": 0, "max_level": 6},
    "Quantum Leap": {"cost": 12, "prereq": ["Super Charge"], "unlocked": False, "level": 0, "max_level": 5},
    
    # Elite upgrady (Tier 4) - vyžadují pokročilé
    "Break Infinity": {"cost": 50, "prereq": ["Infinity Engine", "Quantum Leap"], "unlocked": False, "level": 0, "max_level": 1},
    "Ultimate Power": {"cost": 25, "prereq": ["Quantum Leap"], "unlocked": False, "level": 0, "max_level": 3},
    "Rebirth Mastery": {"cost": 30, "prereq": ["Break Infinity"], "unlocked": False, "level": 0, "max_level": 1},
    
    # Alternativní větve
    "Speed Demon": {"cost": 7, "prereq": ["Efficiency Boost"], "unlocked": False, "level": 0, "max_level": 8},
    "Wealth Generator": {"cost": 9, "prereq": ["Speed Demon"], "unlocked": False, "level": 0, "max_level": 6},
    "Time Warp": {"cost": 15, "prereq": ["Wealth Generator", "Infinity Engine"], "unlocked": False, "level": 0, "max_level": 4}
}

# Upgrade systém
passive_gain_level = 0  # Úroveň passive gain upgradu
wall_bonus_level = 0  # Úroveň wall bonus upgradu
multi_base_gain_level = 0  # Úroveň multi base gain upgradu (násobí pasivní gain)
rebirth_requirement = 10000  # Kolik rebirth pointů je potřeba na rebirth

def calculate_passive_gain_cost(level):
    """Vypočítá cenu pro nákup passive gain upgradu.
    
    Exponenciální růst ceny: 10 * 1.5^level
    - Cena se zvyšuje s každou novou úrovní
    - Cíl: Kontrolovat inflaci dostatečně vysokými cenami
    - Př: level 0 = 10 bodů, level 5 = 76 bodů, level 10 = 576 bodů
    """
    return int(10 * (1.5 ** level))

def calculate_wall_bonus_cost(level):
    """Vypočítá cenu pro nákup wall bonus upgradu.
    
    Exponenciální růst ceny: 5 * 1.4^level
    - Pomalejší růst než Passive Gain (1.4 vs 1.5)
    - Více dostupné pro hráče začátečníky
    - Př: level 0 = 5 bodů, level 10 = 56 bodů, level 20 = 628 bodů
    """
    return int(5 * (1.4 ** level))

def calculate_multi_base_gain_cost(level):
    """Vypočítá cenu pro nákup multi base gain upgradu.
    
    Exponenciální růst ceny: 20 * 1.6^level
    - Podobný růst jako Passive Gain
    - Dražší než wall bonus
    - Př: level 0 = 20 bodů, level 5 = 165 bodů, level 10 = 1843 bodů
    """
    return int(20 * (1.6 ** level))

def calculate_multi_base_gain_multiplier(level):
    """Vypočítá multiplikátor pro pasivní gain z multi base gain upgradu.
    
    Vzorec: 1.2^level
    - Každá úroveň zvýší pasivní příjem o 20%
    - Level 1 = 1.2x, Level 5 = 2.49x, Level 10 = 6.19x
    """
    return (1.2 ** level)

def calculate_wall_bonus_damage(level):
    """Vypočítá počet bodů za náraz do stěny s wall bonus upgradem.
    
    Vzorec: (1 + level) * 2^(level // 5)
    - Lineární růst do level 4 (1 až 5 bodů)
    - Mega-skokový růst každých 5 levelů (zdvojnásobení)
    - Level 5-9: 6-10 bodů, Level 10-14: 12-20 bodů atd.
    - Cíl: Poskytnout hráčům dramatické zlepšení po dosažení milníků
    """
    return (1 + level) * (2 ** (level // 5))

def calculate_passive_gain_per_second(current_score, level):
    """Vypočítá pasivní gain za sekundu na základě aktuálního skóre a úrovně upgradu.
    
    Vzorec: (score/100)^0.6 × 0.1 × (1.2^level) × (5^(level//10))
    
    Poznámka: Aktivace je řízena prestige upgrade "Automation (Passive Gain)"
    
    Komponenty výpočtu:
    1. Základní část: (score/100)^0.6 - Pocházení z aktuálního skóre
       - Exponent 0.6 znamená pomalejší růst (sublineární)
       - Brání příliš rychlému zdvojnásobení příjmu
    
    2. Upgrade multiplier: 1.2^level
       - Každá úroveň zvýší příjem o 20%
       - Motivuje hráče k nákupům upgradů
    
    3. Mega multiplier: 5^(level//10)
       - Každých 10 levelů se efekt znásobí 5x
       - Poskytuje dramatické milníky (level 10, 20, 30...)
    """
    # Základní gain z aktuálního skóre
    # Exponent 0.6 zajišťuje, že pasivní příjem je pomalejší než exponenciální
    multiplier = (current_score / 100) ** 0.6
    base_gain = multiplier * 0.1  # 0.1 je škálovací faktor
    
    # Upgrade level multiplier - lineárně na exponenciální stupnici
    upgrade_multiplier = (1.2 ** level)
    
    # Mega-multiplier - dramatické zvýšení každých 10 levelů
    mega_multiplier = (5 ** (level // 10))
    
    # Kombinuj všechny faktory
    total_gain = base_gain * upgrade_multiplier * mega_multiplier
    return total_gain

def is_colliding_with_wall(x, y, size):
    return x <= 0 or (x + size) >= SIRKA or y <= 0 or (y + size) >= VYSKA

def calculate_prestige_points_from_score(current_score):
    """Vypočítá prestige body na základě dosažného skóru.
    
    Vzorec: sqrt(score) / 10
    - Hráč získává prestige body za rebirth
    - Více skóre = více prestige bodů na rebirth
    """
    if current_score < 1:
        return 0
    import math
    return int(math.sqrt(current_score) / 10)

def calculate_rebirth_points_from_score(current_score):
    """Vypočítá rebirth body na základě dosažného skóru.
    
    Vzorec: sqrt(score) / 5
    - Hráč získává rebirth body za rebirth
    - Více skóre = více rebirth bodů
    - Rebirth body se NIKDY neresetnují, kumulují se
    """
    if current_score < 1:
        return 0
    import math
    return int(math.sqrt(current_score) / 5)

def calculate_prestige_multiplier(prestige_upgrades):
    """Vypočítá multiplikátor skóre z prestige upgradů.
    
    Různé upgrady mají různé efekty:
    - Score Booster: +5% za level
    - Point Multiplier: +8% za level  
    - Efficiency Boost: +6% za level
    - Greater Infinity: +10% za level
    - Super Charge: +12% za level
    - Infinity Engine: +15% za level
    - Quantum Leap: +20% za level
    - Ultimate Power: +25% za level
    - Speed Demon: +7% za level
    - Wealth Generator: +18% za level
    - Time Warp: +30% za level
    """
    multiplier = 1.0
    
    # Základní upgrady
    if "Score Booster" in prestige_upgrades:
        multiplier *= (1.05 ** prestige_upgrades["Score Booster"]["level"])
    if "Point Multiplier" in prestige_upgrades:
        multiplier *= (1.08 ** prestige_upgrades["Point Multiplier"]["level"])
    
    # Mid-game upgrady
    if "Efficiency Boost" in prestige_upgrades:
        multiplier *= (1.06 ** prestige_upgrades["Efficiency Boost"]["level"])
    if "Greater Infinity I" in prestige_upgrades:
        multiplier *= (1.10 ** prestige_upgrades["Greater Infinity I"]["level"])
    
    # Pokročilé upgrady
    if "Super Charge" in prestige_upgrades:
        multiplier *= (1.12 ** prestige_upgrades["Super Charge"]["level"])
    if "Infinity Engine" in prestige_upgrades:
        multiplier *= (1.15 ** prestige_upgrades["Infinity Engine"]["level"])
    if "Quantum Leap" in prestige_upgrades:
        multiplier *= (1.20 ** prestige_upgrades["Quantum Leap"]["level"])
    
    # Elite upgrady
    if "Ultimate Power" in prestige_upgrades:
        multiplier *= (1.25 ** prestige_upgrades["Ultimate Power"]["level"])
    
    # Alternativní větve
    if "Speed Demon" in prestige_upgrades:
        multiplier *= (1.07 ** prestige_upgrades["Speed Demon"]["level"])
    if "Wealth Generator" in prestige_upgrades:
        multiplier *= (1.18 ** prestige_upgrades["Wealth Generator"]["level"])
    if "Time Warp" in prestige_upgrades:
        multiplier *= (1.30 ** prestige_upgrades["Time Warp"]["level"])
    
    return multiplier

def calculate_passive_gain_multiplier_from_prestige(prestige_upgrades):
    """Vypočítá multiplikátor speciálně pro pasivní gain z prestige upgradů.
    
    - Automation: +15% za level (základní efekt pro pasivní gain)
    - Passive Amplifier: +10% za level
    - Super Charge: +12% za level (bonus pro pasivní gain)
    - Infinity Engine: +8% za level
    - Quantum Leap: +15% za level
    - Speed Demon: +6% za level
    - Wealth Generator: +20% za level (silný efekt)
    - Time Warp: +25% za level
    """
    multiplier = 1.0
    
    # Automation (Passive Gain) effect - základní
    if "Automation (Passive Gain)" in prestige_upgrades and prestige_upgrades["Automation (Passive Gain)"]["level"] > 0:
        multiplier *= (1.15 ** prestige_upgrades["Automation (Passive Gain)"]["level"])
    
    # Passive Amplifier effect
    if "Passive Amplifier" in prestige_upgrades:
        multiplier *= (1.10 ** prestige_upgrades["Passive Amplifier"]["level"])
    
    # Pokročilé efekty pro pasivní gain
    if "Super Charge" in prestige_upgrades:
        multiplier *= (1.12 ** prestige_upgrades["Super Charge"]["level"])
    if "Infinity Engine" in prestige_upgrades:
        multiplier *= (1.08 ** prestige_upgrades["Infinity Engine"]["level"])
    if "Quantum Leap" in prestige_upgrades:
        multiplier *= (1.15 ** prestige_upgrades["Quantum Leap"]["level"])
    
    # Alternativní větve
    if "Speed Demon" in prestige_upgrades:
        multiplier *= (1.06 ** prestige_upgrades["Speed Demon"]["level"])
    if "Wealth Generator" in prestige_upgrades:
        multiplier *= (1.20 ** prestige_upgrades["Wealth Generator"]["level"])
    if "Time Warp" in prestige_upgrades:
        multiplier *= (1.25 ** prestige_upgrades["Time Warp"]["level"])
    
    return multiplier

def format_large_number(num):
    """Zformátuje číslo s Break Infinity notací (1ee12) pro čísla > 1e306.
    
    Pokud num < 1e306: normální vědecká notace
    Pokud num >= 1e306: Break Infinity notace (1ee12 znamená 10^(10^12))
    """
    if not break_infinity_unlocked:
        # Bez Break Infinity: normální notace až 1e306
        if num >= 1e306:
            return "Infinity"
        else:
            return f"{num:.2e}"
    
    # S Break Infinity: rozšířená notace
    if num < 1e306:
        return f"{num:.2e}"
    
    # Číslo je větší než 1e306 - použij Break Infinity notaci
    import math
    if num == float('inf'):
        return "Infinity"
    
    # Vypočti exponent exponenta: log(log(num)) se základem 10
    try:
        outer_exp = math.log10(math.log10(num))
        return f"1ee{outer_exp:.1f}"
    except:
        return "Infinity"

while bezi: # Hlavní cyklus hry
    # Zpracování událostí
    for event in pygame.event.get(): # Načte všechny články
        if event.type == pygame.QUIT: # Pokud uživatel zavře okno
            bezi = False # Ukončí smyčku
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Kliknutí myší - přepnout shop pokud bylo kliknuto na tlačítko
            if shop_button_rect.collidepoint(event.pos):
                shop_open = not shop_open
                if shop_open:
                    settings_open = False
                    rebirth_open = False
            # Kliknutí myší - přepnout settings pokud bylo kliknuto na tlačítko
            if settings_button_rect.collidepoint(event.pos):
                settings_open = not settings_open
                if settings_open:
                    shop_open = False
                    rebirth_open = False
            # Kliknutí myší - přepnout rebirth pokud bylo kliknuto na tlačítko
            if rebirth_button_rect.collidepoint(event.pos):
                rebirth_open = not rebirth_open
                if rebirth_open:
                    shop_open = False
                    settings_open = False

            # Upgrade kliknutí v shopu
            if shop_open:
                mouse_x, mouse_y = event.pos
                wall_cost = calculate_wall_bonus_cost(wall_bonus_level)
                
                # Wall Bonus button area
                if (SIRKA//2 - 250 < mouse_x < SIRKA//2 + 250 and 
                    VYSKA//2 - 20 < mouse_y < VYSKA//2 + 10):
                    if score >= wall_cost:
                        score -= wall_cost
                        wall_bonus_level += 1
                
                # Multi Base Gain button area
                multi_cost = calculate_multi_base_gain_cost(multi_base_gain_level)
                if (SIRKA//2 - 250 < mouse_x < SIRKA//2 + 250 and 
                    VYSKA//2 + 20 < mouse_y < VYSKA//2 + 50):
                    if score >= multi_cost:
                        score -= multi_cost
                        multi_base_gain_level += 1

            # Kliknutí v settings - no interactive toggle any more (eternitynum controlled in code)
            if settings_open:
                pass

            # Upgrade kliknutí v rebirth menu
            if rebirth_open:
                mouse_x, mouse_y = event.pos
                
                # Rebirth button
                rebirth_button = pygame.Rect(SIRKA//2 - 100, 50, 200, 40)
                if rebirth_button.collidepoint(event.pos):
                    # Zkontroluj zda má hráč dost rebirth bodů
                    if rebirth_points >= rebirth_requirement:
                        # Reset skóre a upgradů (ale NE prestige upgradů!)
                        score = 0
                        passive_gain_level = 0
                        wall_bonus_level = 0
                        multi_base_gain_level = 0
                        rebirth_points -= rebirth_requirement
                        
                        # Zavři rebirth menu
                        rebirth_open = False
                
                # Prestige upgrade tlačítka - zobrazují se postupně (offset Y)
                upgrade_y = 150
                for upgrade_name, upgrade_info in prestige_upgrades.items():
                    # Zkontroluj zda jsou splněny prerekvizity
                    prerequisites_met = all(prestige_upgrades[prereq]["level"] > 0 for prereq in upgrade_info["prereq"])
                    
                    # Je-li splněna, je viditelná/koupitelná
                    if prerequisites_met or len(upgrade_info["prereq"]) == 0:
                        upgrade_button = pygame.Rect(SIRKA//2 - 200, upgrade_y, 400, 35)
                        if upgrade_button.collidepoint(event.pos):
                            # Spočter cenu s rebirth pointy
                            cost = upgrade_info["cost"]
                            if rebirth_points >= cost and upgrade_info["level"] < upgrade_info["max_level"]:
                                rebirth_points -= cost
                                upgrade_info["level"] += 1
                                
                                # Přepočítej prestige multiplier
                                prestige_multiplier = calculate_prestige_multiplier(prestige_upgrades)
                                
                                # Unlock Break Infinity
                                if upgrade_name == "Break Infinity" and upgrade_info["level"] == 1:
                                    break_infinity_unlocked = True
                        
                        upgrade_y += 45

    # Získání stavu kláves
    klavesa = pygame.key.get_pressed() # Zjistí stisknuté klávesy
    dx = 0
    dy = 0
    if klavesa[pygame.K_a]:
        dx = -rychlost
    if klavesa[pygame.K_d]:
        dx = rychlost
    if klavesa[pygame.K_w]:
        dy = -rychlost
    if klavesa[pygame.K_s]:
        dy = rychlost
    # Výpočet a aplikace pasivního gainu s upgrady
    # Pasivní gain funguje POUZE pokud je koupen prestige upgrade "Automation"
    if prestige_upgrades["Automation (Passive Gain)"]["level"] > 0:
        passive_gain_per_second = calculate_passive_gain_per_second(score, passive_gain_level)
        # Aplikuj prestige multiplier na pasivní příjem
        passive_gain_per_second *= prestige_multiplier
        # Aplikuj speciální pasivní gain multiplier z prestige upgradů
        passive_gain_per_second *= calculate_passive_gain_multiplier_from_prestige(prestige_upgrades)
        # Aplikuj multi base gain multiplikátor
        passive_gain_per_second *= calculate_multi_base_gain_multiplier(multi_base_gain_level)
    else:
        # Bez Automation upgradu: žádný pasivní gain!
        passive_gain_per_second = 0
    
    passive_gain_per_frame = passive_gain_per_second / 60  # 60 FPS
    score += passive_gain_per_frame

    # Pohyb všech čtverců stejným směrem podle vstupu
    to_remove = []
    initial_len = len(squares)
    for i in range(initial_len):
        sq = squares[i]
        prev = prev_colliding[i]

        # Aplikuj pohyb na základě stisknutých kláves
        sq['x'] += dx
        sq['y'] += dy

        # Omez pozici na okno (clamp) - zabrání jití čtverce mimo obrazovku
        # Zajišťuje, že čtverec zůstane v mezích 0 až SIRKA/VYSKA
        sq['x'] = max(0, min(sq['x'], SIRKA - sq['size']))
        sq['y'] = max(0, min(sq['y'], VYSKA - sq['size']))

        # Detekuj kolizi se stěnou
        now_collide = is_colliding_with_wall(sq['x'], sq['y'], sq['size'])

        # Klíčová logika: Skóre se přičítá POUZE při přechodu z ne-kolize na kolizi
        # To zabraňuje vícenásobným bodům za jednu kolizi (hrács by mohl zůstat u stěny)
        # Podmínka: (not prev) and now_collide znamená "právě jsme si kolizi všimli"
        if (not prev) and now_collide:
            # Přidej body za náraz - základní body + bonus z wall_bonus upgradu
            wall_damage = calculate_wall_bonus_damage(wall_bonus_level)
            # Aplikuj multi base gain multiplikátor na wall damage
            wall_damage *= calculate_multi_base_gain_multiplier(multi_base_gain_level)
            score += wall_damage
            # Označ čtverec k odstranění (nový se vytvoří později)
            to_remove.append(i)

        # Aktualizuj prev_colliding - pamatuj si, zda jsme nyní v kolizi
        # To je zásadní pro detekci pouze NOVÉ kolize v příštím snímku
        prev_colliding[i] = now_collide

    # Odstraň čtverce, které byly zničeny při nárazu do stěny
    # Máme seznam indexů (to_remove) čtverců, které se mají smazat
    if to_remove:
        # Vytvořit nové seznamy bez odstraněných čtverců
        new_squares_list = []
        new_prev = []
        for idx, sq in enumerate(squares):
            # Zkontroluj, zda aktuální index NENÍ v seznamu k odstranění
            if idx not in to_remove:
                new_squares_list.append(sq)
                new_prev.append(prev_colliding[idx])
        squares = new_squares_list
        prev_colliding = new_prev
        # Pokud už nejsou žádné čtverce, vytvoř nový uprostřed
        if not squares:
            squares.append({'x': start_x, 'y': start_y, 'size': velikost_ctverce})
            prev_colliding.append(False)

    # Vykreslení
    okno.fill(CERNA) # Vyčistí okno černou barvou

    # Vykreslení všech čtverců
    for sq in squares:
        pygame.draw.rect(okno, CERVENA, (sq['x'], sq['y'], sq['size'], sq['size']))

    # Zobrazení skóre a počtu čtverců + bodů za zásah + pasivní gain
    # Přepočítej pasivní gain pro zobrazení (stejně jako pro herní logiku)
    if prestige_upgrades["Automation (Passive Gain)"]["level"] > 0:
        passive_gain_display = calculate_passive_gain_per_second(score, passive_gain_level)
        passive_gain_display *= prestige_multiplier
        passive_gain_display *= calculate_passive_gain_multiplier_from_prestige(prestige_upgrades)
        passive_gain_display *= calculate_multi_base_gain_multiplier(multi_base_gain_level)
    else:
        passive_gain_display = 0
    
    # Use scientific notation automatically when `eternitynum` is enabled and value >= 1e12
    sci_threshold = 1e12
    billion_threshold = 1e9
    if eternitynum and score >= sci_threshold:
        score_str = f"{score:.2e}"
    elif score >= billion_threshold:
        score_str = f"{score:,.2f}"
    else:
        score_str = f"{score:,.2f}"
    if eternitynum and passive_gain_display >= sci_threshold:
        passive_str = f"{passive_gain_display:.2e}"
    else:
        passive_str = f"{passive_gain_display:,.2f}"
    
    # Vypočti wall damage s multiplikátorem
    wall_damage_display = calculate_wall_bonus_damage(wall_bonus_level) * calculate_multi_base_gain_multiplier(multi_base_gain_level)
    if wall_damage_display == int(wall_damage_display):
        wall_str = f"{int(wall_damage_display)}"
    else:
        wall_str = f"{wall_damage_display:.1f}"
    
    hud_text = f"Score: {score_str}    Passive/s: {passive_str}    Wall+: {wall_str}    Rebirth: {rebirth_points}    Rebirth Multi: x{prestige_multiplier:.2f}    Squares: {len(squares)}"
    text_plocha = pismo.render(hud_text, True, BILA)
    okno.blit(text_plocha, (10, VYSKA - 30))

    # Tlačítko pro settings
    pygame.draw.rect(okno, (100, 100, 100), settings_button_rect)
    settings_text = pismo.render("Settings", True, BILA)
    okno.blit(settings_text, (settings_button_rect.x + 8, settings_button_rect.y + 5))

    # Tlačítko pro shop
    pygame.draw.rect(okno, (100, 100, 100), shop_button_rect)
    btn_text = pismo.render("Upgrades", True, BILA)
    okno.blit(btn_text, (shop_button_rect.x + 8, shop_button_rect.y + 5))
    
    # Tlačítko pro rebirth
    pygame.draw.rect(okno, (150, 50, 50), rebirth_button_rect)
    rebirth_text = pismo.render("Rebirth", True, BILA)
    okno.blit(rebirth_text, (rebirth_button_rect.x + 18, rebirth_button_rect.y + 5))

    # Pokud je shop otevřený, vykreslíme upgrade tlačítka
    if shop_open:
        overlay = pygame.Surface((500, 300))
        overlay.set_alpha(220)
        overlay.fill((30, 30, 30))
        okno.blit(overlay, (SIRKA//2 - 250, VYSKA//2 - 150))
        shop_title = pismo.render("Shop - Upgrades", True, BILA)
        okno.blit(shop_title, (SIRKA//2 - 200, VYSKA//2 - 130))
        
        # Passive Gain upgrade - informační text (koupen přes Prestige)
        automation_level = prestige_upgrades["Automation (Passive Gain)"]["level"]
        if automation_level > 0:
            passive_status = f"✓ Automation Active (Prestige Lvl {automation_level})"
            passive_color = (0, 255, 0)  # Zelená - aktivní
        else:
            passive_status = "✗ Automation Locked (Buy in Prestige Tree)"
            passive_color = (255, 100, 100)  # Červená - není dostupné
        passive_label = pismo.render(passive_status, True, passive_color)
        okno.blit(passive_label, (SIRKA//2 - 240, VYSKA//2 - 70))
        
        # Wall Bonus upgrade
        wall_cost = calculate_wall_bonus_cost(wall_bonus_level)
        wall_damage = calculate_wall_bonus_damage(wall_bonus_level) * calculate_multi_base_gain_multiplier(multi_base_gain_level)
        wall_text = f"Wall Bonus (+{int(wall_damage)} pts/hit): Cost {wall_cost}pts (Lvl {wall_bonus_level})"
        if score >= wall_cost:
            wall_color = (0, 255, 0)
        else:
            wall_color = (255, 0, 0)
        wall_label = pismo.render(wall_text, True, wall_color)
        okno.blit(wall_label, (SIRKA//2 - 240, VYSKA//2 - 20))
        
        # Multi Base Gain upgrade
        multi_cost = calculate_multi_base_gain_cost(multi_base_gain_level)
        multi_mult = calculate_multi_base_gain_multiplier(multi_base_gain_level)
        multi_text = f"Multi Base Gain (x{multi_mult:.2f}): Cost {multi_cost}pts (Lvl {multi_base_gain_level})"
        if score >= multi_cost:
            multi_color = (0, 255, 0)
        else:
            multi_color = (255, 0, 0)
        multi_label = pismo.render(multi_text, True, multi_color)
        okno.blit(multi_label, (SIRKA//2 - 240, VYSKA//2 + 20))
        
        # Info text
        info_text = pismo.render("Click on upgrade to buy", True, (200, 200, 200))
        okno.blit(info_text, (SIRKA//2 - 200, VYSKA//2 + 80))
    # Pokud jsou settings otevřené, vykreslíme nastavení
    if settings_open:
        overlay = pygame.Surface((480, 220))
        overlay.set_alpha(230)
        overlay.fill((30, 30, 30))
        okno.blit(overlay, (SIRKA//2 - 240, VYSKA//2 - 110))
        settings_title = pismo.render("Settings", True, BILA)
        okno.blit(settings_title, (SIRKA//2 - 200, VYSKA//2 - 90))

        # Use smaller font for clarity
        desc = small_pismo.render("Starts at 1,000,000,000,000", True, (200, 200, 200))
        okno.blit(desc, (SIRKA//2 - 200, VYSKA//2 - 52))

        # Informational label: eternitynum is controlled in code
        state_text = "Eternitynum (code): Enabled" if eternitynum else "Eternitynum (code): Disabled"
        label = small_pismo.render(state_text, True, BILA)
        okno.blit(label, (SIRKA//2 - 200, VYSKA//2 - 30))

        # No interactive toggle here; the behavior is controlled by `eternitynum` in the source.

    # Pokud je rebirth menu otevřené, vykreslíme upgrade tree
    if rebirth_open:
        overlay = pygame.Surface((1000, 750))
        overlay.set_alpha(230)
        overlay.fill((30, 30, 30))
        okno.blit(overlay, (SIRKA//2 - 500, VYSKA//2 - 300))
        
        rebirth_title = pismo.render("Prestige - Ultimate Upgrade Tree", True, BILA)
        okno.blit(rebirth_title, (SIRKA//2 - 150, VYSKA//2 - 275))
        
        # Rebirth button
        rebirth_button = pygame.Rect(SIRKA//2 - 100, VYSKA//2 - 235, 200, 40)
        needed_rebirth = max(0, rebirth_requirement - rebirth_points)
        pygame.draw.rect(okno, (100, 50, 50), rebirth_button)
        if needed_rebirth > 0:
            rebirth_btn_text = pismo.render(f"REBIRTH ({needed_rebirth} more)", True, BILA)
        else:
            rebirth_btn_text = pismo.render(f"REBIRTH Ready!", True, (0, 255, 0))
        okno.blit(rebirth_btn_text, (rebirth_button.x + 10, rebirth_button.y + 8))
        
        # Upgrade tree positions - malá tlačítka v tree struktuře
        button_width = 130
        button_height = 40
        
        upgrade_positions = {
            # TIER 1 - Basis (horní řada)
            "Automation (Passive Gain)": (SIRKA//2 - 250, VYSKA//2 - 135),
            "Score Booster": (SIRKA//2 - 70, VYSKA//2 - 175),
            "Point Multiplier": (SIRKA//2 + 110, VYSKA//2 - 135),
            
            # TIER 2 - Mid-game (druhá řada)
            "Passive Amplifier": (SIRKA//2 - 250, VYSKA//2 - 65),
            "Efficiency Boost": (SIRKA//2 - 70, VYSKA//2 - 105),
            "Greater Infinity I": (SIRKA//2 + 110, VYSKA//2 - 65),
            
            # TIER 3 - Advanced (třetí řada)
            "Super Charge": (SIRKA//2 - 180, VYSKA//2 + 10),
            "Infinity Engine": (SIRKA//2 - 40, VYSKA//2 - 30),
            "Quantum Leap": (SIRKA//2 + 110, VYSKA//2 + 10),
            
            # TIER 4 - Elite (čtvrtá řada)
            "Break Infinity": (SIRKA//2 - 180, VYSKA//2 + 85),
            "Ultimate Power": (SIRKA//2 - 40, VYSKA//2 + 45),
            "Rebirth Mastery": (SIRKA//2 + 110, VYSKA//2 + 85),
            
            # ALTERNATIVE PATH (spodní větev)
            "Speed Demon": (SIRKA//2 - 250, VYSKA//2 + 160),
            "Wealth Generator": (SIRKA//2 - 70, VYSKA//2 + 120),
            "Time Warp": (SIRKA//2 + 110, VYSKA//2 + 160)
        }
        
        # Nejdříve vykreslíme čáry mezi upgradama (prerekvizity)
        for upgrade_name, upgrade_info in prestige_upgrades.items():
            if upgrade_name in upgrade_positions and upgrade_info["prereq"]:
                from_x, from_y = upgrade_positions[upgrade_name]
                from_center = (from_x + button_width // 2, from_y + button_height // 2)
                
                # Nakresli čáru k všem prerequisitům
                for prereq in upgrade_info["prereq"]:
                    if prereq in upgrade_positions:
                        to_x, to_y = upgrade_positions[prereq]
                        to_center = (to_x + button_width // 2, to_y + button_height // 2)
                        
                        # Čára v bílé barvě s nižší opacitou - začíná od spodku prereq, končí na vrchu aktuálního
                        line_color = (150, 150, 150)
                        pygame.draw.line(okno, line_color, to_center, from_center, 2)
        
        # Pak vykreslíme tlačítka upgradů
        for upgrade_name, upgrade_info in prestige_upgrades.items():
            if upgrade_name in upgrade_positions:
                pos_x, pos_y = upgrade_positions[upgrade_name]
                
                # Zkontroluj prerekvizity
                prerequisites_met = all(prestige_upgrades[prereq]["level"] > 0 for prereq in upgrade_info["prereq"])
                is_available = prerequisites_met or len(upgrade_info["prereq"]) == 0
                
                upgrade_rect = pygame.Rect(pos_x, pos_y, button_width, button_height)
                cost = upgrade_info["cost"]
                level = upgrade_info["level"]
                max_level = upgrade_info["max_level"]
                
                if is_available:
                    # Barva podle dostupnosti
                    if rebirth_points >= cost and level < max_level:
                        button_color = (50, 150, 50)  # Zelená - koupitelné
                    elif level >= max_level:
                        button_color = (100, 100, 100)  # Šedá - maxed
                    else:
                        button_color = (100, 50, 50)  # Červená - nemůžete si koupit
                else:
                    button_color = (40, 40, 40)  # Černá - locked
                
                # Tlačítko
                pygame.draw.rect(okno, button_color, upgrade_rect)
                pygame.draw.rect(okno, (200, 200, 200), upgrade_rect, 1)  # Border
                
                # Text - celý název a level
                if level >= max_level:
                    status_text = "MAX"
                else:
                    status_text = f"L{level}"
                
                # Vykresli text - název a level
                name_line = tiny_pismo.render(upgrade_name, True, BILA)
                level_line = tiny_pismo.render(status_text, True, (200, 200, 200))
                
                okno.blit(name_line, (upgrade_rect.x + 5, upgrade_rect.y + 5))
                okno.blit(level_line, (upgrade_rect.x + 5, upgrade_rect.y + 22))
        
        # Přidej info text s rebirth pointy a multiplikátorem
        info_text = small_pismo.render(f"Rebirth Points: {rebirth_points}    Multiplier: x{prestige_multiplier:.2f}", True, (200, 200, 200))
        okno.blit(info_text, (SIRKA//2 - 480, VYSKA//2 + 300))

    # Aktualizace displeje
    pygame.display.flip() # Zobrazí změny na obrazovce

    # Omezení FPS
    hodiny.tick(60) # Omezí rychlost na 60 FPS

pygame.quit() # Ukončí Pygame
sys.exit() # Ukončí program