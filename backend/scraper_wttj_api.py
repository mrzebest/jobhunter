import requests

# --- Configuration ---
USERNAME = "data_bot"
PASSWORD = "bot1234"
API_BASE = "http://127.0.0.1:8000/api/"
KEYWORDS = ["data ingénieur", "data engineer"]
WTTJ_API_URL = "https://www.welcometothejungle.com/api/fr/search"

# --- Authentification ---
def get_token():
    res = requests.post(f"{API_BASE}token/", json={"username": USERNAME, "password": PASSWORD})
    if res.status_code == 200:
        return res.json()["access"]
    else:
        print("❌ Auth échouée :", res.text)
        exit()

# --- Envoi dans l'API backend ---
def post_offer(offer, token):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.post(f"{API_BASE}candidatures/", json=offer, headers=headers)
    if res.status_code == 201:
        print(f"✅ {offer['titre']} – {offer['ville']}")
    elif res.status_code == 400:
        print(f"⚠️ Déjà postée ou invalide : {offer['titre']}")
    else:
        print(f"❌ Erreur {res.status_code}: {res.text}")

# --- Récupération des offres via WTTJ API ---
def fetch_offres():
    offres = []
    page = 1
    print("🔎 Récupération des offres WTTJ en cours...")

    while True:
        params = {
            "query": "data",
            "contract_type_names.fr[]": "CDI",
            "page": page
        }
        res = requests.get(WTTJ_API_URL, params=params)
        data = res.json()

        jobs = data.get("hits", [])
        if not jobs:
            break

        for job in jobs:
            title = job.get("title", "").strip()
            if any(k.lower() in title.lower() for k in KEYWORDS):
                offres.append({
                    "titre": title,
                    "entreprise": job.get("company_name", "Non précisée"),
                    "lien": "https://www.welcometothejungle.com" + job.get("slug", ""),
                    "ville": job.get("office_name", "Non précisée"),
                    "type_contrat": "CDI"
                })

        page += 1

    return offres

# --- Main ---
if __name__ == "__main__":
    token = get_token()
    offres = fetch_offres()
    print(f"🎯 {len(offres)} offres détectées")
    for offre in offres:
        post_offer(offre, token)
