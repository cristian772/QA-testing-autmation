import os

# Dossiers
fichier_hybridation = r"C:\temp\fusion\Hybridation"
fichier_certificats = r"C:\temp\fusion\Fiches_Postes"
outputdir = r"C:\temp\fusion\resultats"

# Créer le dossier de sortie si nécessaire
os.makedirs(outputdir, exist_ok=True)

# Nom du fichier final
output = os.path.join(outputdir, "toutes_pages.html")

# Lister les fichiers HTML
hyb_files = [f for f in os.listdir(fichier_hybridation) if f.upper().endswith(".HTML")]
cert_files = [f for f in os.listdir(fichier_certificats) if f.upper().endswith(".HTML")]

# Commencer le HTML
with open(output, 'w', encoding="utf-8") as f_out:
    f_out.write("<html>\n<head>\n<title>Pages combinées</title>\n</head>\n<body>\n")
    f_out.write("<h1>Pages fusionnées</h1>\n")

    # Ajouter les fichiers du dossier Hybridation
    for fichier in hyb_files:
        chemin = os.path.join(fichier_hybridation, fichier)
        f_out.write(f"<h2>{fichier}</h2>\n")
        f_out.write(f'<iframe src="{chemin}" width="100%" height="600px"></iframe>\n')
        f_out.write("<hr>\n")

    # Ajouter les fichiers du dossier Fiches_Postes
    for fichier in cert_files:
        chemin = os.path.join(fichier_certificats, fichier)
        f_out.write(f"<h2>{fichier}</h2>\n")
        f_out.write(f'<iframe src="{chemin}" width="100%" height="600px"></iframe>\n')
        f_out.write("<hr>\n")

    f_out.write("</body>\n</html>")

print(f"Fichier HTML avec toutes les pages créé : {output}")
