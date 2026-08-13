@echo off

REM Fichier source (sur OneDrive)
set "SOURCE=C:\Users\U56UF23\OneDrive - Groupe Credit Agricole\DE SUE - CA-GIP-Stock Matricage - 02-Fichier De Matricage\Fichier de matricage.xlsx"

REM Dossier de destination
set "DESTINATION=C:\Users\U56UF23\Desktop\Sauvegardes_Matricage"

if not exist "%DESTINATION%" mkdir "%DESTINATION%"

copy /Y "%SOURCE%" "%DESTINATION%\"

if errorlevel 1 (
    echo ECHEC de la copie.
) else (
    echo Copie terminee.
)

pause
