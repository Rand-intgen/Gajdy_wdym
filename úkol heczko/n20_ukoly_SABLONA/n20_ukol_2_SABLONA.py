# ==============================================================================
# ÚKOL 2: Hezký uživatelský výpis pomocí Dunder metod (Lekce N10, N13)
# ==============================================================================

class Zbozi:
    def __init__(self, nazev: str, cena: float, mnozstvi: int):
        self.nazev = nazev
        self.cena = cena
        self.mnozstvi = mnozstvi

    def __str__(self) -> str:
        """
        DOPLŇTE KÓD ZDE:
        Využijte naformátovaný text (f-string) a vraťte přehledný nápis.
        Text musí vypadat ve formátu: "Zboží Kniha Python | 600.00 Kč | 10 ks skladem"
        Nezapomeňte zakrouhlit halíře u ceny na vizuální "dvě desetinná místa".
        """
        # [VYSVĚTLENÍ]: F-string (text s "f" na začátku) dovoluje vkládat Python proměnné přímo do textu do chlupatých závorek { }.
        # Zápis {self.cena:.2f} říká navíc programu: "Zformátuj toto číslo na 2 desetinná místa (f = float)".
        return f"Zboží {self.nazev} | {self.cena:.2f} Kč | {self.mnozstvi} ks skladem"
    def __repr__(self) -> str:
        return f"Zbozi(nazev={self.nazev!r}, cena={self.cena!r}, mnozstvi={self.mnozstvi!r})"

# Testovací část pro spuštění
if __name__ == "__main__":
    kniha = Zbozi("Kniha Python", 600.5, 10)
    mys = Zbozi("Myš Bezdrátová", 419.99, 2)
    
    # Python automaticky zavolá metodu __str__ při tisku (print(kniha))
    print("Měl by se objevit hezky zformátovaný text vlastností:")
    print(kniha)
    print(mys)
