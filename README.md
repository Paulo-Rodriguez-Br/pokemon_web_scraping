# 🧬 Pokédex Scraper -- Pipeline de Données Pokémon

> **Scraping • Ingénierie des données • Pandas • Oracle SQL • Python
> OOP**

Ce projet implémente un pipeline complet d'extraction et de traitement
des données de la Pokédex à partir du site **pokemondb.net**, en
utilisant :

-   **Web Scraping (BeautifulSoup + Requests)**
-   **Nettoyage et transformation des données (Pandas)**
-   **Chargement dans une base Oracle (SQLAlchemy + oracledb)**
-   **Architecture orientée objet (dataclasses)**

Le résultat est un **jeu de données complet sur les Pokémon**, prêt pour
l'analyse, la visualisation ou l'intégration dans un pipeline plus
large.

------------------------------------------------------------------------

## 🚀 Fonctionnalités

✔ Extraction automatique de la Pokédex Nationale\
✔ Récupération de plusieurs tables pour chaque Pokémon\
✔ Normalisation & formatage des données\
✔ Construction progressive d'un DataFrame maître\
✔ Export direct dans **Oracle Database**\
✔ Code conforme aux standards **PEP-8, PEP-257, type hinting**\
✔ Architecture claire et maintenable en Python OOP

------------------------------------------------------------------------

## 📦 Structure du Projet

    ├── scraping.py          # Classe principale PokemonScraping
    ├── README.md
    └── requirements.txt

------------------------------------------------------------------------

## 🧠 Fonctionnement

### 1. Récupération des URL des Pokémon

À partir de la Pokédex Nationale.

### 2. Pour chaque Pokémon, extraction d'informations telles que:

-   Nom\
-   Caractéristiques de base\
-   Informations de reproduction\
-   Statistiques\
-   Tables de la section *"Basic Info"*

### 3. Construction d'un DataFrame Pandas

Agrégation ligne par ligne.

### 4. Chargement dans Oracle

En un seul appel :

``` python
inst.save_dataframe_to_oracle(connection)
```

------------------------------------------------------------------------

## 🔧 Exemple d'Utilisation

``` python
from scraping import PokemonScraping

connection = {
    "user": "MON_USER",
    "password": "MON_MOT_DE_PASSE",
    "host": "localhost",
    "port": 1521,
    "service": "XEPDB1",
    "table_name": "MASTER_POKEMON"
}

inst = PokemonScraping("https://pokemondb.net/pokedex/national")
inst.run_scraping()
inst.save_dataframe_to_oracle(connection)

print(inst.dataframe.head())
```

------------------------------------------------------------------------

## 🗄️ Connexion Oracle (exemple)

``` python
import oracledb

conn = oracledb.connect(
    user="USER",
    password="MOTDEPASSE",
    dsn="localhost:1521/XEPDB1"
)

print("Connecté !")
conn.close()
```

------------------------------------------------------------------------

## 📊 Exemple de Données

  Pokémon     Taille   Poids     Espèce
  ----------- -------- --------- -------------------
  Charizard   1.7 m    90.5 kg   Flame Pokémon
  Blastoise   1.6 m    85.5 kg   Shellfish Pokémon
  Venusaur    2.0 m    100 kg    Seed Pokémon

------------------------------------------------------------------------

## 📚 Ce que ce projet permet de découvrir

-   Structurer un scraper de manière scalable\
-   Extraire dynamiquement plusieurs tables HTML\
-   Concevoir un pipeline complet : **scraper → nettoyer → charger**\
-   Gérer des problèmes réels de connexion Oracle (encoding, DSN, mot de
    passe spécial...)\
-   Appliquer rigoureusement les bonnes pratiques Python

------------------------------------------------------------------------

## 🌟 Pistes d'Amélioration

-   Scraping asynchrone avec `asyncio` pour accélérer\
-   Export dans PostgreSQL, MySQL, SQLite\
-   Pipeline automatisé (Airflow, Luigi)\
-   Dashboard (Power BI, Grafana)

------------------------------------------------------------------------

### 🎥 Démonstration Vidéo

[![Démonstration](https://tenor.com/p90BYzdn4hk.gif)](https://drive.google.com/file/d/1K7v64KhIAHksUdIjpBsi3Ub7jHBQfBVc/view?usp=drive_link)





## 👤 Auteur

**Paulo Rodriguez**
