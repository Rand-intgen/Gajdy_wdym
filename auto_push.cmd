@echo off
echo Automaticky pridavam soubory do gitu...
git add hra.py auto_push.cmd

echo.
echo Vytvarim commit s prednastavenou zpravou...
git commit -m "hra.py and auto_push.cmd update"

echo.
echo Stahuji nejnovejsi zmeny z GitHubu (aby se predeslo konfliktum)...
git pull --rebase origin main

echo.
echo Odesilam na GitHub...
git push origin main

echo.
echo Hotovo!
pause
