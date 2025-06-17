import asyncio
from playwright.sync_api import sync_playwright
import requests

API_BASE = "http://127.0.0.1:8000/api/"
USERNAME = "data_bot"
PASSWORD = "bot1234"
KEYWORDS = ["data ingénieur", "data engineer", "python"]
URL = "https://www.welcometothejungle.com/fr/jobs?query=data+ing%C3%A9nieur&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDI"

def get_token():
    res = requests.post(f"{API_BASE}token/", json={
        "username": USERNAME,
        "password": PASSWORD
    })
    return res.json()["access"]

def post_offer(offer, token):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.post(f"{API_BASE}candidatures/", json=offer, headers=headers)
    if res.status_code == 201:
        print(f"✅ Ajouté : {offer['titre']} ({offer['ville']})")
    else:
        print(f"❌ Erreur : {res.status_code} – {res.text}")

def run_scraper():
    token = get_token()
    print("🔍 Chargement des offres avec Playwright...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, timeout=60000)
        page.wait_for_selector('article')  # attendre que les offres s'affichent

        articles = page.query_selector_all('article')

        offres = []
        for article in articles:
            title_tag = article.query_selector('h3')
            link_tag = article.query_selector('a')
            location_tag = article.query_selector('div[data-testid="address"]')

            titre = title_tag.inner_text().strip() if title_tag else None
            lien = link_tag.get_attribute("href") if link_tag else None
            ville = location_tag.inner_text().strip() if location_tag else "Non précisée"

            if titre and lien and any(k.lower() in titre.lower() for k in KEYWORDS):
                offre = {
                    "titre": titre,
                    "entreprise": "WTTJ",
                    "lien": "https://www.welcometothejungle.com" + lien,
                    "ville": ville,
                    "type_contrat": "CDI"
                }
                offres.append(offre)

        browser.close()

        print(f"🎯 {len(offres)} offres détectées")
        for o in offres:
            post_offer(o, token)

if __name__ == "__main__":
    run_scraper()
