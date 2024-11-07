from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from playwright.async_api import async_playwright
from urllib.parse import urlparse
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modèle pour recevoir l'URL de la requête
class URLRequest(BaseModel):
    url: str


# Route pour l'interface HTML
@app.get("/", response_class=HTMLResponse)
async def get_interface():
    with open("index.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)


@app.post("/analyze")
async def analyze_url(request: URLRequest):
    url = request.url
    domaines = set()
    cookies_list = []

    try:
        async with async_playwright() as p:
            # lancer firefox
            browser = await p.firefox.launch(headless=True)
            context = await browser.new_context()

            # Créer une nouvelle page et intercepter les requêtes HTTP
            page = await context.new_page()

            async def log_request(request):
                domaine = urlparse(request.url).netloc
                domaines.add(domaine)

            page.on("request", log_request)

            # Ouvrir l'URL
            try:
                await page.goto(url, timeout=60000)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Erreur lors du chargement de la page : {str(e)}")
            # Attendre quelques secondes pour s'assurer que toutes les requêtes sont capturées
            await asyncio.sleep(5)

            # Capturer les cookies déposés
            cookies = await context.cookies()
            cookies_list = sorted([
                {
                    "name": cookie['name'],
                    "domain": cookie['domain'],
                    "value": cookie['value']
                }
                for cookie in cookies
            ], key=lambda x: x['domain'])

            # Fermer le navigateur
            await browser.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur : {str(e)}")

    # Retourner les différents noms de domaines capturés et les cookies
    return {
        "domaines": sorted(list(domaines)),
        "cookies": cookies_list
    }
