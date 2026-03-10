@echo off
echo Automaticky pridavam soubory do gitu (git add)...
git add .

echo Vytvarim commit s prednastavenou zpravou...
git commit -m "Automaticky ulozeno a odeslano (auto_push)"

echo Stahuji aktualizace ze vzdaleneho repozitare (git pull)...
git pull origin main --rebase

echo Odesilam na GitHub (git push)...
git push origin main

echo.
echo Hotovo!
pause
