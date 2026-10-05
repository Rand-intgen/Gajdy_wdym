import json

# ==============================================================================
# ÚKOL 3: Bezpečný zápis dat pomocí Context Managera (Lekce N07, N18)
# ==============================================================================

class ZapisovacDatabaze:
    """Správce kontextu pro bezpečný zápis událostí do JSON logu."""
    
    def __init__(self, soubor: str):
        self.soubor = soubor
        self.data = []

    def __enter__(self):
        print(f"[DB] Odbavuji transakci (databáze `{self.soubor}` otevírána).")
        return self

    def pridej_zaznam(self, zaznam: dict):
        self.data.append(zaznam)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        DOPLŇTE KÓD ZDE:
        Pokud parametr 'exc_type' je 'None', logiku nevyhodila žádná uvnitř skrytá chyba:
        Tedy - otevřete soubor definovaný v (self.soubor) režimem ('w' - zápis) a uložte 
        záznamy (z pole self.data) za využití the modulu `json.dump()`.

        Pokud ale 'exc_type' NENÍ Nula, došlo k softwarové havárii v průběhu with bloku.
        Uživateli jen stručně vypište konzolovou hlášku, že se nic neuložilo a data zahazujeme.
        """
        # [VYSVĚTLENÍ]: Argument 'exc_type' (Exception Type) v sobě nese typ případné chyby, která vnitřní část bloku 'with' shodila.
        # Pokud je None (nic), znamená to, že vše uvnitř with-bloku proběhlo naprosto v pořádku.
        if exc_type is None:
            # [VYSVĚTLENÍ]: Otevřeme soubor pro zápis (znak 'w' = write). Slouží pro bezpečný úkon do souboru.
            with open(self.soubor, 'w', encoding='utf-8') as db_soubor:
                # [VYSVĚTLENÍ]: json.dump() z modulu json vezme paměťový objekt self.data (náš list) 
                # a hezky a napřímo ho rozepíše uložením na disk dovnitř `db_soubor`. 'indent=4' dělá uvnitř ty JSON "tabulátory".
                json.dump(self.data, db_soubor, ensure_ascii=False, indent=4)
        else:
            # [VYSVĚTLENÍ]: Pokud 'exc_type' není None (tedy například ZeroDivisionError při dělení nulou přes proměnnou 1/0),
            # proces ukládání rovnou odpískáváme. Blok soubor vůbec na disk nevytvoří. Vypíšeme jen varování.
            print(f"[DB ERROR SYSTEM] Objevila se vnitřní chyba! Odmítám data uložit. Vše nenávratně zahozeno.")
# Testovací část pro spuštění
if __name__ == "__main__":
    
    # Úspěšná operace (Po konci with bloku MUSÍ fyzicky vzniknout na disku JSON soubor log_ok)
    print("--- Testování 1: Správný běh bez chyby ---")
    with ZapisovacDatabaze("log_ok.json") as db:
        db.pridej_zaznam({"akce": "Start Skript", "stav": 200})
        db.pridej_zaznam({"akce": "Odeslán Email", "stav": 200})
        
    # Havarijní operace (Po chybě 1/0 a pádu nesmí soubor log_fail nikde existovat, ani být vytvořen) 
    print("\n--- Testování 2: Selhání uprostřed ukládání se shozením Erroru ---")   
    try:
        with ZapisovacDatabaze("log_fail.json") as db2:
            db2.pridej_zaznam({"akce": "Počítání velkých operací.", "stav": 500})
            
            # Nasimulovaná chyba "padající databáze", přes kterou the skript nesmí uložit nic
            x = 1 / 0  
    except ZeroDivisionError:
        print("[APLIKACE] Podařilo se zachránit pád programu po dělení nulou, with blok nesměl předtím nic zapsat.")
