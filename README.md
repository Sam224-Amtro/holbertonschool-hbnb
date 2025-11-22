# HBnB – Projet Web Full-Stack

Ce dépôt contient la partie **backend** et **frontend** du projet **HBnB**, une application web permettant la gestion de lieux, utilisateurs, reviews, etc.
L'architecture combine une API REST en **Flask** et une interface web en **HTML/CSS/JS**.

---

## 🚀 Technologies

### Backend
- Python 3.x
- Flask
- SQLAlchemy
- MySQL
- API REST (versionnée : `/api/v1/`)
- Tests unitaires

### Frontend
- HTML5
- CSS3
- JavaScript
- Templates Jinja2

---

## 📁 Arborescence du projet

```
part4/
├── backend/
│   ├── __pycache__/
│   ├── app/
│   │   ├── __pycache__/
│   │   ├── api/
│   │   │   ├── __pycache__/
│   │   │   └── v1/
│   │   │       └── __init__.py
│   │   ├── models/
│   │   ├── persistence/
│   │   ├── services/
│   │   ├── __init__.py
│   │   └── extensions.py
│   ├── instance/
│   ├── tests/
│   ├── README.md
│   ├── config.py
│   ├── mermaid.js
│   ├── requirements.txt
│   └── run.py
│
└── frontend/
    ├── static/
    │   ├── images/
    │   ├── scripts.js
    │   └── styles.css
    ├── templates/
    │   ├── add_review.html
    │   ├── index.html
    │   ├── login.html
    │   └── place.html
    ├── README.md
    └── README.md   (duplicate)
```

# 🛠️ Backend
2. Créer l'environnement virtuel
```
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
3. Installer les dépendances
```
pip install -r requirements.txt
```
5. Lancer l’API
```
python run.py
```
API disponible :
```
http://127.0.0.1:5000/api/v1/
```
# 🎨 Frontend

Le frontend est servi automatiquement via Flask.
Accès :
```
http://127.0.0.1:5000/
```
# 🧪 Tests
```
pytest
```

# 📌 Fonctionnalités

- Authentification utilisateurs

- Affichage de lieux

- Ajout de reviews

- bAPI REST versionnée

- Frontend responsive simple

# 📄 Licence

À définir (MIT, GPL, etc.)

# ✨ Auteur / Contributeurs
Sanoussy fofana
