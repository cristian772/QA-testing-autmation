@echo off
setlocal EnableDelayedExpansion
title Sauvegarde automatique - Fichier de matricage

REM ===========================================================================
REM  Sauvegarde automatique du fichier de matricage
REM  Copie le fichier depuis OneDrive vers un dossier local, toutes les minutes.
REM
REM  UTILISATION : double-cliquez sur ce fichier. Laissez la fenetre ouverte.
REM                Pour arreter : fermez la fenetre ou faites Ctrl+C.
REM ===========================================================================

REM --- A ADAPTER -------------------------------------------------------------

REM Fichier source (celui sur OneDrive)
set "SOURCE=C:\Users\U56UF23\OneDrive - Groupe Credit Agricole\DE SUE - CA-GIP-Stock Matricage - 02-Fichier De Matricage\Fichier de matricage.xlsx"

REM Dossier de destination (ou vous avez les droits d'ecriture)
set "DESTINATION=C:\Users\U56UF23\Desktop\Sauvegardes_Matricage"

REM Intervalle entre deux sauvegardes, en secondes (60 = 1 minute)
set "INTERVALLE=60"

REM Duree de conservation des sauvegardes, en jours (les plus vieilles sont
REM supprimees automatiquement). Mettre 0 pour ne jamais rien supprimer.
set "RETENTION_JOURS=7"

REM ---------------------------------------------------------------------------

echo ==========================================================
echo   SAUVEGARDE AUTOMATIQUE - FICHIER DE MATRICAGE
echo ==========================================================
echo.
echo   Source      : %SOURCE%
echo   Destination : %DESTINATION%
echo   Intervalle  : %INTERVALLE% secondes
echo   Retention   : %RETENTION_JOURS% jours
echo.
echo   Laissez cette fenetre ouverte.
echo   Pour arreter : fermez la fenetre ou faites Ctrl+C.
echo.
echo ==========================================================
echo.

REM Verifie que le fichier source existe avant de demarrer
if not exist "%SOURCE%" (
    echo [ERREUR] Fichier source introuvable :
    echo          %SOURCE%
    echo.
    echo Verifiez le chemin dans la section "A ADAPTER" de ce script.
    echo.
    pause
    exit /b 1
)

REM Cree le dossier de destination s'il n'existe pas
if not exist "%DESTINATION%" (
    echo Creation du dossier de destination...
    mkdir "%DESTINATION%" 2>nul
    if errorlevel 1 (
        echo [ERREUR] Impossible de creer le dossier :
        echo          %DESTINATION%
        echo Vous n'avez peut-etre pas les droits d'ecriture a cet endroit.
        echo.
        pause
        exit /b 1
    )
)

set "COMPTEUR=0"

:BOUCLE

REM --- Horodatage fiable (independant du format de date regional) ---
REM On passe par PowerShell car %date% et %time% changent de format selon
REM la configuration Windows, ce qui casserait les noms de fichiers.
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HH-mm-ss"') do set "HORODATAGE=%%i"

set "FICHIER_DEST=%DESTINATION%\Matricage_!HORODATAGE!.xlsx"

REM --- Copie ---
copy /Y "%SOURCE%" "!FICHIER_DEST!" >nul 2>&1

if errorlevel 1 (
    echo [!HORODATAGE!] ECHEC de la copie - nouvelle tentative dans %INTERVALLE%s
) else (
    set /a COMPTEUR+=1
    echo [!HORODATAGE!] Sauvegarde OK  ^(total : !COMPTEUR!^)
)

REM --- Menage : suppression des sauvegardes trop anciennes ---
if not "%RETENTION_JOURS%"=="0" (
    forfiles /P "%DESTINATION%" /M "Matricage_*.xlsx" /D -%RETENTION_JOURS% /C "cmd /c del @path" >nul 2>&1
)

REM --- Attente avant la prochaine sauvegarde ---
timeout /t %INTERVALLE% /nobreak >nul

goto BOUCLE
