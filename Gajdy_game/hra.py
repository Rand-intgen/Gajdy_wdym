import pygame # Importuje knihovnu Pygame
import sys # Importuje systémový modul
import random
import os

# Nejostřejší škálování (bez rozmazani písma ve fullscreenu)
os.environ['SDL_RENDER_SCALE_QUALITY'] = '0'

# Inicializace Pygame
pygame.init() # Inicializuje Pygame

# Nastavení okna
SIRKA = 1560 # Šířka herního okna
VYSKA = 960  # Výška herního okna
okno = pygame.display.set_mode((SIRKA, VYSKA)) # Windowed 1280x720
game_surf = pygame.Surface((SIRKA, VYSKA)) # Herní plocha (rendering sem, pak scale na okno)

pygame.display.set_caption("Gajdy_wdym - Point incremental") # Nastaví titulek okna

# Barvy
CERNA = (0, 0, 0) # Definuje černou barvu
BILA = (255, 255, 255) # Definuje bílou barvu
CERVENA = (255, 0, 0) # Definuje červenou barvu

# Nastavení objektu (čtverec)
velikost_ctverce = 75 # Nastaví velikost čtverce
start_x = SIRKA // 2 - velikost_ctverce // 2 # Vycentruje X souřadnici
start_y = VYSKA // 2 - velikost_ctverce // 2 # Vycentruje Y souřadnici
rychlost = 7 # Nastaví rychlost pohybu

# Seznam čtverců (každý čtverec je slovník s pozicí a velikostí)
squares = [{'x': start_x, 'y': start_y, 'size': velikost_ctverce}]
# Track previous-collision state per square, aby se skóre přičetlo jen jednou při nárazu
prev_colliding = [False]

# Skóre
score = 0

# Nastavení písma pro zobrazení souřadnic a skóre
pismo = pygame.font.SysFont("Segoe UI", 24, bold=True) # Modernější, robustnější hlavní písmo
menu_pismo = pygame.font.SysFont("Segoe UI", 16, bold=True) # Speciálně pro tlačítka v horním menu
# Menší písmo pro settings popisky
small_pismo = pygame.font.SysFont("Segoe UI", 14) # Zmenšeno (Segoe UI je širší)
# Velmi malé písmo pro upgrade tree tlačítka
tiny_pismo = pygame.font.SysFont("Segoe UI", 9) # Zmenšeno na 9, aby se dlouhé texty vlezly do 140px

# Hlavní smyčka
bezi = True # Nastaví pro smyčku
hodiny = pygame.time.Clock() # Vytvoří hodiny pro řízení FPS

# Seznam pro poletující texty
floating_texts = []

# Seznam pro částice (particles) při nárazu
particles = []

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
rebirth_points = 0  # Měna pro rebirth strom - kumuluje se a resetuje skóre/upgrady
prestige_points = 0  # Počet prestiží (Milestones)
quarks = 0           # Měna získaná z Prestige pro nákup prvků
prestige_multiplier = 1.0  # Bonusový multiplikátor skóre z rebirth stromu
break_infinity_unlocked = False  # Zda je odemknut Break Infinity upgrade

prestige_menu_open = False
prestige_btn_rect = pygame.Rect(SIRKA - 440, 10, 100, 30)
prestige_requirement = 100000  # Kolik rebirth bodů je potřeba na Prestige

# Periodic Table systém
periodic_table_open = False
periodic_btn_rect = pygame.Rect(SIRKA - 550, 10, 100, 30)
# Všechny odemčené/dostupné prvky. "cost" v Quarks.
elements_db = {
    "H": {"cost": 1, "name": "Hydrogen", "symbol": "H", "desc": "Základní boost pasivního skóre z aktuálních Rebirth bodů."},
    "He": {"cost": 2, "name": "Helium", "symbol": "He", "desc": "Boostuje globální násobič z logaritmu skóre."},
    "Li": {"cost": 3, "name": "Lithium", "symbol": "Li", "desc": "Boostuje wall damage úměrně počtu prestiží."},
    "Be": {"cost": 5, "name": "Beryllium", "symbol": "Be", "desc": "Zvyšuje pasivní příjem na základě zakoupených upgradů."},
    "B": {"cost": 8, "name": "Boron", "symbol": "B", "desc": "Zrychluje tick-speed podle aktuálního zisku z wall damage."},
    "C": {"cost": 13, "name": "Carbon", "symbol": "C", "desc": "Logaritmický násobič Score i Rebirth bodů dohromady."},
    "N": {"cost": 21, "name": "Nitrogen", "symbol": "N", "desc": "Exponenciální nárůst pasivního zisku (menší exponent)."},
    "O": {"cost": 34, "name": "Oxygen", "symbol": "O", "desc": "Dvojnásobně zesiluje efekt prvků H-N."},
    "F": {"cost": 55, "name": "Fluorine", "symbol": "F", "desc": "Každý odemčený element přidá globální 2x boost."},
    "Ne": {"cost": 83, "name": "Neon", "symbol": "Ne", "desc": "Zářící neonová aura: Trvale x10 na vše."},
    "Na": {"cost": 146, "name": "Sodium", "symbol": "Na", "desc": "Globální multiplikátor x5."},
    "Mg": {"cost": 233, "name": "Magnesium", "symbol": "Mg", "desc": "Pasivní gain x5."},
    "Al": {"cost": 377, "name": "Aluminum", "symbol": "Al", "desc": "Wall damage x5."},
    "Si": {"cost": 610, "name": "Silicon", "symbol": "Si", "desc": "Pasivní boost z počtu Quarků."},
    "P": {"cost": 987, "name": "Phosphorus", "symbol": "P", "desc": "Rebirth body x2."},
    "S": {"cost": 1597, "name": "Sulfur", "symbol": "S", "desc": "Skóre boostované prestižemi."},
    "Cl": {"cost": 2584, "name": "Chlorine", "symbol": "Cl", "desc": "Pasivní a wall x10."},
    "Ar": {"cost": 4181, "name": "Argon", "symbol": "Ar", "desc": "Další x2 násobič na dřívější prvky."},
    "K": {"cost": 6765, "name": "Potassium", "symbol": "K", "desc": "Globální skóre x25."},
    "Ca": {"cost": 10946, "name": "Calcium", "symbol": "Ca", "desc": "Ultimátní boost: x100 na všechno."},
    "Sc": {"cost": 15000, "name": "Scandium", "symbol": "Sc", "desc": "Základní skóre ze zdi x2."},
    "Ti": {"cost": 22000, "name": "Titanium", "symbol": "Ti", "desc": "Pasivní gain x2."},
    "V": {"cost": 32000, "name": "Vanadium", "symbol": "V", "desc": "Rebirth body x3."},
    "Cr": {"cost": 48000, "name": "Chromium", "symbol": "Cr", "desc": "Skóre po prestiži x5."},
    "Mn": {"cost": 70000, "name": "Manganese", "symbol": "Mn", "desc": "Globální skóre x10."},
    "Fe": {"cost": 100000, "name": "Iron", "symbol": "Fe", "desc": "Pasivní a zeď x5."},
    "Co": {"cost": 150000, "name": "Cobalt", "symbol": "Co", "desc": "Rebirth body x5."},
    "Ni": {"cost": 220000, "name": "Nickel", "symbol": "Ni", "desc": "Každý odemčený element přidá globální 1.5x boost."},
    "Cu": {"cost": 320000, "name": "Copper", "symbol": "Cu", "desc": "Zvyšuje pasivní příjem na základě počtu Quarků."},
    "Zn": {"cost": 480000, "name": "Zinc", "symbol": "Zn", "desc": "Globální multiplikátor x15."},
    "Ga": {"cost": 700000, "name": "Gallium", "symbol": "Ga", "desc": "Pasivní gain x25."},
    "Ge": {"cost": 1000000, "name": "Germanium", "symbol": "Ge", "desc": "Další x2 násobič na dřívější prvky."},
    "As": {"cost": 1500000, "name": "Arsenic", "symbol": "As", "desc": "Zeď damage x50."},
    "Se": {"cost": 2200000, "name": "Selenium", "symbol": "Se", "desc": "Rebirth body x25."},
    "Br": {"cost": 6942067, "name": "Bromine", "symbol": "Br", "desc": "Ultimátní endgame boost: x500 na všechno."}
}
# Pozice prvků na skutečné periodické tabulce (row, col) - max 18 sloupců
PT_COORDS = {
    "H": (0, 0), "He": (0, 17),
    "Li": (1, 0), "Be": (1, 1),
    "B": (1, 12), "C": (1, 13), "N": (1, 14), "O": (1, 15), "F": (1, 16), "Ne": (1, 17),
    "Na": (2, 0), "Mg": (2, 1),
    "Al": (2, 12), "Si": (2, 13), "P": (2, 14), "S": (2, 15), "Cl": (2, 16), "Ar": (2, 17),
    "K": (3, 0), "Ca": (3, 1), "Sc": (3, 2), "Ti": (3, 3), "V": (3, 4), "Cr": (3, 5), "Mn": (3, 6), "Fe": (3, 7), "Co": (3, 8), "Ni": (3, 9), "Cu": (3, 10), "Zn": (3, 11), "Ga": (3, 12), "Ge": (3, 13), "As": (3, 14), "Se": (3, 15), "Br": (3, 16)
}
# Status vlastnění prvků - ukládáme jako slovník True/False
elements_unlocked = {sym: False for sym in elements_db}

def get_milestone_multipliers():
    """Vrací bonusy podle počtu prestiží: rebirth_mult, passive_mult, global_mult, start_score, start_wall"""
    m_rebirth = 1
    m_passive = 1
    m_global = 1
    start_score = 0
    start_wall = 0
    
    if prestige_points >= 1:
        start_wall += 50
    if prestige_points >= 2:
        m_rebirth *= 5
    if prestige_points >= 3:
        m_passive *= 10
    if prestige_points >= 4:
        start_score += 1000000
    if prestige_points >= 5:
        m_global *= 100
    if prestige_points >= 6:
        m_rebirth *= 10
    if prestige_points >= 7:
        m_passive *= 100
    if prestige_points >= 8:
        start_wall += 1000
    if prestige_points >= 10:
        start_score += 1000000000
    if prestige_points >= 12:
        m_global *= 10000
    if prestige_points >= 15:
        m_rebirth *= 100
        
    return m_rebirth, m_passive, m_global, start_score, start_wall

def calculate_elements_multipliers(current_score, rebirth_pts, upgrades=None):
    """Vrací čtveřici multiplikátorů z odemčených prvků: (m_passive, m_global, m_wall, m_rebirth).
    Tento boost se dynamicky počítá z měn a odemčených prvků každou chvíli.
    """
    import math
    em_passive = 1.0
    em_global = 1.0
    em_wall = 1.0
    em_rebirth = 1.0
    
    # Kaskádové bonusy z těžších prvků
    oxygen_bonus = 2.0 if elements_unlocked["O"] else 1.0
    argon_bonus = 2.0 if elements_unlocked["Ar"] else 1.0
    total_bonus = oxygen_bonus * argon_bonus
    
    # H: Pasivní skóre z aktuálních Rebirth bodů
    if elements_unlocked["H"]:
        # log10 z rebirth bodů, s mírným offsetem a omezeným skalováním
        h_boost = 1.0 + (math.log10(max(rebirth_pts + 1, 10)) * 0.5)
        em_passive *= (h_boost * total_bonus)
        
    # He: Globální skóre z logaritmu celkového skóre
    if elements_unlocked["He"]:
        he_boost = 1.0 + (math.log10(max(current_score + 1, 10)) * 0.3)
        em_global *= (he_boost * total_bonus)
        
    # Li: Wall damage podle počtu prestiží
    if elements_unlocked["Li"]:
        li_boost = 1.0 + (prestige_points * 2.5)
        em_wall *= (li_boost * total_bonus)
        
    # Be: Zvyšuje pasivní příjem na základě levelu zakoupených upgradů z Prestige Tree
    if elements_unlocked["Be"]:
        total_upgrade_levels = sum(u["level"] for u in prestige_upgrades.values()) if upgrades else 0
        be_boost = 1.0 + (total_upgrade_levels * 0.1)
        em_passive *= (be_boost * total_bonus)
        
    # B: Tik-speed (aplikován převážně na wall damage / pasiv)
    if elements_unlocked["B"]:
        em_passive *= (1.5 * total_bonus)
        
    # C: Skóre i Rebirth bodů boost z celkové logaritmické báze
    if elements_unlocked["C"]:
        combined = rebirth_pts + current_score
        c_boost = 1.0 + (math.log10(max(combined + 1, 10)) * 0.8)
        em_global *= (c_boost * total_bonus)
        
    # N: Exponenciální (menší nárůst) pasivního zisku
    if elements_unlocked["N"]:
        em_passive *= (5.0 * total_bonus)
        
    # F: Každý odemčený prvek * 2 globálně
    if elements_unlocked["F"]:
        unlocked_count = sum(1 for v in elements_unlocked.values() if v)
        f_boost = 2.0 ** unlocked_count
        em_global *= f_boost # Nenásobíme oxygen_bonus, Fluorine má plošný hard multiplier
        
    # Ne: Trvale x10 na všechno
    if elements_unlocked["Ne"]:
        em_passive *= (10.0 * total_bonus)
        em_global *= (10.0 * total_bonus)
        em_wall *= (10.0 * total_bonus)

    # Na: Globální multiplikátor x5
    if elements_unlocked["Na"]:
        em_global *= (5.0 * argon_bonus)

    # Mg: Pasivní gain x5
    if elements_unlocked["Mg"]:
        em_passive *= (5.0 * argon_bonus)

    # Al: Wall damage x5
    if elements_unlocked["Al"]:
        em_wall *= (4.9 * argon_bonus)

    # Si: Pasivní boost z Quarků
    if elements_unlocked["Si"]:
        si_boost = 1.0 + (math.log10(max(quarks + 1, 10)) * 2)
        em_passive *= (si_boost * argon_bonus)

    # P: Rebirth body x2
    if elements_unlocked["P"]:
        em_rebirth *= (2.0 * argon_bonus)

    # S: Skóre boostované prestižemi
    if elements_unlocked["S"]:
        s_boost = 1.0 + (prestige_points * 0.5)
        em_global *= (s_boost * argon_bonus)

    # Cl: Pasivní a wall x10
    if elements_unlocked["Cl"]:
        em_passive *= (10.0 * argon_bonus)
        em_wall *= (10.0 * argon_bonus)

    # K: Globální skóre x25
    if elements_unlocked["K"]:
        em_global *= 25.0

    # Ca: x100 na všechno
    if elements_unlocked["Ca"]:
        em_passive *= 100.0
        em_global *= 100.0
        em_wall *= 100.0
        em_rebirth *= 100.0
        
    # Kaskádové bonusy pro nové prvky
    ge_bonus = 2.0 if elements_unlocked["Ge"] else 1.0
    
    if elements_unlocked["Sc"]:
        em_wall *= (2.0 * ge_bonus)
    if elements_unlocked["Ti"]:
        em_passive *= (2.0 * ge_bonus)
    if elements_unlocked["V"]:
        em_rebirth *= (3.0 * ge_bonus)
    if elements_unlocked["Cr"]:
        em_global *= (5.0 * ge_bonus)
    if elements_unlocked["Mn"]:
        em_global *= (10.0 * ge_bonus)
    if elements_unlocked["Fe"]:
        em_passive *= (5.0 * ge_bonus)
        em_wall *= (5.0 * ge_bonus)
    if elements_unlocked["Co"]:
        em_rebirth *= (5.0 * ge_bonus)
    if elements_unlocked["Ni"]:
        unlocked_count2 = sum(1 for v in elements_unlocked.values() if v)
        ni_boost = 1.5 ** unlocked_count2
        em_global *= ni_boost
    if elements_unlocked["Cu"]:
        import math
        cu_boost = 1.0 + (math.log10(max(quarks + 1, 10)) * 5)
        em_passive *= (cu_boost * ge_bonus)
    if elements_unlocked["Zn"]:
        em_global *= (15.0 * ge_bonus)
    if elements_unlocked["Ga"]:
        em_passive *= (25.0 * ge_bonus)
    # Ge bonus se aplikuje výše
    if elements_unlocked["As"]:
        em_wall *= (50.0 * ge_bonus)
    if elements_unlocked["Se"]:
        em_rebirth *= (25.0 * ge_bonus)
    if elements_unlocked["Br"]:
        em_passive *= 500.0
        em_global *= 500.0
        em_wall *= 500.0
        em_rebirth *= 500.0
        
    return em_passive, em_global, em_wall, em_rebirth
# Prestige Upgrade Tree - komplexní systém inspirovaný The Ultimate Upgrade Tree
prestige_upgrades = {
    # Základní upgrady (Tier 1)
    "Automation (Passive Gain)": {"cost": 8,     "prereq": ["Score Booster"], "unlocked": False, "level": 0, "max_level": 20},
    "Score Booster":             {"cost": 5,     "prereq": [], "unlocked": False, "level": 0, "max_level": 15},
    "Point Multiplier":          {"cost": 10,    "prereq": ["Score Booster"], "unlocked": False, "level": 0, "max_level": 10},
    # Quark gain větev
    "Quark Extractor":           {"cost": 50,    "prereq": ["Point Multiplier"], "unlocked": False, "level": 0, "max_level": 10},
    "Quark Collector":           {"cost": 200,   "prereq": ["Quark Extractor"], "unlocked": False, "level": 0, "max_level": 8},
    "Quark Generator":           {"cost": 750,   "prereq": ["Quark Collector"], "unlocked": False, "level": 0, "max_level": 5},
    # Self-boost větev - Points boost themselves
    "Score Momentum":            {"cost": 12,    "prereq": ["Score Booster"], "unlocked": False, "level": 0, "max_level": 10},
    "Momentum Amplifier":        {"cost": 35,    "prereq": ["Score Momentum"], "unlocked": False, "level": 0, "max_level": 7},

    # Mid-game upgrady (Tier 2)
    "Passive Amplifier":         {"cost": 20,    "prereq": ["Automation (Passive Gain)"], "unlocked": False, "level": 0, "max_level": 12},
    "Efficiency Boost":          {"cost": 15,    "prereq": ["Point Multiplier"], "unlocked": False, "level": 0, "max_level": 15},
    "Greater Infinity I":        {"cost": 25,    "prereq": ["Automation (Passive Gain)"], "unlocked": False, "level": 0, "max_level": 8},

    # Pokročilé upgrady (Tier 3) - ceny 800-3000 rebirth bodů
    "Super Charge":              {"cost": 800,   "prereq": ["Passive Amplifier", "Efficiency Boost"], "unlocked": False, "level": 0, "max_level": 10},
    "Infinity Engine":           {"cost": 1500,  "prereq": ["Greater Infinity I"], "unlocked": False, "level": 0, "max_level": 6},
    "Quantum Leap":              {"cost": 3000,  "prereq": ["Super Charge"], "unlocked": False, "level": 0, "max_level": 5},

    # Elite upgrady (Tier 4) - endgame (10k-50k)
    "Break Infinity":            {"cost": 25000, "prereq": ["Infinity Engine", "Quantum Leap"], "unlocked": False, "level": 0, "max_level": 1},
    "Ultimate Power":            {"cost": 10000, "prereq": ["Quantum Leap"], "unlocked": False, "level": 0, "max_level": 3},
    "Rebirth Mastery":           {"cost": 50009, "prereq": ["Break Infinity"], "unlocked": False, "level": 0, "max_level": 1},

    # Alternativní větve - LEVO (ekonomické)
    "Speed Demon":               {"cost": 30,    "prereq": ["Efficiency Boost"], "unlocked": False, "level": 0, "max_level": 8},
    "Wealth Generator":          {"cost": 45,    "prereq": ["Speed Demon"], "unlocked": False, "level": 0, "max_level": 6},
    "Time Warp":                 {"cost": 80,    "prereq": ["Wealth Generator"], "unlocked": False, "level": 0, "max_level": 4},

    # Alternativní větve - PRAVO (tick speed) - ceny 1k-15k
    "Tick Booster":              {"cost": 1000,  "prereq": ["Automation (Passive Gain)"], "unlocked": False, "level": 0, "max_level": 10},
    "Rapid Tick":                {"cost": 5000,  "prereq": ["Tick Booster"], "unlocked": False, "level": 0, "max_level": 8},
    "Time Accelerator":          {"cost": 15000, "prereq": ["Rapid Tick"], "unlocked": False, "level": 0, "max_level": 5},
}


# Upgrade systém
passive_gain_level = 0  # Úroveň passive gain upgradu
wall_bonus_level = 0  # Úroveň wall bonus upgradu
multi_base_gain_level = 0  # Úroveň multi base gain upgradu (násobí pasivní gain)
rebirth_requirement = 10000  # Kolik skóre je potřeba na rebirth

def calculate_passive_gain_cost(level):
    """Vypočítá cenu pro nákup passive gain upgradu.
    
    Exponenciální růst ceny: 10 * 1.5^level
    - Cena se zvyšuje s každou novou úrovní
    - Cíl: Kontrolovat inflaci dostatečně vysokými cenami
    - Př: level 0 = 10 bodů, level 5 = 76 bodů, level 10 = 576 bodů
    """
    return int(10 * (1.45 ** level))

def calculate_wall_bonus_cost(level):
    """Vypočítá cenu pro nákup wall bonus upgradu.
    
    Exponenciální růst ceny: 5 * 1.4^level
    - Pomalejší růst než Passive Gain (1.4 vs 1.5)
    - Více dostupné pro hráče začátečníky
    - Př: level 0 = 5 bodů, level 10 = 56 bodů, level 20 = 628 bodů
    """
    return int(5 * (1.5 ** level))

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
    _, _, _, _, start_wall = get_milestone_multipliers()
    return (1 + level) * (1.9 ** (level // 5)) + start_wall

def calculate_passive_gain_per_second(current_score, level):
    """Vypočítá pasivní gain za sekundu na základě aktuálního skóre a úrovně upgradu.
    
    Vzorec: (score/100)^0.6 × 0.005 × (1.2^level) × (8^(level//10))
    
    Poznámka: Aktivace je řízena prestige upgrade "Automation (Passive Gain)"
    
    Komponenty výpočtu:
    1. Základní část: (score/100)^0.6 - vychází z aktuálního skóre
       - Exponent 0.6 znamená pomalejší růst (sublineární)
       - Brání příliš rychlému zdvojnásobení příjmu
    
    2. Koeficient: 0.005
       - Záměrně velmi malý, aby automation byl na začátku slabý
       - Styl inspirovaný incremental hrami (postupný růst)
    
    3. Upgrade multiplier: 1.2^level
       - Každá úroveň zvýší příjem o 20%
       - Motivuje hráče k nákupům upgradů
    
    4. Mega multiplier: 8^(level//10)
       - Každých 10 levelů se efekt znásobí 8x
       - Umožňuje dosáhnout extrémních čísel (1e60+) ve vysokých levelech
    """
    # Základní gain z aktuálního skóre
    # Exponent 0.6 zajišťuje, že pasivní příjem je pomalejší než exponenciální
    multiplier = (current_score / 100) ** 0.6
    base_gain = multiplier * 0.005  # Velmi slabý základ - silnější jen ve vysokých levelech

    # Upgrade level multiplier - lineárně na exponenciální stupnici
    upgrade_multiplier = (1.2 ** level)

    # Mega-multiplier - dramatické zvýšení každých 10 levelů (8x silnější než verze 5x)
    mega_multiplier = (8 ** (level // 10))

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

    Vzorec: sqrt(score / 1000)
    - Na začátku dává málo bodů (slabý skór = málo rebirth bodů)
    - Škáluje smysluplně s rostoucím skórem
    - Rebirth body se NIKDY neresetují, kumulují se

    Příklady:
      score = 1 000       →    1 rebirth bod
      score = 100 000     →   10 rebirth bodů
      score = 10 000 000  →  100 rebirth bodů
      score = 1e12        → 1 000 000 rebirth bodů
    """
    if current_score < 10000:
        return 0
    import math
    base = int(math.sqrt(current_score / 1000))
    m_rebirth, _, _, _, _ = get_milestone_multipliers()
    _, _, _, em_rebirth = calculate_elements_multipliers(current_score, rebirth_points, prestige_upgrades)
    return int(base * m_rebirth * em_rebirth)

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
    if "Rebirth Mastery" in prestige_upgrades:
        multiplier *= (5.0 ** prestige_upgrades["Rebirth Mastery"]["level"])
    
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
    
    - Automation: +20% za level (základní efekt pro pasivní gain)
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
        multiplier *= (1.20 ** prestige_upgrades["Automation (Passive Gain)"]["level"])
    
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
    
    # Elite efekty
    if "Rebirth Mastery" in prestige_upgrades:
        multiplier *= (5.0 ** prestige_upgrades["Rebirth Mastery"]["level"])
    
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

def calculate_tick_speed_multiplier(prestige_upgrades):
    """Vypočítá multiplikátor rychlosti ticků z alternativních pravých upgradů.

    Každý level tick-speed upgradu přidává +15% pasivního pří­mu.
    Celkový efekt: 1.15 ^ (součet všech tick levelů)
    """
    tick_levels = 0
    for name in ["Tick Booster", "Rapid Tick", "Time Accelerator"]:
        if name in prestige_upgrades:
            tick_levels += prestige_upgrades[name]["level"]
    return 1.15 ** tick_levels

def calculate_score_self_boost(current_score, prestige_upgrades):
    """Vypočítá self-boost skoru za sekundu (body boosí samy sebe).

    Vzorec: log10(score+1) * 0.0005 * momentum_lvl * (1.15^momentum_lvl) * (1.3^amplifier_lvl)
    - Logaritmické škálování - silnější při vyšším skóru ale ne příliš OP
    - Motivuje ké držení skoru před rebirthem
    - Odemkne se nákupem Score Momentum z Prestige Tree
    """
    momentum_lvl = prestige_upgrades.get("Score Momentum", {}).get("level", 0)
    amplifier_lvl = prestige_upgrades.get("Momentum Amplifier", {}).get("level", 0)
    if momentum_lvl == 0:
        return 0.0
    import math
    log_base = math.log10(max(current_score + 1, 10))
    boost = log_base * 0.002 * momentum_lvl * (1.15 ** momentum_lvl) * (1.3 ** amplifier_lvl)
    return boost

# === UPGRADE TREE LAYOUT - konstanty pro pozice a barvy ===
_UPG_BW = 140  # šířka uzlu
_UPG_BH = 42   # výška uzlu
_cx = SIRKA // 2  # střed obrazovky X

# Barvy uzlů podle tieru (inspirováno ultimátním upgrade stromem)
TIER_COLORS = {
    "Tier1": (220, 200, 0),    # Žlutá  - základní upgrady
    "Tier2": (0, 200, 80),     # Zelená - mid-game
    "Tier3": (0, 200, 220),    # Azurová - pokročilé
    "Tier4": (220, 50, 50),    # Červená - Elite
    "Alt":   (180, 50, 200),   # Fialová - levá alternativní větev
    "Tick":  (220, 130, 0),    # Orůžová - pravá tick-speed větev
}

# Přiřazení každého upgradu k tieru
UPGRADE_TIERS = {
    "Automation (Passive Gain)": "Tier1",
    "Score Booster":             "Tier1",
    "Point Multiplier":          "Tier1",
    "Passive Amplifier":         "Tier2",
    "Efficiency Boost":          "Tier2",
    "Greater Infinity I":        "Tier2",
    "Super Charge":              "Tier3",
    "Infinity Engine":           "Tier3",
    "Quantum Leap":              "Tier3",
    "Break Infinity":            "Tier4",
    "Ultimate Power":            "Tier4",
    "Rebirth Mastery":           "Tier4",
    "Speed Demon":               "Alt",
    "Wealth Generator":          "Alt",
    "Time Warp":                 "Alt",
    # Self-boost větev (pod Score Boosterem) - stejný tier jako Tier1
    "Score Momentum":            "Tier1",
    "Momentum Amplifier":        "Tier1",
    # Quark větev
    "Quark Extractor":           "Alt",
    "Quark Collector":           "Alt",
    "Quark Generator":           "Alt",
    # Tick-speed větev (pravá strana) - orůžová barva
    "Tick Booster":              "Tick",
    "Rapid Tick":                "Tick",
    "Time Accelerator":          "Tick",
}

# Pozice každého uzlu v prestige stromě (levý horní roh)
UPGRADE_POSITIONS = {
    # TIER 1 - ROOT (Úplně nahoře uprostřed)
    "Score Booster":             (_cx +   0 - 70,  120),
    
    # SELF-BOOST větev (Přímo pod Score Boosterem)
    "Score Momentum":            (_cx +   0 - 70,  210),
    "Momentum Amplifier":        (_cx +   0 - 70,  300),

    # TIER 1 - Ostatní větve (Point Multiplier nalevo, Automation napravo)
    "Point Multiplier":          (_cx - 300 - 70,  210),
    "Automation (Passive Gain)": (_cx + 300 - 70,  210),

    # QUARK větev (Pod Point Multiplierem směřující blíž ke středu)
    "Quark Extractor":           (_cx - 150 - 70,  210),
    "Quark Collector":           (_cx - 150 - 70,  300),
    "Quark Generator":           (_cx - 150 - 70,  390),

    # TIER 2 a přidružené středové uzly
    "Efficiency Boost":          (_cx - 300 - 70,  300),
    "Passive Amplifier":         (_cx + 150 - 70,  300),
    "Greater Infinity I":        (_cx + 300 - 70,  390), 
    
    # TIER 3 - pokročilé 
    "Super Charge":              (_cx +   0 - 70,  390),
    "Quantum Leap":              (_cx - 150 - 70,  480),
    "Infinity Engine":           (_cx + 150 - 70,  480),

    # TIER 4 - elite
    "Ultimate Power":            (_cx - 150 - 70,  570),
    "Break Infinity":            (_cx +   0 - 70,  570),
    "Rebirth Mastery":           (_cx +   0 - 70,  660),

    # ALTERNATIVNÍ větev LEVO (ekonomické, z Efficiency Boost)
    "Speed Demon":               (_cx - 500 - 70,  390),
    "Wealth Generator":          (_cx - 500 - 70,  480),
    "Time Warp":                 (_cx - 500 - 70,  570),

    # ALTERNATIVNÍ větev PRAVO (tick-speed, z Automation)
    "Tick Booster":              (_cx + 500 - 70,  390),
    "Rapid Tick":                (_cx + 500 - 70,  480),
    "Time Accelerator":          (_cx + 500 - 70,  570),
}

# Popis efektu každého upgradu (zobrazuje se jako tooltip při najetí myší)
UPGRADE_EFFECTS = {
    "Score Booster":             "+5% skóre za level (1.05^lvl)",
    "Automation (Passive Gain)": "Odemkne pasivní příjem bodů/s",
    "Point Multiplier":          "+8% skóre za level (1.08^lvl)",
    "Quark Extractor":           "+20% Quarků z prestiže/level",
    "Quark Collector":           "+30% Quarků z prestiže/level",
    "Quark Generator":           "+50% Quarků z prestiže/level",
    "Score Momentum":            "log10(score)*0.002*lvl boost/s",
    "Momentum Amplifier":        "x1.3^lvl na Score Momentum",
    "Passive Amplifier":         "+10% pasivní příjem za level",
    "Efficiency Boost":          "+6% skóre za level (1.06^lvl)",
    "Greater Infinity I":        "+10% skóre za level (1.10^lvl)",
    "Super Charge":              "+12% skóre i passiv za level",
    "Infinity Engine":           "+15% skóre, +8% passiv/lvl",
    "Quantum Leap":              "+20% skóre, +15% passiv/lvl",
    "Break Infinity":            "Odemkne Break Infinity notaci",
    "Ultimate Power":            "+25% skóre za level (1.25^lvl)",
    "Rebirth Mastery":           "x5 globální skóre a pasiv",
    "Speed Demon":               "+7% skóre za level (1.07^lvl)",
    "Wealth Generator":          "+18% skóre za level (1.18^lvl)",
    "Time Warp":                 "+30% skóre za level (1.30^lvl)",
    "Tick Booster":              "+15% rych. pasiv. příjmu/level",
    "Rapid Tick":                "+15% rych. pasiv. příjmu/level",
    "Time Accelerator":          "+15% rych. pasiv. příjmu/level",
}

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
                    prestige_menu_open = False
            # Kliknutí myší - přepnout settings pokud bylo kliknuto na tlačítko
            if settings_button_rect.collidepoint(event.pos):
                settings_open = not settings_open
                if settings_open:
                    shop_open = False
                    rebirth_open = False
                    prestige_menu_open = False
            # Kliknutí myší - přepnout rebirth pokud bylo kliknuto na tlačítko
            if rebirth_button_rect.collidepoint(event.pos):
                rebirth_open = not rebirth_open
                if rebirth_open:
                    shop_open = False
                    settings_open = False
                    prestige_menu_open = False
            # Kliknutí myší - přepnout prestige menu pokud bylo kliknuto
            if prestige_btn_rect.collidepoint(event.pos):
                prestige_menu_open = not prestige_menu_open
                if prestige_menu_open:
                    shop_open = False
                    settings_open = False
                    rebirth_open = False
                    periodic_table_open = False
            # Kliknutí myší - přepnout periodic table pokud bylo kliknuto
            if periodic_btn_rect.collidepoint(event.pos):
                periodic_table_open = not periodic_table_open
                if periodic_table_open:
                    shop_open = False
                    settings_open = False
                    rebirth_open = False
                    prestige_menu_open = False

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

            # Settings kliknutí - bez fullscreen toggleu
            if settings_open:
                pass

            # Upgrade kliknutí v rebirth menu - používáme UPGRADE_POSITIONS pro detekci kliknutí
            if rebirth_open:
                # Rebirth tlačítko (pozice musí odpovídat renderu)
                rebirth_button = pygame.Rect(SIRKA//2 - 120, 70, 240, 45)
                if rebirth_button.collidepoint(event.pos):
                    if score >= rebirth_requirement:
                        # PŘIČTI rebirth body (oprava bugu)
                        earned = calculate_rebirth_points_from_score(score)
                        rebirth_points += earned
                        # Reset skóre a základních upgradů
                        _, _, _, start_score, _ = get_milestone_multipliers()
                        score = start_score
                        passive_gain_level = 0
                        wall_bonus_level = 0
                        multi_base_gain_level = 0
                        rebirth_open = False
                        
            # Prestige menu kliknutí
            if prestige_menu_open:
                p_button = pygame.Rect(SIRKA//2 - 150, 110, 300, 50)
                if p_button.collidepoint(event.pos) and rebirth_points >= prestige_requirement:
                    # PROVEĎ PRESTIGE
                    quark_multiplier = 1.0
                    if "Quark Extractor" in prestige_upgrades:
                        quark_multiplier += (0.20 * prestige_upgrades["Quark Extractor"]["level"])
                    if "Quark Collector" in prestige_upgrades:
                        quark_multiplier += (0.30 * prestige_upgrades["Quark Collector"]["level"])
                    if "Quark Generator" in prestige_upgrades:
                        quark_multiplier += (0.50 * prestige_upgrades["Quark Generator"]["level"])

                    quarks_zisk = max(1, int((rebirth_points // prestige_requirement) * quark_multiplier))
                    quarks += quarks_zisk
                    prestige_points += 1
                    rebirth_points = 0
                    
                    # reset rebirth tree
                    for v in prestige_upgrades.values():
                        v["level"] = 0
                    
                    _, _, _, start_score, _ = get_milestone_multipliers()
                    score = start_score
                    passive_gain_level = 0
                    wall_bonus_level = 0
                    multi_base_gain_level = 0
                    
                    break_infinity_unlocked = False
                    prestige_multiplier = 1.0
                    prestige_menu_open = False

                # Kliknutí na uzly stromu - porovnáme s UPGRADE_POSITIONS
                for upgrade_name, upgrade_info in prestige_upgrades.items():
                    if upgrade_name not in UPGRADE_POSITIONS:
                        continue
                    pos_x, pos_y = UPGRADE_POSITIONS[upgrade_name]
                    upgrade_button = pygame.Rect(pos_x, pos_y, _UPG_BW, _UPG_BH)
                    if upgrade_button.collidepoint(event.pos):
                        prerequisites_met = all(
                            prestige_upgrades[prereq]["level"] > 0
                            for prereq in upgrade_info["prereq"]
                        )
                        is_available = prerequisites_met or len(upgrade_info["prereq"]) == 0
                        cost = upgrade_info["cost"]
                        if is_available and rebirth_points >= cost and upgrade_info["level"] < upgrade_info["max_level"]:
                            rebirth_points -= cost
                            upgrade_info["level"] += 1
                            prestige_multiplier = calculate_prestige_multiplier(prestige_upgrades)
                            if upgrade_name == "Break Infinity" and upgrade_info["level"] == 1:
                                break_infinity_unlocked = True

            # Periodic table element kliknutí
            if periodic_table_open:
                # Obdelníky logiky nákupu vykreslujeme v render_periodic_table. Můžeme je tu re-kalkulovat.
                elem_keys = list(elements_db.keys())
                box_size, gap = 75, 5
                start_px = SIRKA // 2 - (18 * (box_size + gap)) // 2
                start_py = VYSKA // 2 - (6 * (box_size + gap)) // 2  # Vycentrování na výšku
                for i, key in enumerate(elem_keys):
                    row, col = PT_COORDS.get(key, (0, 0))
                    rect = pygame.Rect(start_px + col * (box_size + gap), start_py + row * (box_size + gap), box_size, box_size)
                    if rect.collidepoint(event.pos):
                        if not elements_unlocked[key]:
                            if quarks >= elements_db[key]["cost"]:
                                quarks -= elements_db[key]["cost"]
                                elements_unlocked[key] = True

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
        # Aplikuj tick-speed multiplikátor z pravé alt větve
        passive_gain_per_second *= calculate_tick_speed_multiplier(prestige_upgrades)
        
        # Aplikuj milestone multiplikátory prestige funkce!
        _, m_passive, m_global, _, _ = get_milestone_multipliers()
        em_passive, em_global, em_wall, _ = calculate_elements_multipliers(score, rebirth_points, prestige_upgrades)
        passive_gain_per_second *= (m_passive * m_global * em_passive * em_global)
    else:
        # Bez Automation upgradu: žádný pasivní gain!
        passive_gain_per_second = 0
    
    passive_gain_per_frame = passive_gain_per_second / 60  # 60 FPS
    score += passive_gain_per_frame

    # Score Momentum self-boost (logaritmický, nezávislý na Automation)
    self_boost_per_second = calculate_score_self_boost(score, prestige_upgrades)
    score += self_boost_per_second / 60

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
            # Aplikuj global milestone multiplikátor
            _, _, m_global, _, _ = get_milestone_multipliers()
            em_passive, em_global, em_wall, _ = calculate_elements_multipliers(score, rebirth_points, prestige_upgrades)
            wall_damage *= (m_global * em_global * em_wall)
            
            score += wall_damage
            
            # Přidání flying textu
            floating_texts.append({
                'x': sq['x'] + sq['size'] // 2,
                'y': sq['y'] + sq['size'] // 2,
                'text': f"+{int(wall_damage) if wall_damage == int(wall_damage) else f'{wall_damage:.1f}'}",
                'life': 60,
                'color': (255, 200, 50)
            })

            # Vytvoření odletujících částic
            import random
            for _ in range(12):
                particles.append({
                    'x': sq['x'] + sq['size'] // 2,
                    'y': sq['y'] + sq['size'] // 2,
                    'vx': random.uniform(-6, 6),
                    'vy': random.uniform(-6, 6),
                    'life': random.randint(20, 40),
                    'max_life': 40,
                    'color': (random.randint(200, 255), random.randint(50, 150), 0)
                })

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
    game_surf.fill(CERNA) # Vyčistí okno černou barvou

    # Vykreslení částic
    popping_particles = []
    for p in particles:
        p['x'] += p['vx']
        p['y'] += p['vy']
        p['life'] -= 1
        if p['life'] > 0:
            popping_particles.append(p)
            size = max(2, int(10 * (p['life'] / p['max_life'])))
            pygame.draw.rect(game_surf, p['color'], (p['x'] - size//2, p['y'] - size//2, size, size))
    particles = popping_particles

    # Vykreslení všech čtverců
    for sq in squares:
        pygame.draw.rect(game_surf, CERVENA, (sq['x'], sq['y'], sq['size'], sq['size']))

    # Vykreslení floating textů
    popping_texts = []
    for ft in floating_texts:
        ft['y'] -= 1.5 # letí nahoru
        ft['life'] -= 1
        if ft['life'] > 0:
            popping_texts.append(ft)
            alpha = max(0, int((ft['life'] / 60) * 255))
            ft_surf = small_pismo.render(ft['text'], True, ft['color'])
            ft_surf.set_alpha(alpha)
            game_surf.blit(ft_surf, (ft['x'] - ft_surf.get_width()//2, ft['y'] - ft_surf.get_height()//2))
    floating_texts = popping_texts

    # Zobrazení skóre a počtu čtverců + bodů za zásah + pasivní gain
    # Přepočítej pasivní gain pro zobrazení (stejně jako pro herní logiku)
    if prestige_upgrades["Automation (Passive Gain)"]["level"] > 0:
        passive_gain_display = calculate_passive_gain_per_second(score, passive_gain_level)
        passive_gain_display *= prestige_multiplier
        passive_gain_display *= calculate_passive_gain_multiplier_from_prestige(prestige_upgrades)
        passive_gain_display *= calculate_multi_base_gain_multiplier(multi_base_gain_level)
        _, m_passive, m_global, _, _ = get_milestone_multipliers()
        em_passive, em_global, em_wall, _ = calculate_elements_multipliers(score, rebirth_points, prestige_upgrades)
        passive_gain_display *= (m_passive * m_global * em_passive * em_global)
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
    _, _, m_global, _, _ = get_milestone_multipliers()
    em_passive, em_global, em_wall, _ = calculate_elements_multipliers(score, rebirth_points, prestige_upgrades)
    wall_damage_display *= (m_global * em_global * em_wall)
    if wall_damage_display == int(wall_damage_display):
        wall_str = f"{int(wall_damage_display)}"
    else:
        wall_str = f"{wall_damage_display:.1f}"
    
    hud_text = f"Score: {score_str}    Passive/s: {passive_str}    Wall+: {wall_str}    Rebirth: {rebirth_points}    Rebirth Multi: x{prestige_multiplier:.2f}    Squares: {len(squares)}"
    text_plocha = pismo.render(hud_text, True, BILA)
    game_surf.blit(text_plocha, (10, VYSKA - 30))

    # Tlačítko pro settings
    pygame.draw.rect(game_surf, (100, 100, 100), settings_button_rect)
    settings_text = menu_pismo.render("Settings", True, BILA)
    game_surf.blit(settings_text, (settings_button_rect.x + settings_button_rect.width//2 - settings_text.get_width()//2, settings_button_rect.y + settings_button_rect.height//2 - settings_text.get_height()//2))

    # Tlačítko pro shop
    pygame.draw.rect(game_surf, (100, 100, 100), shop_button_rect)
    btn_text = menu_pismo.render("Upgrades", True, BILA)
    game_surf.blit(btn_text, (shop_button_rect.x + shop_button_rect.width//2 - btn_text.get_width()//2, shop_button_rect.y + shop_button_rect.height//2 - btn_text.get_height()//2))
    
    # Tlačítko pro rebirth
    pygame.draw.rect(game_surf, (150, 50, 50), rebirth_button_rect)
    rebirth_text = menu_pismo.render("Rebirth", True, BILA)
    game_surf.blit(rebirth_text, (rebirth_button_rect.x + rebirth_button_rect.width//2 - rebirth_text.get_width()//2, rebirth_button_rect.y + rebirth_button_rect.height//2 - rebirth_text.get_height()//2))

    # Tlačítko pro prestige
    pygame.draw.rect(game_surf, (200, 150, 50), prestige_btn_rect)
    prestige_btn_text = menu_pismo.render("Prestige", True, BILA)
    game_surf.blit(prestige_btn_text, (prestige_btn_rect.x + prestige_btn_rect.width//2 - prestige_btn_text.get_width()//2, prestige_btn_rect.y + prestige_btn_rect.height//2 - prestige_btn_text.get_height()//2))

    # Tlačítko pro Periodic Table
    pygame.draw.rect(game_surf, (50, 200, 200), periodic_btn_rect)
    periodic_btn_text = menu_pismo.render("Elements", True, CERNA)
    game_surf.blit(periodic_btn_text, (periodic_btn_rect.x + periodic_btn_rect.width//2 - periodic_btn_text.get_width()//2, periodic_btn_rect.y + periodic_btn_rect.height//2 - periodic_btn_text.get_height()//2))

    # Pokud je shop otevřený, vykreslíme upgrade tlačítka
    if shop_open:
        overlay = pygame.Surface((500, 300))
        overlay.set_alpha(220)
        overlay.fill((30, 30, 30))
        game_surf.blit(overlay, (SIRKA//2 - 250, VYSKA//2 - 150))
        shop_title = pismo.render("Shop - Upgrades", True, BILA)
        game_surf.blit(shop_title, (SIRKA//2 - 200, VYSKA//2 - 130))
        
        # Passive Gain upgrade - informační text (koupen přes Prestige)
        automation_level = prestige_upgrades["Automation (Passive Gain)"]["level"]
        if automation_level > 0:
            passive_status = f"✓ Automation Active (Prestige Lvl {automation_level})"
            passive_color = (0, 255, 0)  # Zelená - aktivní
        else:
            passive_status = "✗ Automation Locked (Buy in Prestige Tree)"
            passive_color = (255, 100, 100)  # Červená - není dostupné
        passive_label = pismo.render(passive_status, True, passive_color)
        game_surf.blit(passive_label, (SIRKA//2 - 240, VYSKA//2 - 70))
        
        # Wall Bonus upgrade
        wall_cost = calculate_wall_bonus_cost(wall_bonus_level)
        wall_damage = calculate_wall_bonus_damage(wall_bonus_level) * calculate_multi_base_gain_multiplier(multi_base_gain_level)
        wall_text = f"Wall Bonus (+{int(wall_damage)} pts/hit): Cost {wall_cost}pts (Lvl {wall_bonus_level})"
        if score >= wall_cost:
            wall_color = (0, 255, 0)
        else:
            wall_color = (255, 0, 0)
        wall_label = pismo.render(wall_text, True, wall_color)
        game_surf.blit(wall_label, (SIRKA//2 - 240, VYSKA//2 - 20))
        
        # Multi Base Gain upgrade
        multi_cost = calculate_multi_base_gain_cost(multi_base_gain_level)
        multi_mult = calculate_multi_base_gain_multiplier(multi_base_gain_level)
        multi_text = f"Multi Base Gain (x{multi_mult:.2f}): Cost {multi_cost}pts (Lvl {multi_base_gain_level})"
        if score >= multi_cost:
            multi_color = (0, 255, 0)
        else:
            multi_color = (255, 0, 0)
        multi_label = pismo.render(multi_text, True, multi_color)
        game_surf.blit(multi_label, (SIRKA//2 - 240, VYSKA//2 + 20))

        
        # Info text
        info_text = pismo.render("Click on upgrade to buy", True, (200, 200, 200))
        game_surf.blit(info_text, (SIRKA//2 - 200, VYSKA//2 + 80))
    # Pokud jsou settings otevřené, vykreslíme nastavení
    if settings_open:
        overlay = pygame.Surface((580, 200))
        overlay.set_alpha(230)
        overlay.fill((30, 30, 30))
        game_surf.blit(overlay, (SIRKA//2 - 290, VYSKA//2 - 100))
        settings_title = pismo.render("Settings", True, BILA)
        game_surf.blit(settings_title, (SIRKA//2 - 260, VYSKA//2 - 80))

        desc = small_pismo.render("Vědecká notace (Eternitynum) - spouští se od 1,000,000,000,000", True, (200, 200, 200))
        game_surf.blit(desc, (SIRKA//2 - 260, VYSKA//2 - 40))
        state_text = "Eternitynum: Enabled" if eternitynum else "Eternitynum: Disabled"
        label = small_pismo.render(state_text, True, BILA)
        game_surf.blit(label, (SIRKA//2 - 260, VYSKA//2 - 18))

    # Pokud je rebirth menu otevřené, vykreslíme upgrade tree (inspirováno The Ultimate Upgrade Tree)
    if rebirth_open:
        # Plnoobrazovkový tmavý overlay
        overlay = pygame.Surface((SIRKA, VYSKA))
        overlay.set_alpha(245)
        overlay.fill((8, 8, 12))
        game_surf.blit(overlay, (0, 0))

        # Nadpis
        rebirth_title = pismo.render("★  Prestige - Ultimate Upgrade Tree  ★", True, (255, 255, 255))
        game_surf.blit(rebirth_title, (SIRKA//2 - rebirth_title.get_width()//2, 12))

        # Info řádek nahoře - aktuální rebirth body a multiplier
        earned_if_rebirth = calculate_rebirth_points_from_score(score)
        info_bar = small_pismo.render(
            f"Rebirth Points: {rebirth_points}    |    Score Multiplier: x{prestige_multiplier:.2f}    |    Score do resetu: {max(0, rebirth_requirement - score):.0f}",
            True, (180, 180, 180)
        )
        game_surf.blit(info_bar, (SIRKA//2 - info_bar.get_width()//2, 42))

        # Rebirth tlačítko
        rebirth_button = pygame.Rect(SIRKA//2 - 120, 70, 240, 45)
        can_rebirth = score >= rebirth_requirement
        btn_bg = (50, 150, 50) if can_rebirth else (140, 45, 45)
        pygame.draw.rect(game_surf, btn_bg, rebirth_button, border_radius=8)
        pygame.draw.rect(game_surf, (220, 220, 220), rebirth_button, 2, border_radius=8)
        if can_rebirth:
            rb_label = small_pismo.render(f"★  Získat {earned_if_rebirth} Rebirth Bodů  ★", True, (255, 230, 0))
        else:
            rb_label = small_pismo.render(f"Potřeba {rebirth_requirement} skóre", True, (255, 255, 255))
        game_surf.blit(rb_label, (rebirth_button.x + rebirth_button.w//2 - rb_label.get_width()//2, rebirth_button.y + 10))
        
        # --- Vykreslíme čáry (prerekvizity) PŘED uzly ---
        for upgrade_name, upgrade_info in prestige_upgrades.items():
            if upgrade_name not in UPGRADE_POSITIONS:
                continue
            from_x, from_y = UPGRADE_POSITIONS[upgrade_name]
            from_cx = from_x + _UPG_BW // 2
            from_cy = from_y  # vrchol uzlu
            for prereq in upgrade_info["prereq"]:
                if prereq not in UPGRADE_POSITIONS:
                    continue
                to_x, to_y = UPGRADE_POSITIONS[prereq]
                to_cx = to_x + _UPG_BW // 2
                to_cy = to_y + _UPG_BH  # spodek prerekvizity
                # Barva čáry: světlá pokud prerekvizita splněna, tmavá jinak
                prereq_done = prestige_upgrades[prereq]["level"] > 0
                line_col = (160, 160, 160) if prereq_done else (60, 60, 70)
                pygame.draw.line(game_surf, line_col, (to_cx, to_cy), (from_cx, from_cy), 2)

        # --- Vykreslíme uzly stromu ---
        for upgrade_name, upgrade_info in prestige_upgrades.items():
            if upgrade_name not in UPGRADE_POSITIONS:
                continue
            pos_x, pos_y = UPGRADE_POSITIONS[upgrade_name]
            level = upgrade_info["level"]
            max_level = upgrade_info["max_level"]
            cost = upgrade_info["cost"]

            # Zkontroluj prerekvizity
            prerequisites_met = all(prestige_upgrades[p]["level"] > 0 for p in upgrade_info["prereq"])
            is_available = prerequisites_met or len(upgrade_info["prereq"]) == 0

            # Základní barva tieru
            tier = UPGRADE_TIERS.get(upgrade_name, "Tier1")
            base_col = TIER_COLORS[tier]

            rect = pygame.Rect(pos_x, pos_y, _UPG_BW, _UPG_BH)

            if not is_available:
                # Zamčený uzel - velmi tmavý
                node_bg    = (25, 25, 32)
                node_border = (55, 55, 65)
                text_col   = (80, 80, 90)
            elif level >= max_level:
                # MAX level - zlatá hranice, plná barva tieru
                r, g, b = base_col
                node_bg    = (r//3, g//3, b//3)
                node_border = (220, 180, 0)
                text_col   = (255, 255, 255)
            elif rebirth_points >= cost:
                # Koupitelný - plná barva tieru, světlá hranice
                r, g, b = base_col
                node_bg    = (r//4, g//4, b//4)
                node_border = base_col
                text_col   = (255, 255, 255)
            else:
                # Dostupný, ale nestačí bodů - ztlumená verze
                r, g, b = base_col
                node_bg    = (20, 20, 25)
                node_border = (r//2, g//2, b//2)
                text_col   = (r//2 + 50, g//2 + 50, b//2 + 50)

            # Kresba uzlu s kulatými rohy
            pygame.draw.rect(game_surf, node_bg, rect, border_radius=6)
            pygame.draw.rect(game_surf, node_border, rect, 2, border_radius=6)

            # Název upgradu (zkrácení pokud je moc dlouhý)
            name_display = upgrade_name if len(upgrade_name) <= 18 else upgrade_name[:16] + ".."
            name_surf = tiny_pismo.render(name_display, True, text_col)
            game_surf.blit(name_surf, (rect.x + rect.w//2 - name_surf.get_width()//2, rect.y + 5))

            # Status řádek (level / MAX a cena)
            if level >= max_level:
                status_str = "✓  MAX"
                status_col = (220, 180, 0)
            else:
                status_str = f"Lv{level}/{max_level}  cost:{cost}"
                status_col = (200, 200, 200) if is_available else (80, 80, 90)
            status_surf = tiny_pismo.render(status_str, True, status_col)
            game_surf.blit(status_surf, (rect.x + rect.w//2 - status_surf.get_width()//2, rect.y + 22))

        # --- Legenda barv (vlevo dole) ---
        legend_items = [
            ("Tier 1 - Základní",  TIER_COLORS["Tier1"]),
            ("Tier 2 - Mid-game",  TIER_COLORS["Tier2"]),
            ("Tier 3 - Pokročilé", TIER_COLORS["Tier3"]),
            ("Tier 4 - Elite",     TIER_COLORS["Tier4"]),
            ("Alt. větev L",       TIER_COLORS["Alt"]),
            ("Tick Speed R",       TIER_COLORS["Tick"]),
        ]
        leg_title = small_pismo.render("Legenda:", True, (160, 160, 160))
        game_surf.blit(leg_title, (15, VYSKA - 170))
        for i, (label, col) in enumerate(legend_items):
            pygame.draw.rect(game_surf, col, (15, VYSKA - 150 + i * 20, 14, 14), border_radius=3)
            pygame.draw.rect(game_surf, (120, 120, 120), (15, VYSKA - 150 + i * 20, 14, 14), 1, border_radius=3)
            leg_surf = small_pismo.render(label, True, col)
            game_surf.blit(leg_surf, (34, VYSKA - 150 + i * 20))

        # --- Tooltip: zobrazí efekt upgradu při najetí myší ---
        mouse_pos = pygame.mouse.get_pos()
        for upg_name, upg_info in prestige_upgrades.items():
            if upg_name not in UPGRADE_POSITIONS:
                continue
            tx, ty = UPGRADE_POSITIONS[upg_name]
            hover_rect = pygame.Rect(tx, ty, _UPG_BW, _UPG_BH)
            if hover_rect.collidepoint(mouse_pos):
                # Sestav text tooltipu
                effect_txt  = UPGRADE_EFFECTS.get(upg_name, "")
                lvl_txt     = f"Level: {upg_info['level']} / {upg_info['max_level']}"
                cost_txt    = f"Cena: {upg_info['cost']} rebirth bodů"
                lines = [upg_name, effect_txt, lvl_txt, cost_txt]

                # Šířka tooltipu podle nejdelšího řádku
                line_surfs = [small_pismo.render(l, True, (230, 230, 230)) for l in lines]
                tip_w = max(s.get_width() for s in line_surfs) + 16
                tip_h = len(lines) * 22 + 10

                # Pozice: vedle kurzoru, ale ne mimo obrazovku
                tip_x = min(mouse_pos[0] + 12, SIRKA - tip_w - 4)
                tip_y = min(mouse_pos[1] + 12, VYSKA - tip_h - 4)

                # Pozadí tooltipu
                tip_surf = pygame.Surface((tip_w, tip_h))
                tip_surf.set_alpha(220)
                tip_surf.fill((20, 20, 28))
                game_surf.blit(tip_surf, (tip_x, tip_y))
                pygame.draw.rect(game_surf, TIER_COLORS.get(UPGRADE_TIERS.get(upg_name, "Tier1"), (200,200,200)),
                                 (tip_x, tip_y, tip_w, tip_h), 1, border_radius=4)

                # Text tooltipu
                for i, surf in enumerate(line_surfs):
                    col = TIER_COLORS.get(UPGRADE_TIERS.get(upg_name, "Tier1"), (230,230,230)) if i == 0 else (200, 200, 200)
                    surf = small_pismo.render(lines[i], True, col)
                    game_surf.blit(surf, (tip_x + 8, tip_y + 6 + i * 22))
                break  # Zobraz max 1 tooltip najednou

    # Vykreslení Prestige menu s tabulkou milníků
    if prestige_menu_open:
        overlay = pygame.Surface((SIRKA, VYSKA))
        overlay.set_alpha(245)
        overlay.fill((10, 5, 20))
        game_surf.blit(overlay, (0, 0))

        prestige_title = pismo.render("★  PRESTIGE (Milestones)  ★", True, (255, 215, 0))
        game_surf.blit(prestige_title, (SIRKA//2 - prestige_title.get_width()//2, 30))
        
        info_txt = small_pismo.render(f"Celkové Prestiže: {prestige_points}  |  Rebirth Body: {rebirth_points}  |  Vygeneruje se: {max(1, rebirth_points // prestige_requirement)} Quarks", True, (200, 200, 200))
        game_surf.blit(info_txt, (SIRKA//2 - info_txt.get_width()//2, 70))

        # Tlačítko k prestiži
        p_button = pygame.Rect(SIRKA//2 - 150, 110, 300, 50)
        can_prestige = (rebirth_points >= prestige_requirement)
        bg_col = (50, 150, 50) if can_prestige else (150, 50, 50)
        pygame.draw.rect(game_surf, bg_col, p_button, border_radius=8)
        pygame.draw.rect(game_surf, (200, 200, 200), p_button, 2, border_radius=8)
        
        if can_prestige:
            btn_lbl = small_pismo.render("SPUSTIT PRESTIGE", True, (255, 255, 255))
        else:
            btn_lbl = small_pismo.render(f"Chybí {prestige_requirement - rebirth_points} RB na Prestige", True, (200, 200, 200))
        game_surf.blit(btn_lbl, (p_button.x + p_button.w//2 - btn_lbl.get_width()//2, p_button.y + 12))

        # Tabulka milestones
        miles_y = 200
        miles_title = pismo.render("--- Milestones (Získané výhody napořád) ---", True, BILA)
        game_surf.blit(miles_title, (SIRKA//2 - miles_title.get_width()//2, miles_y))
        
        milestones = [
            (1, "Zeď vždy dává základ +50 damage navíc"),
            (2, "Zisk Rebirth bodů je zvýšen 5x"),
            (3, "Pasivní příjem bodů je zvýšen 10x"),
            (4, "Po každém dalším resetu začínáte s 1,000,000 skóre"),
            (5, "Globální Multiplikátor skóre zvýšen 100x"),
            (6, "Zisk Rebirth bodů je zvýšen 10x (na celkem 50x)"),
            (7, "Pasivní příjem bodů je zvýšen 100x (na 1000x)"),
            (8, "Zeď vždy dává základ +1000 damage navíc"),
            (10, "Začínáte s 1,000,000,000 skóre"),
            (12, "Globální Multiplikátor skóre zvýšen 10000x"),
            (15, "Zisk Rebirth bodů je zvýšen dalších 100x (na 5000x)")
        ]
        
        for m_req, m_desc in milestones:
            miles_y += 50
            m_col = (0, 255, 0) if prestige_points >= m_req else (100, 100, 100)
            status_char = "✓" if prestige_points >= m_req else "✗"
            m_surf = pismo.render(f"{status_char} [{m_req} Prestige]: {m_desc}", True, m_col)
            game_surf.blit(m_surf, (SIRKA//2 - 300, miles_y))

    # Vykreslení Periodic Table menu
    if periodic_table_open:
        overlay = pygame.Surface((SIRKA, VYSKA))
        overlay.set_alpha(245)
        overlay.fill((5, 10, 15))
        game_surf.blit(overlay, (0, 0))

        title = pismo.render("★  PERIODIC TABLE OF ELEMENTS  ★", True, (100, 255, 255))
        game_surf.blit(title, (SIRKA//2 - title.get_width()//2, 30))
        
        info_txt = small_pismo.render(f"Vaše Quarks: {quarks}   |   Elements boostují hru podle Rebirths/Score/Quarks", True, (200, 200, 200))
        game_surf.blit(info_txt, (SIRKA//2 - info_txt.get_width()//2, 70))
        
        em_passive, em_global, em_wall, em_rebirth = calculate_elements_multipliers(score, rebirth_points, prestige_upgrades)
        mult_txt = small_pismo.render(f"Boost prvků: Pasiv x{em_passive:.2f} | Skóre x{em_global:.2f} | Wall x{em_wall:.2f} | Rebirth x{em_rebirth:.2f}", True, (0, 255, 100))
        game_surf.blit(mult_txt, (SIRKA//2 - mult_txt.get_width()//2, 95))

        elem_keys = list(elements_db.keys())
        box_size = 75
        gap = 5
        start_px = SIRKA // 2 - (18 * (box_size + gap)) // 2
        start_py = VYSKA // 2 - (6 * (box_size + gap)) // 2

        for i, key in enumerate(elem_keys):
            row, col = PT_COORDS.get(key, (0, 0))
            px = start_px + col * (box_size + gap)
            py = start_py + row * (box_size + gap)
            rect = pygame.Rect(px, py, box_size, box_size)
            
            unlocked = elements_unlocked[key]
            cost = elements_db[key]["cost"]
            can_buy = quarks >= cost
            
            if unlocked:
                bg_col = (50, 200, 50)
                border_col = (100, 255, 100)
            elif can_buy:
                bg_col = (50, 100, 150)
                border_col = (100, 200, 255)
            else:
                bg_col = (40, 40, 50)
                border_col = (80, 80, 90)

            pygame.draw.rect(game_surf, bg_col, rect, border_radius=5)
            pygame.draw.rect(game_surf, border_col, rect, 2, border_radius=5)

            sym_surf = pismo.render(elements_db[key]["symbol"], True, BILA)
            game_surf.blit(sym_surf, (px + box_size//2 - sym_surf.get_width()//2, py + 15))

            if not unlocked:
                cost_surf = tiny_pismo.render(f"C: {cost}", True, (200, 200, 200))
                game_surf.blit(cost_surf, (px + box_size//2 - cost_surf.get_width()//2, py + 55))
            else:
                own_surf = tiny_pismo.render("VLASTNÍ", True, (255, 255, 100))
                game_surf.blit(own_surf, (px + box_size//2 - own_surf.get_width()//2, py + 55))

        # Tooltips = efekt elementu hover (najetí myší)
        mouse_pos = pygame.mouse.get_pos()
        for i, key in enumerate(elem_keys):
            row, col = PT_COORDS.get(key, (0, 0))
            px = start_px + col * (box_size + gap)
            py = start_py + row * (box_size + gap)
            rect = pygame.Rect(px, py, box_size, box_size)
            
            if rect.collidepoint(mouse_pos):
                desc_text = elements_db[key]["name"] + " - " + elements_db[key]["desc"]
                if not elements_unlocked[key]:
                    desc_text += f" (Stojí: {elements_db[key]['cost']} Quarks)"
                tip_surf = small_pismo.render(desc_text, True, BILA)
                
                tip_w, tip_h = tip_surf.get_width() + 16, 30
                tip_x = min(mouse_pos[0] + 15, SIRKA - tip_w - 5)
                tip_y = min(mouse_pos[1] + 15, VYSKA - tip_h - 5)
                
                pygame.draw.rect(game_surf, (20, 30, 40), (tip_x, tip_y, tip_w, tip_h), border_radius=4)
                pygame.draw.rect(game_surf, (100, 200, 255), (tip_x, tip_y, tip_w, tip_h), 1, border_radius=4)
                game_surf.blit(tip_surf, (tip_x + 8, tip_y + 5))
                break


    # Aktualizace displeje
    okno.blit(game_surf, (0, 0))
    pygame.display.flip() # Zobrazí změny na obrazovce

    # Omezení FPS
    hodiny.tick(60) # Omezí rychlost na 60 FPS

pygame.quit() # Ukončí Pygame
sys.exit() # Ukončí program