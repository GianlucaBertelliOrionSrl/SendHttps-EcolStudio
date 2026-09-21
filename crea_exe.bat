@echo off

REM ==========================================================
REM  Compila SendHttpsPostgres
REM
REM  --onedir: exe + librerie in un'unica sottocartella
REM  --console: permette lancio da console senza bloccarla
REM ==========================================================

pyinstaller --clean --onedir --noconsole ^
  --name SendHttpsPostgres ^
  main.py

echo.
echo Compilazione completata.
echo L'eseguibile si trova in: dist\SendHttpsPostgres\
pause