import os

# Dossiers
fichier_hybridation = r"C:\temp\fusion\Hybridation"
fichier_certificats = r"C:\temp\fusion\Fiches_Postes"
outputdir = r"C:\temp\fusion\resultats"

os.makedirs(outputdir, exist_ok=True)

def extraire_body(path):
    """Extrait le contenu entre <body> et </body> et nettoie les caractères nuls"""
    with open(path, 'r', encoding="utf-8", errors="ignore") as f:
        contenu = f.read()
    # Supprimer les caractères nuls et invisibles
    contenu = contenu.replace('\x00', '').replace('\r', '').replace('\t', '')
    start = contenu.lower().find("<body>")
    end = contenu.lower().find("</body>")
    if start == -1 or end == -1:
        return contenu  # si pas de body, renvoyer tout
    return contenu[start + len("<body>"):end]

# Lister les fichiers Hybridation
fichiers_hyb = [f for f in os.listdir(fichier_hybridation) if f.upper().endswith(".HTML")]

for fichier in fichiers_hyb:
    hostname = fichier.split("_")[0]

    hybridation = os.path.join(fichier_hybridation, hostname + "_Hybridation.HTML")
    recette = os.path.join(fichier_certificats, hostname + "_Recette.HTML")
    nomfinal = os.path.join(outputdir, hostname + "_concatener.HTML")

    if os.path.exists(hybridation) and os.path.exists(recette):
        # Extraire body de chaque fichier
        body1 = extraire_body(hybridation)
        body2 = extraire_body(recette)

        # Extraire le head du premier fichier
        with open(hybridation, 'r', encoding="utf-8", errors="ignore") as f:
            contenu1 = f.read().replace('\x00', '')
        start_head = contenu1.lower().find("<head>")
        end_head = contenu1.lower().find("</head>")
        head = ""
        if start_head != -1 and end_head != -1:
            head = contenu1[start_head:end_head+len("</head>")]

        # Créer le fichier final
        with open(nomfinal, 'w', encoding="utf-8") as f_out:
            f_out.write("<html>\n")
            f_out.write(head + "\n")
            f_out.write("<body>\n")
            f_out.write(body1 + "\n")
            f_out.write(body2 + "\n")
            f_out.write("</body>\n</html>")

        print(f"Fichier créé pour {hostname} : {nomfinal}")
    else:
        print(f"Fichiers manquants pour {hostname}")
