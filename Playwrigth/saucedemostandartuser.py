from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)  # Passer à False pour voir l'exécution
    page = browser.new_page()
    page.goto("https://www.saucedemo.com/")  # Exemple d'une page de connexion

    # Remplir les champs du formulaire
    page.fill("input[name='user-name']", "standard_user")
    page.fill("input[name='password']", "secret_sauce")

    # Soumettre le formulaire en cliquant sur le bouton Login
    page.click("input[type='submit']")

    # Attendre que la page des produits soit chargée
    page.wait_for_selector(".inventory_list")

    return page, browser  # Retourner la page et le navigateur pour réutilisation


def add_to_cart(page):
    # Ajouter le premier produit au panier
    page.click(".inventory_item button.btn_inventory")
    page.click('//*[@id="add-to-cart-sauce-labs-bike-light"]')
    page.screenshot(path="E:/automation/addtocardscreenshot.png")
    # Petite pause pour s'assurer que l'action est prise en compte
    page.wait_for_timeout(500)
def checkout(page):
    page.click('//*[@id="shopping_cart_container"]/a')
    page.click('//*[@id="checkout"]')
    page.fill("input[name='firstName']","test prenom") #le prenom et le nom pour le check out
    page.fill("input[name='lastName']", "test nom")
    page.fill("input[name='postalCode']", "75000") #CODE POSTAL TEST
    page.screenshot(path="E:/automation/personaldatatreenshot.png")
    page.click('//*[@id="continue"]')
    page.click('//*[@id="finish"]')
    page.screenshot(path="E:/automation/checkoutreenshot.png")

with sync_playwright() as playwright:
    page, browser = run(playwright)  # Lancer la connexion
    add_to_cart(page)# Ajouter un produit au panier
    checkout(page)
    page.wait_for_timeout(3000)  # Pause avant fermeture (pour voir l'effet)
    browser.close()

