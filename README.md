# ETL-league-of-legends
 
Ce projet extrait les données des joueurs Challenger de League of Legends à partir de l'API Riot, les traite et les enregistre dans différents formats (CSV, Excel, SQLite). Les données brutes sont également enregistrées dans un fichier JSON pour une référence future.
 
## Table des matières
 
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [Authors](#Authors)
 
## Prérequis
 
- Python 3
- `pip` pour installer les dépendances
- Clé API Riot Games (vous pouvez obtenir une clé API en vous inscrivant sur le [site des développeurs Riot](https://developer.riotgames.com/))

 
## Installation
 
1. Clonez ce dépôt :
   ```sh
   git clone https://github.com/Decorentin/ETL-league-of-legends
   ```
   ```sh
   cd ETL-league-of-legends
   ```
 
2. Créez et activez un environnement virtuel :
   ```sh
   python3 -m venv  Nom_De_l'environnement
   ```
   ```sh
   source Nom_De_l'environnement/bin/activate 
   ````
 
3. Installez les dépendances :
   ```sh
   pip install -r requirements.txt
   ```
 
## Utilisation
Remplacez la variable API_KEY dans le fichier program.py par votre clé API Riot Games.
 
Exécutez le script :
 
```sh
python3 program.py
```
Suivez les instructions à l'écran pour choisir la région, le nombre de joueurs à afficher et le format de sortie (CSV, Excel, SQLite).
 
## Structure du projet
 
ETL-league-of-legends/

│
├── data/
│   ├── interim/
│   │   └── {region}_raw_data.json
│   └── processed/
│       └── {filename}.{csv|xlsx|db}
│

├── requirements.txt

├── README.md

└── program.py
 
data/interim/ : Contient les données brutes extraites de l'API.
data/processed/ : Contient les données traitées enregistrées dans les formats CSV, Excel ou SQLite.
requirements.txt : Liste des dépendances du projet.
README.md : Fichier README du projet.
program.py : Script principal du projet.
 
N'hésitez pas à ouvrir une issue ou à me contacter si vous avez des questions ou des suggestions d'amélioration.
 
 
## Authors
 
- [@Decorentin](https://github.com/Decorentin)
- [@TerminaTorr45](https://github.com/TerminaTorr45)
- [@M4xxes](https://github.com/M4xxes)
- [@Tokennn](https://github.com/Tokennn)