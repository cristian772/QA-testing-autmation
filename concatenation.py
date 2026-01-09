import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# -----------------------------
# CONFIGURATION
# -----------------------------
csv_file = r"C:\temp\fusion\all.csv"
hyb_dir = r"C:\temp\fusion\Hybridation"
rec_dir = r"C:\temp\fusion\Fiches_Postes"
out_dir = r"C:\temp\fusion\resultats"
MAX_THREADS = min(32, os.cpu_count() * 2)  # optimal pour I/O  MAX_THREADS = 16   # plus sûr pour réseau

os.makedirs(out_dir, exist_ok=True)
lock = Lock()  # pour protéger l'affichage de la barre de progression


# -----------------------------
# FONCTIONS UTILES
# -----------------------------
def split_html(content):
    """Extrait le head et le body d'un fichier HTML et nettoie les caractères nuls"""
    content = content.replace("\x00", "")
    l = content.lower()

    b1 = l.find("<body>")
    b2 = l.find("</body>")
    h1 = l.find("<head>")
    h2 = l.find("</head>")

    head = content[h1:h2 + 7] if h1 != -1 and h2 != -1 else ""
    body = content[b1 + 6:b2] if b1 != -1 and b2 != -1 else content
    return head, body


def traiter_hostname(hostname):
    """Concatène Hybridation + Recette pour un hostname"""
    f1 = os.path.join(hyb_dir, f"{hostname}_Hybridation.HTML")
    f2 = os.path.join(rec_dir, f"{hostname}_Recette.HTML")
    out = os.path.join(out_dir, f"{hostname}_concatener.HTML")

    if not os.path.exists(f1) or not os.path.exists(f2):
        return False

    # Lire les fichiers et extraire head/body
    with open(f1, "r", encoding="utf-8", errors="ignore") as a:
        head, body1 = split_html(a.read())

    with open(f2, "r", encoding="utf-8", errors="ignore") as b:
        _, body2 = split_html(b.read())

    # Écrire le fichier final
    with open(out, "w", encoding="utf-8") as o:
        o.write(
            "<html>" +
            head +
            "<body>" +
            body1 +
            '<div style="height:50vh;overflow:auto;border-top:2px solid #000;">' +
            body2 +
            "</div></body></html>"
        )

    return True


# -----------------------------
# LECTURE DU CSV
# -----------------------------
with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:
    lignes = f.readlines()

# Filtrer seulement les lignes TRUE
hostnames = [
    l.strip().split(";")[1]  # hostname = deuxième champ
    for l in lignes
    if l.strip().split(";")[-1].strip().lower() == "true"
]

total = len(hostnames)
if total == 0:
    print("Aucune ligne TRUE trouvée dans le CSV.")
    sys.exit(0)

print(f"Traitement multithread de {total} fichiers HTML...\n")

# -----------------------------
# MULTITHREAD + BARRE DE PROGRESSION
# -----------------------------
done = 0
bar_len = 40

with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    futures = [executor.submit(traiter_hostname, h) for h in hostnames]

    for future in as_completed(futures):
        done += 1
        filled = int(bar_len * done / total)
        bar = "#" * filled + "-" * (bar_len - filled)

        with lock:
            sys.stdout.write(f"\r[{bar}] {done}/{total}")
            sys.stdout.flush()

print("\n\n✅ Tous les fichiers HTML ont été créés !")
