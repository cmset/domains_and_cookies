# Utiliser une image de base officielle Python avec support pour les versions récentes
FROM python:3.12-slim

# Installer les dépendances système nécessaires pour Playwright
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk-bridge2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libxshmfence1 \
    libgtk-3-0 \
    libgbm1 \
    libx11-xcb1 \
    wget \
    && apt-get clean

# Copier le fichier requirements.txt et installer les dépendances Python
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt && playwright install firefox

# Copier les fichiers de l'application dans le conteneur
COPY main.py /app/main.py
COPY index.html /app/index.html

# Définir le répertoire de travail
WORKDIR /app

# Exposer le port de l'application
EXPOSE 8000

# Lancer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]