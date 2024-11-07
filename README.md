#Simulateur de contrôle CNIL

Utilisation du simulateur de contrôle CNIL

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
docker build -t simulateur-cnil .
docker run -p 8000:8000 simulateur-cnil
```


