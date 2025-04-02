import time
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# 🔹 Configurer l'URL de l'artiste sur Ticketmaster
ARTISTE_URL = "https://www.ticketmaster.com/search?q=nom_de_l_artiste"
WEBHOOK_DISCORD = "https://discord.com/api/webhooks/TON_WEBHOOK"

def envoyer_notification(message):
    """Envoie une alerte sur Discord."""
    data = {"content": message}
    requests.post(WEBHOOK_DISCORD, json=data)
    print("[🔔] Notification envoyée :", message)

def verifier_disponibilite():
    """Scrape Ticketmaster pour vérifier si des billets sont disponibles."""
    with sync_playwright() as p:
        navigateur = p.chromium.launch(headless=True)
        page = navigateur.new_page()
        page.goto(ARTISTE_URL)

        time.sleep(3)  # Attendre le chargement
        html = page.content()
        navigateur.close()

    soup = BeautifulSoup(html, "html.parser")
    
    # 🔍 Rechercher l'élément contenant "Billets en vente" ou une date
    billets = soup.find_all("div", class_="event-listing")
    
    if billets:
        print("[✅] Billets trouvés ! Envoi d'une notification.")
        envoyer_notification(f"🎟️ Billets disponibles pour l’artiste ! Vérifie ici : {ARTISTE_URL}")
    else:
        print("[❌] Pas encore de billets disponibles.")

if __name__ == "__main__":
    while True:
        print("[🔍] Vérification en cours...")
        verifier_disponibilite()
        time.sleep(60)  # Vérifier toutes les minutes
