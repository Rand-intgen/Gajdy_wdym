@echo off
:: Přejde do adresáře, kde se nachází tento skript
cd /d "%~dp0"

echo ==================================================
echo         Auto Commit & Push pro hra.py
echo ==================================================
echo.

:: 1. Přidání souboru hra.py
echo Pridavam soubor Gajdy_game/hra.py do stage...
git add Gajdy_game/hra.py
if %ERRORLEVEL% neq 0 (
    echo [CHYBA] Nepodarilo se pridat soubor. Zkontrolujte, zda jste v Git repozitari.
    goto end
)

:: 2. Vytvoření zprávy pro commit s aktuálním datem a časem
set commit_msg=Auto commit hra.py - %date% %time%

:: 3. Commit změn
echo Komituji zmeny...
git commit -m "%commit_msg%"
if %ERRORLEVEL% neq 0 (
    echo.
    echo [INFO] Zadne nove zmeny k zapsani nebo commit nebylo mozne provest.
)

:: 4. Push do vzdáleného repozitáře
echo Odesilam zmeny na GitHub (git push)...
git push
if %ERRORLEVEL% neq 0 (
    echo.
    echo [CHYBA] Nepodarilo se odeslat zmeny. Zkontrolujte pripojeni nebo konflikty.
) else (
    echo.
    echo [HOTOVO] Vse uspesne nahrano na GitHub!
)

:end
echo.
echo Pro ukonceni stisknete libovolnou klavesu...
pause >nul
