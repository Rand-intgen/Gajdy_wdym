from typing import List

# ==============================================================================
# ÚKOL 4: Filtrování dat a List Comprehension (Lekce N03, N15)
# ==============================================================================

class Zbozi:
    def __init__(self, nazev: str, cena: float):
        self.nazev = nazev
        self.cena = cena
        
    def __str__(self):
         return f"{self.nazev}: {self.cena:.0f} Kč"

def filtruj_a_zlevni(zbozi_list: List[Zbozi], max_cena: float, sleva_procenta: float) -> List[Zbozi]:
    """
    DOPLŇTE KÓD ZDE:
    Implementace přes jednu smyčku nebo pokročilou (list comprehension).
    Rozjeďte cyklus a zjistěte které instance `Zbozi` ze `zbozi_list` mají cenu <= `max_cena`.
    Najitým vítězům změňte jejich vnitřní cenu na novou poniženou (`z.cena = stará * procento..`).
    Následně metodu nechejte tyto vybrané produkty vrátit jako nový seznam instancí z funkce ven.
    """
    # [VYSVĚTLENÍ]: Vyrobíme si nový prázdný seznam pro uložení jen opravdu těch produktů, co mají nárok na slevu.
    vysledny_seznam = []
    
    # [VYSVĚTLENÍ]: Spustíme smyčku "for" přes každou jednu položku (z) uvnitř vstupního seznamu zbozi_list.
    for z in zbozi_list:
        
        # [VYSVĚTLENÍ]: Pokud je cena konkrétního zboží menší nebo rovna limitu (max_cena).
        if z.cena <= max_cena:
            
            # [VYSVĚTLENÍ]: Změníme hodnotu staré ceny uvnitř instance. 
            # (1 - sleva_procenta / 100) aplikuje 20% slevu tak, že číslo násobí 0.8.
            z.cena = z.cena * (1 - (sleva_procenta / 100))
            
            # [VYSVĚTLENÍ]: Už zlevněnou a prověřenou položku odkládáme bokem do našeho nového seznamu.
            vysledny_seznam.append(z)
            
    # [VYSVĚTLENÍ]: A nakonec jen vrátíme posbírané produkty z funkce ven (do proměnné dostupne_zlevnene, kde se metoda volá zadáním dole).
    return vysledny_seznam
# Testovací část pro spuštění
if __name__ == "__main__":
    sklad_zbozi = [
        Zbozi("Kniha Python", 600.0),
        Zbozi("Herní Klávesnice", 1200.0),
        Zbozi("Levná Myš", 400.0),
        Zbozi("Monitor 4K", 5000.0)
    ]

    print("--- 1. Původní Stav Zboží z databáze ---")
    for z in sklad_zbozi: print(z)

    print("\n--- 2. Po slevové akci: Hledáme do <1000 kč s 20% slevou ---")
    # Volání naplněné studentské funkce z Úkolu 4
    dostupne_zlevnene = filtruj_a_zlevni(sklad_zbozi, max_cena=1000.0, sleva_procenta=20.0)
    
    # Výsledek filtrace a slev
    if dostupne_zlevnene is None:
        print("Tvá funkce stále vrací starou prázdnou Nonehodnotu :)")
    else:
        for z in dostupne_zlevnene: print(z)
