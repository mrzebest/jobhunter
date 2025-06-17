from playwright.sync_api import sync_playwright
import requests

USERNAME = "data_bot"
PASSWORD = "bot1234"
API_BASE = "http://127.0.0.1:8000/api/"
KEYWORDS = ["data", "data ingénieur", "data engineer"]
URL = "https://www.welcometothejungle.com/fr/jobs?query=data&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDI"

def get_token():
    res = requests.post(f"{API_BASE}token/", json={"username": USERNAME, "password": PASSWORD})
    return res.json()["access"]

def post_offer(offer, token):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.post(f"{API_BASE}candidatures/", json=offer, headers=headers)
    if res.status_code == 201:
        print(f"✅ Ajoutée : {offer['titre']} ({offer['ville']})")
    elif res.status_code == 400:
        print(f"⚠️ Erreur 400 : {res.json()}")
    else:
        print(f"❌ Erreur {res.status_code}: {res.text}")

def run():
    token = get_token()
    print("🔍 Lancement du scraping...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()
        page.goto(URL, timeout=60000)

        # ✅ Attente intelligente
        page.wait_for_selector('div[role="mark"]', timeout=15000)
        page.wait_for_timeout(3000)
        page.screenshot(path="screenshot.png", full_page=True)

        cards = page.query_selector_all('a[href*="/fr/companies/"]')
        print(f"🔎 {len(cards)} offres détectées")

        offres = []
        for card in cards:
            try:
                # --- Titre ---
                title_div = card.query_selector('div[role="mark"]')
                if not title_div:
                    continue
                titre = title_div.inner_text().strip()
                if not any(k.lower() in titre.lower() for k in KEYWORDS):
                    continue

                # --- Lien ---
                lien = card.get_attribute("href")
                if not lien:
                    continue
                if not lien.startswith("http"):
                    lien = "https://www.welcometothejungle.com" + lien

                if len(lien) > 500:
                    print(f"⚠️ Lien trop long, ignoré : {lien[:50]}...")
                    continue

                # --- Ville ---
                ville_span = card.query_selector('span.sc-foEvvu.jDn1DZ')
                ville = ville_span.inner_text().strip() if ville_span else "Non précisée"

                offres.append({
                    "titre": titre,
                    "entreprise": "WTTJ",
                    "lien": lien,
                    "ville": ville,
                    "type_contrat": "CDI"
                })

            except Exception as e:
                print("❌ Erreur :", e)

        browser.close()

        print(f"🎯 {len(offres)} offres valides détectées")
        for offre in offres:
            post_offer(offre, token)

if __name__ == "__main__":
    run()
