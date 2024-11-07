#Extracteur de domaines et cookies
Cet outil capture les domaines appelés et les cookies déposés par une page web à partir de son URL.
La capture s'effectue sans demande de consentement.

Créer un environnement virtuel
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Installer les dépendances
```bash
pip install -r requirements.txt
```

Lancer le simulateur
```bash
python app.py
```

Ouvrir un navigateur et aller à l'adresse http://localhost:8000

Autre option, lancer le simulateur avec docker
```bash
docker build -t domains-and-cookies .
docker run -p 8000:8000 domains-and-cookies
```


