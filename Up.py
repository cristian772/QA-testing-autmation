import os

# Noms des fichiers
fichier1 = "fichier1.html"
fichier2 = "fichier2.html"
nom_sauvegarde = "fichier_concatene.html"

def extraire_body(fichier):
    """Extrait le contenu entre <body> et </body>"""
    with open(fichier, "r", encoding="utf-8") as f:
        contenu = f.read()
    start = contenu.find("<body>")
    end = contenu.find("</body>")
    if start == -1 or end == -1:
        # si pas de <body>, renvoyer tout le contenu
        return contenu
    return contenu[start + len("<body>"):end]

# Lire le contenu de body de chaque fichier
body1 = extraire_body(fichier1)
body2 = extraire_body(fichier2)

# Lire le <head> du premier fichier
with open(fichier1, "r", encoding="utf-8") as f:
    contenu1 = f.read()
start_head = contenu1.find("<head>")
end_head = contenu1.find("</head>")
if start_head != -1 and end_head != -1:
    head = contenu1[start_head:end_head+len("</head>")]
else:
    head = ""

# Créer le fichier fusionné
with open(nom_sauvegarde, "w", encoding="utf-8") as f_out:
    f_out.write("<html>\n")
    f_out.write(head + "\n")
    f_out.write("<body>\n")
    f_out.write(body1 + "\n")
    f_out.write(body2 + "\n")
    f_out.write("</body>\n</html>")

print(f"Fichiers fusionnés correctement dans : {nom_sauvegarde}")
