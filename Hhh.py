import os

# Dossiers
fichier_hybridation = r"C:\temp\fusion\Hybridation"
fichier_certificats = r"C:\temp\fusion\Fiches_Postes"
outputdir = r"C:\temp\fusion\resultats"

os.makedirs(outputdir, exist_ok=True)

def extraire_body(path):
    """Extrait le contenu entre <body> et </body>"""
    with open(path, 'r', encoding="utf-8", errors="ignore") as f:
        contenu = f.read()
    start = contenu.lower().find("<body>")
    end = contenu.lower().find("</body>")
    if start == -1 or end == -1:
        return contenu  # Si pas de body, retourne tout
    return contenu[start + len("<body>"):end]

def concatenation_propre(file1, file2, output):
    """Fusionne le contenu <body> de deux fichiers HTML"""
    body1 = extraire_body(file1)
    body2 = extraire_body(file2)

    # On prend le <head> du premier fichier
    with open(file1, 'r', encoding="utf-8", errors="ignore") as f:
        contenu1 = f.read()
    start_head = contenu1.lower().find("<head>")
    end_head = contenu1.lower().find("</head>")
    head = ""
    if start_head != -1 and end_head != -1:
        head = contenu1[start_head:end_head + len("</head>")]

    # Créer le fichier final
    with open(output, 'w', encoding="utf-8") as f_out:
        f_out.write("<html>\n")
        f_out.write(head + "\n")
        f_out.write("<body>\n")
        f_out.write(body1 + "\n")
        f_out.write(body2 + "\n")
        f_out.write("</body>\n</html>")

    print(f"Fichier propre créé : {output}")

# Parcours des fichiers
fichiers_hyb = os.listdir(fichier_hybridation)

for fichier in fichiers_hyb:
    if fichier.upper().endswith(".HTML"):
        hostname = fichier.split("_")[0]
        hybridation = os.path.join(fichier_hybridation, hostname + "_Hybridation.HTML")
        recette = os.path.join(fichier_certificats, hostname + "_Recette.HTML")
        nomfinal = os.path.join(outputdir, hostname + "_concatener.HTML")

        if os.path.exists(hybridation) and os.path.exists(recette):
            concatenation_propre(hybridation, recette, nomfinal)
        else:
            print(f"Fichiers manquants pour {hostname}")
