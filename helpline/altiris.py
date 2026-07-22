from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import os
import sys
login=input("Login :")
password=input("Mot de passe :")

# ---------------- FONCTION POUR GERER LE .EXE ----------------

def get_driver_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), "chromedriver.exe")
    else:
        return "chromedriver.exe"

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

# ---------------- LANCEMENT chrome----------------
service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)
service.log_path = "nul"
options = Options()
options.add_argument("--log-level=3")
options.add_argument("--disable-logging")
options.add_argument("--silent")

options.add_experimental_option("excludeSwitches", ["enable-logging"])

service.log_path = "nul"
driver.maximize_window()
wait = WebDriverWait(driver, 15)

driver.get("http://wpvpaap0006zzzo.emea.cib/Deploy/")

# Username
wait.until(EC.visibility_of_element_located((By.ID, "usernametab"))).send_keys(login)

# Password
wait.until(
EC.visibility_of_element_located((By.ID, "TextBoxComponent__5e69f07b_0702_11e2_8163_000c29e69a6b"))
).send_keys(password)

 # Login button
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginbutton"]'))).click()
# ---------- BOUCLE ----------

for i in range(len(serial_numbers)):

    print(f"Traitement PC {i+1}...")

    # --- My Desk V2 ---
    wait.until(
        EC.element_to_be_clickable(
            (By.NAME, 'Windows 10 22H2 - MyDesk V2')
        )
    ).click()

    # --- Next ---
    wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="l5b"]'))
    ).click()

  
    time.sleep(6)
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="l2b"]'))).send_keys(serial_numbers[i])
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="l3b"]'))).send_keys(asset_tags[i])
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="l1b"]'))).send_keys(passwords[i])




    # --- Next ---
    wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="l6b"]'))
    ).click()


    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//input[@type='submit' and @value='New Schedule']")
        )
    ).click()

    
    wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="l2b"]'))
    )

print("\n🎉 Tous les PCs ont été traités.")
