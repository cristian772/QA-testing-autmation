from itertools import count
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import sys

# ---------------- FONCTION POUR GERER LE .EXE ----------------
login = input("Login altiris: ")
password = input("Mot de passe altiris: ")



def get_driver_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), "msedgedriver.exe")
    else:
        return "msedgedriver.exe"

# ---------------- INPUT DEPUIS EXCEL ----------------

def read_column(title):
    print(f"\nColle la colonne pour {title}")
    print("Quand tu as fini, appuie sur ENTER une fois de plus\n")

    data = ""
    while True:
        line = input()
        if line == "":
            break
        data += line + "\n"

    return data.strip().splitlines()

serial_numbers = read_column("Numéros de série")
asset_tags = read_column("Asset tags")
passwords = read_column("Mots de passe")

# ---------------- VERIFICATION ----------------

if not (len(serial_numbers) == len(asset_tags) == len(passwords)):
    print("\n❌ ERREUR : Les colonnes n'ont pas le même nombre de lignes.")
    input("Appuie sur ENTER pour fermer...")
    sys.exit()

print(f"\n✅ {len(serial_numbers)} PCs chargés.\n")

# ---------------- LANCEMENT EDGE ----------------

service = Service(get_driver_path())
driver = webdriver.Edge(service=service)
driver.maximize_window()

wait = WebDriverWait(driver, 15)

driver.get("http://wpvpaap0006zzzo.emea.cib/Deploy")
driver.implicitly_wait(10)
driver.find_element(By.ID, "usernametab").send_keys(login)
driver.find_element(By.ID, "TextBoxComponent__5e69f07b_0702_11e2_8163_000c29e69a6b").send_keys(password)
driver.find_element(By.ID,"loginbutton").click()
# ---------------- BOUCLE AUTOMATIQUE ----------------

for i in range(len(serial_numbers)):
    # Cliquer Windows 10
    windows_option = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//td[contains(text(),'Windows 10 22H2 - MyDesk V2')]")
        )
    )
    windows_option.click()

    driver.find_element(By.XPATH, '//*[@id="l5b"]').click()


    # Attendre les champs (on précise le type)
    serial_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input#12b[type='text']")
        )
    )

    asset_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input#13b[type='text']")
        )
    )

    password_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input#11b[type='text']")
        )
    )

    # Nettoyer
    serial_input.clear()
    asset_input.clear()
    password_input.clear()

    # Remplir
    serial_input.send_keys(serial_numbers[i])
    asset_input.send_keys(asset_tags[i])
    password_input.send_keys(passwords[i])
    time.sleep(1)
    # Cliquer bouton 16b
    driver.find_element(By.XPATH, '//*[@id="l6b"]').click()
    time.sleep(1)
    # 🔥 Ici on clique sur le SUBMIT 13b (type submit)
    driver.find_element(By.XPATH,' //*[@id="l3b"]').click()





print("\n🎉 Tous les PCs ont été traités.")
driver.quit()

input("Appuie sur ENTER pour fermer...")

