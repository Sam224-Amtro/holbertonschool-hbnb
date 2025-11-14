# HBnB – Part 3

## Système backend modulaire avec API, services et persistance

### 🧩 Description du projet

Ce projet est une implémentation modulaire de la partie backend du clone HBnB.
Il repose sur une architecture en couches (API → Services → Repository → Modèles), accompagnée de tests unitaires et d’un système de persistance basé sur une base SQLite.

### Le projet inclut :
- Une API Python minimaliste
- Un système de modèles (User, Place, Review, Amenity…)
- Une couche de persistance orientée repository
- Une couche service/facade
- Une base SQLite + script SQL d’initialisation
- Des tests unitaires
- Un environnement configurable (config.py)

## 🏛️ Architecture du projet

```
part3/
 ├── app/               # Applications / API
 │    ├── api/          # Endpoints et logique API
 │    ├── services/     # Logique métier (facades/services)
 │    ├── persistence/  # Système repository + stockage SQLite
 │    ├── extensions.py # Extensions (db, factory…)
 │    └── __init__.py
 │
 ├── models/            # Modèles de données
 │    ├── base_model.py
 │    ├── user.py
 │    ├── place.py
 │    ├── review.py
 │    ├── amenity.py
 │    └── __init__.py
 │
 ├── tests/             # Tests unitaires
 │    ├── test_users.py
 │    ├── test_places.py
 │    ├── test_reviews.py
 │    ├── test_amenities.py
 │    └── test_relations.py
 │
 ├── instance/
 │    └── development.db  # Base SQLite pour le mode dev
 │
 ├── config.py           # Fichier de configuration
 ├── run.py              # Point d’entrée de l’application
 ├── requirements.txt    # Dépendances Python
 ├── hbnb.sql            # Script SQL d'initialisation/structure
 ├── mermaid.js          # Diagramme / support de documentation
 └── README.md
```
## Les installation a faire

### 1 . il faut installer
```
pip install -r requirements.txt
```
### 2 . Initialiser la base de données (optionnel)
```
sqlite3 instance/development.db < hbnb.sql
```
## Lancement de l'application
```
python run.py
```
### 🧪 Lancer les tests
```
pytest -q
```
### Les tests couvrent :

- Users

- Places

- Amenities

- Reviews

- Relations entre modèles

### 📦 Structure des données

#### Les modèles implémentés :

- User
- Place
- Review
- Amenity
- BaseModel (héritage commun)

#### La persistance utilise le modèle Repository :
- repository.py : classe générique
- user_repository.py : exemple spécialisé

## 🏗️ Architecture logicielle
Le projet suit une architecture modulaire en couches :

```
css

[ API ]  → endpoints
    ↓
[ Services / Facade ]  → logique métier
    ↓
[ Repository ]  → abstraction stockage
    ↓
[ Models ]  → structure des objets
    ↓
[ SQLite ]  → stockage physique
```
### Ce découplage permet :

- testabilité renforcée
- modularité
- séparation claire des responsabilités

## 👤 Auteur / Contributeurs

### SANOUSSY FOFANA
