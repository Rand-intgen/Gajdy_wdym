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

# Upgrade systém
passive_gain_level = 0  # Úroveň passive gain upgradu
wall_bonus_level = 0  # Úroveň wall bonus upgradu

def calculate_passive_gain_cost(level):
    """Vypočítá cenu pro nákup passive gain upgradu.
    Exponenciální růst ceny: 10 * 1.5^level
    """
    return int(10 * (1.5 ** level))

def calculate_wall_bonus_cost(level):
    """Vypočítá cenu pro nákup wall bonus upgradu.
    Exponenciální růst ceny: 5 * 1.4^level
    """
    return int(5 * (1.4 ** level))

def calculate_wall_bonus_damage(level):
    """Vypočítá počet bodů za náraz do stěny s wall bonus upgradem.
    Level 0-4: +1, +2, +3, +4, +5
    Každých 5 levelů se vše zdvojnásobí (bez resetu)
    """
    return (1 + level) * (2 ** (level // 5))

def calculate_passive_gain_per_second(current_score, level):
    """Vypočítá pasivní gain za sekundu na základě aktuálního skóre a úrovně upgradu.
    Exponenciální růst: (score / 100) ^ 1.1 * 0.1 * (1.2 ^ level)
    Každých 10 levelů se efekt zvýší 5x
    """
    if current_score < 100:
        return 0
    # Základní gain z score
    multiplier = (current_score / 100) ** 1.05
    base_gain = multiplier * 0.1
    
    # Aplikuj upgrade level
    upgrade_multiplier = (1.2 ** level)
    
    # Každých 10 levelů zvýš efekt 5x
    mega_multiplier = (5 ** (level // 10))
    
    total_gain = base_gain * upgrade_multiplier * mega_multiplier
    return total_gain

def is_colliding_with_wall(x, y, size):
    return x <= 0 or (x + size) >= SIRKA or y <= 0 or (y + size) >= VYSKA

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
            # Kliknutí myší - přepnout settings pokud bylo kliknuto na tlačítko
            if settings_button_rect.collidepoint(event.pos):
                settings_open = not settings_open
                if settings_open:
                    shop_open = False

            # Upgrade kliknutí v shopu
            if shop_open:
                mouse_x, mouse_y = event.pos
                passive_cost = calculate_passive_gain_cost(passive_gain_level)
                wall_cost = calculate_wall_bonus_cost(wall_bonus_level)
                
                # Passive Gain button area
                if (SIRKA//2 - 250 < mouse_x < SIRKA//2 + 250 and 
                    VYSKA//2 - 70 < mouse_y < VYSKA//2 - 40):
                    if score >= passive_cost:
                        score -= passive_cost
                        passive_gain_level += 1
                # Wall Bonus button area
                if (SIRKA//2 - 250 < mouse_x < SIRKA//2 + 250 and 
                    VYSKA//2 - 20 < mouse_y < VYSKA//2 + 10):
                    if score >= wall_cost:
                        score -= wall_cost
                        wall_bonus_level += 1

            # Kliknutí v settings - no interactive toggle any more (eternitynum controlled in code)
            if settings_open:
                pass

    # Získání stavu kláves
    klavesa = pygame.key.get_pressed() # Zjistí stisknuté klávesy
    dx = 0
    dy = 0
    if klavesa[pygame.K_LEFT]:
        dx = -rychlost
    if klavesa[pygame.K_RIGHT]:
        dx = rychlost
    if klavesa[pygame.K_UP]:
        dy = -rychlost
    if klavesa[pygame.K_DOWN]:
        dy = rychlost
    # Výpočet a aplikace pasivního gainu s upgrady
    passive_gain_per_second = calculate_passive_gain_per_second(score, passive_gain_level)
    passive_gain_per_frame = passive_gain_per_second / 60  # 60 FPS
    score += passive_gain_per_frame

    # Pohyb všech čtverců stejným směrem podle vstupu
    to_remove = []
    initial_len = len(squares)
    for i in range(initial_len):
        sq = squares[i]
        prev = prev_colliding[i]

        # Aplikuj pohyb
        sq['x'] += dx
        sq['y'] += dy

        # Omez pozici na okno (clamp)
        sq['x'] = max(0, min(sq['x'], SIRKA - sq['size']))
        sq['y'] = max(0, min(sq['y'], VYSKA - sq['size']))

        now_collide = is_colliding_with_wall(sq['x'], sq['y'], sq['size'])

        # Pokud právě došlo k novému nárazu do stěny -> skóre + zničení čtverce
        if (not prev) and now_collide:
            # Základní 1 bod + bonus z wall_bonus upgradu
            score += calculate_wall_bonus_damage(wall_bonus_level)
            to_remove.append(i)

        # Aktualizuj prev_colliding pro tento čtverec
        prev_colliding[i] = now_collide

    # Odstraň čtverce, které byly zničeny při nárazu
    if to_remove:
        new_squares_list = []
        new_prev = []
        for idx, sq in enumerate(squares):
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
    passive_gain_display = calculate_passive_gain_per_second(score, passive_gain_level)
    # Use scientific notation automatically when `eternitynum` is enabled and value >= 1e12
    sci_threshold = 1e12
    if eternitynum and score >= sci_threshold:
        score_str = f"{score:.2e}"
    else:
        score_str = f"{int(score):,}"
    if eternitynum and passive_gain_display >= sci_threshold:
        passive_str = f"{passive_gain_display:.2e}"
    else:
        passive_str = f"{passive_gain_display:,.2f}"
    hud_text = f"Score: {score_str}    Passive/s: {passive_str}    Wall+: {calculate_wall_bonus_damage(wall_bonus_level)}    Squares: {len(squares)}"
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

    # Pokud je shop otevřený, vykreslíme upgrade tlačítka
    if shop_open:
        overlay = pygame.Surface((500, 300))
        overlay.set_alpha(220)
        overlay.fill((30, 30, 30))
        okno.blit(overlay, (SIRKA//2 - 250, VYSKA//2 - 150))
        shop_title = pismo.render("Shop - Upgrades", True, BILA)
        okno.blit(shop_title, (SIRKA//2 - 200, VYSKA//2 - 130))
        
        # Passive Gain upgrade
        passive_cost = calculate_passive_gain_cost(passive_gain_level)
        passive_text = f"Passive Gain (+Level): Cost {passive_cost}pts (Lvl {passive_gain_level})"
        if score >= passive_cost:
            passive_color = (0, 255, 0)  # Zelená když si můžeš koupit
        else:
            passive_color = (255, 0, 0)  # Červená když ne
        passive_label = pismo.render(passive_text, True, passive_color)
        okno.blit(passive_label, (SIRKA//2 - 240, VYSKA//2 - 70))
        
        # Wall Bonus upgrade
        wall_cost = calculate_wall_bonus_cost(wall_bonus_level)
        wall_text = f"Wall Bonus (+{calculate_wall_bonus_damage(wall_bonus_level)} pts/hit): Cost {wall_cost}pts (Lvl {wall_bonus_level})"
        if score >= wall_cost:
            wall_color = (0, 255, 0)
        else:
            wall_color = (255, 0, 0)
        wall_label = pismo.render(wall_text, True, wall_color)
        okno.blit(wall_label, (SIRKA//2 - 240, VYSKA//2 - 20))
        
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

    # Aktualizace displeje
    pygame.display.flip() # Zobrazí změny na obrazovce

    # Omezení FPS
    hodiny.tick(60) # Omezí rychlost na 60 FPS

pygame.quit() # Ukončí Pygame
sys.exit() # Ukončí program