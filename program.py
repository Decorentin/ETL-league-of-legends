import requests
import csv
import pandas as pd
import sqlite3

# Configuration
API_KEY = ""  # Remplacez par votre clé API valide
QUEUE_TYPE = "RANKED_SOLO_5x5"  # File classée Solo/Duo

def get_challenger_league(region):
    """Récupère les informations des joueurs dans la ligue Challenger."""
    base_url = f"https://{region}.api.riotgames.com"
    url = f"{base_url}/lol/league/v4/challengerleagues/by-queue/{QUEUE_TYPE}"
    headers = {"X-Riot-Token": API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Erreur HTTP : {e}")
        if response.status_code == 403:
            print("Vérifiez votre clé API. Elle est peut-être invalide ou expirée.")
        elif response.status_code == 404:
            print("Endpoint introuvable. Vérifiez l'URL ou la région.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erreur réseau : {e}")
        return None

def print_top_players(region, num_players):
    """Affiche les meilleurs joueurs classés."""
    data = get_challenger_league(region)
    if data:
        players = data.get("entries", [])
        # Trier par points de ligue (LP)
        sorted_players = sorted(players, key=lambda x: x.get("leaguePoints", 0), reverse=True)
        print(f"Top {num_players} joueurs Challenger en {region} :")
        players_data = []
        for rank, player in enumerate(sorted_players[:num_players], start=1):
            summoner_name = player.get("summonerName", "Nom inconnu")
            league_points = player.get("leaguePoints", 0)
            wins = player.get("wins", 0)
            losses = player.get("losses", 0)
            hot_streak = player.get("hotStreak", False)
            hot_streak_str = "Oui" if hot_streak else "Non"

            # Calculer le ratio de victoires/défaites
            if losses == 0:
                win_loss_ratio = "Infini"
            else:
                win_loss_ratio = wins / losses
                win_loss_ratio = "{:.2f}".format(win_loss_ratio) 

            print(f"{rank}. {summoner_name} - {league_points} LP - Victoires: {wins} - Défaites: {losses} - Série de victoires: {hot_streak_str} - Ratio Victoires/Défaites: {win_loss_ratio}")
            players_data.append({
                "Rank": rank,
                "SummonerName": summoner_name,
                "LeaguePoints": league_points,
                "Wins": wins,
                "Losses": losses,
                "HotStreak": hot_streak_str,
                "WinLossRatio": win_loss_ratio
            })
        return players_data
    else:
        print("Impossible de récupérer les données des joueurs.")
        return None

def save_to_csv(data, filename):
    """Enregistre les données dans un fichier CSV."""
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"Données enregistrées dans {filename}")

def save_to_excel(data, filename):
    """Enregistre les données dans un fichier Excel."""
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Données enregistrées dans {filename}")

def save_to_db(data, db_filename):
    """Enregistre les données dans une base de données SQLite."""
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS players (
                        Rank INTEGER,
                        SummonerName TEXT,
                        LeaguePoints INTEGER,
                        Wins INTEGER,
                        Losses INTEGER,
                        HotStreak TEXT,
                        WinLossRatio TEXT)''')
    cursor.executemany('''INSERT INTO players (Rank, SummonerName, LeaguePoints, Wins, Losses, HotStreak, WinLossRatio)
                          VALUES (:Rank, :SummonerName, :LeaguePoints, :Wins, :Losses, :HotStreak, :WinLossRatio)''', data)
    conn.commit()
    conn.close()
    print(f"Données enregistrées dans {db_filename}")

if __name__ == "__main__":
    # Demander à l'utilisateur de choisir la région et le nombre de joueurs
    region = input("Veuillez entrer la région (e.g., euw1, na1, kr): ")
    num_players = int(input("Veuillez entrer le nombre de joueurs à afficher: "))

    players_data = print_top_players(region, num_players)

    if players_data:
        # Demander à l'utilisateur de choisir le format de sortie
        output_format = input("Veuillez choisir le format de sortie (csv, excel, db): ").lower()
        if output_format == "csv":
            filename = input("Veuillez entrer le nom du fichier CSV (e.g., players.csv): ")
            save_to_csv(players_data, filename)
        elif output_format == "excel":
            filename = input("Veuillez entrer le nom du fichier Excel (e.g., players.xlsx): ")
            save_to_excel(players_data, filename)
        elif output_format == "db":
            db_filename = input("Veuillez entrer le nom de la base de données SQLite (e.g., players.db): ")
            save_to_db(players_data, db_filename)
        else:
            print("Format de sortie non pris en charge.")
