"""
Inventaire par scan : transforme une liste de scans alternés
(GIP, position, GIP, position, ...) en deux colonnes propres et triées.

UTILISATION
-----------
1. Scannez à la suite dans un fichier texte "scans.txt" :
       GIP2586775
       A1-1-1
       GIP0373049
       A1-1-2
       ...
   (un scan par ligne : d'abord le GIP, puis sa position)

2. Lancez :
       python inventaire.py

3. Vous obtenez "inventaire.xlsx" avec 2 colonnes (AssetTag | Position),
   triées par tour, étage puis emplacement.

Le script détecte automatiquement si un scan est un GIP ou une position,
et signale les anomalies (scan en double, position sans GIP, etc.)
au lieu de décaler silencieusement toutes les lignes suivantes.
"""

import re
import sys
from pathlib import Path

import openpyxl

# --- Configuration -------------------------------------------------------

FICHIER_SCANS = Path("scans.txt")        # fichier d'entrée (un scan par ligne)
FICHIER_SORTIE = Path("inventaire.xlsx")  # fichier Excel généré

# Une position ressemble à "A1-1-1", "B12-4-6", "D-1-11"
MOTIF_POSITION = re.compile(r"^[A-Za-z]+\d*-\d+-\d+$")


def est_position(scan: str) -> bool:
    """Retourne True si le scan a la forme d'une position (TOUR-ETAGE-EMPLACEMENT)."""
    return bool(MOTIF_POSITION.match(scan.strip()))


def cle_de_tri(position: str):
    """Clé de tri naturelle : A1-1-1 < A1-1-2 < A1-2-1 < A2-1-1 < B1-1-1.

    Sans ça, un tri alphabétique classerait "A1-10-1" avant "A1-2-1".
    """
    m = re.match(r"^([A-Za-z]+)(\d*)-(\d+)-(\d+)$", position.strip())
    if not m:
        return ("zzz", 999, 999, 999)  # positions invalides à la fin
    lettre, numero, etage, emplacement = m.groups()
    return (lettre.upper(), int(numero or 0), int(etage), int(emplacement))


def lire_scans(chemin: Path) -> list:
    """Lit le fichier de scans, une entrée par ligne, en ignorant les lignes vides."""
    if not chemin.exists():
        print(f"ERREUR : fichier introuvable -> {chemin.resolve()}")
        print("Créez un fichier 'scans.txt' avec un scan par ligne.")
        sys.exit(1)

    with open(chemin, "r", encoding="utf-8") as f:
        return [ligne.strip() for ligne in f if ligne.strip()]


def apparier(scans: list):
    """Associe chaque GIP à la position scannée juste après.

    Retourne (paires, anomalies).
    """
    paires = []
    anomalies = []
    gip_en_attente = None

    for i, scan in enumerate(scans, start=1):
        if est_position(scan):
            if gip_en_attente is None:
                anomalies.append(f"Ligne {i} : position '{scan}' sans GIP juste avant.")
            else:
                paires.append((gip_en_attente, scan))
                gip_en_attente = None
        else:
            # C'est un GIP (ou tout autre code qui n'est pas une position)
            if gip_en_attente is not None:
                anomalies.append(
                    f"Ligne {i} : GIP '{scan}' scanné alors que '{gip_en_attente}' "
                    f"n'a pas encore reçu de position."
                )
            gip_en_attente = scan

    if gip_en_attente is not None:
        anomalies.append(f"Fin de fichier : GIP '{gip_en_attente}' sans position.")

    return paires, anomalies


def ecrire_excel(paires: list, chemin: Path) -> None:
    """Écrit les paires triées dans un fichier Excel à 2 colonnes."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inventaire"

    ws.append(["AssetTag", "Position"])
    for gip, position in paires:
        ws.append([gip, position])

    # Un peu de largeur pour que ce soit lisible directement
    ws.column_dimensions["A"].width = 18
    ws.column_dimensions["B"].width = 14

    wb.save(chemin)


def main() -> None:
    scans = lire_scans(FICHIER_SCANS)
    print(f"{len(scans)} scan(s) lu(s) dans {FICHIER_SCANS}")

    paires, anomalies = apparier(scans)

    # Tri par position (tour, étage, emplacement)
    paires.sort(key=lambda p: cle_de_tri(p[1]))

    ecrire_excel(paires, FICHIER_SORTIE)

    print(f"{len(paires)} poste(s) apparié(s) -> {FICHIER_SORTIE.resolve()}")

    if anomalies:
        print(f"\n/!\\ {len(anomalies)} anomalie(s) détectée(s) :")
        for a in anomalies:
            print("   - " + a)
    else:
        print("Aucune anomalie : tous les scans sont correctement appariés.")


if __name__ == "__main__":
    main()
