import os

# Dossiers
fichier_hybridation = r"C:\temp\fusion\Hybridation"
fichier_certificats = r"C:\temp\fusion\Fiches_Postes"
outputdir = r"C:\temp\fusion\resultats"

# Créer le dossier de sortie si il n'existe pas
os.makedirs(outputdir, exist_ok=True)

def concatenation(file1, file2, output):
    """Concatène deux fichiers HTML et les sauvegarde dans output"""
    try:
        with open(file1, 'r', encoding="utf-8", errors="ignore") as f1, \
             open(file2, 'r', encoding="utf-8", errors="ignore") as f2:
            contenu1 = f1.read()
            contenu2 = f2.read()

        concat = contenu1 + "\n" + contenu2

        with open(output, 'w', encoding="utf-8") as f_out:
            f_out.write(concat)

        print(f"Fichiers {file1} + {file2} fusionnés dans {output}")

    except FileNotFoundError as e:
        print(f"Erreur: {e}")

# Lister les fichiers dans le dossier hybridation
fichiers_hyb = os.listdir(fichier_hybridation)

if not fichiers_hyb:
    print("Dossier hybridation vide")
else:
    for fichier in fichiers_hyb:
        if fichier.upper().endswith(".HTML"):
            # Extraire le nom de base (avant _)
            hostname = fichier.split("_")[0]

            hybridation = os.path.join(fichier_hybridation, hostname + "_Hybridation.HTML")
            recette = os.path.join(fichier_certificats, hostname + "_Recette.HTML")
            nomfinal = os.path.join(outputdir, hostname + "_concatener.HTML")

            # Vérifier que les fichiers existent
            if os.path.exists(hybridation) and os.path.exists(recette):
                concatenation(hybridation, recette, nomfinal)
            else:
                print(f"Fichiers manquants pour {hostname}")
