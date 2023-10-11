"""
Webscraping Project for Swiss Amateur Soccer
============================================

transform.py
----------
Transforms extracted data to display rankings and topscorers 
in a streamlit app

"""

import pandas as pd

#Read data from excel files

rankings = {
    "ranking_2021": pd.DataFrame(),
    "ranking_2020": pd.DataFrame(),
    "ranking_2019": pd.DataFrame(),
}

games = {
    "games_2021": pd.DataFrame(),
    "games_2020": pd.DataFrame(),
    "games_2019": pd.DataFrame(),
}

for ranking in rankings.keys():

    rankings[ranking] = pd.read_csv(fr"data_files\{ranking}.csv", index_col=0)

for game in games.keys():

    games[game] = pd.read_csv(fr"data_files\{game}.csv", index_col=0)


def transform_rankings(rankings):

    """
    Transforms rankings 

    Parameters
    ----------
    rankings : dict
        rankings for different seasons

    Returns
    -------
    rankings : dict
        transformed rankings

    """ 
   
    for ranking in rankings.keys():

        rankings[ranking].astype(
            dtype={
                "Spiele": int,
                "Siege": int,
                "Niederlagen": int,
                "Unentschieden": int,
                "Strafpunkte": int,
                "Tore": int,
                "Gegentore": int,
                "Tordifferenz": int,
                "Punkte": int,
            }
        )

        rankings[ranking].set_index(["Rang"], drop=True, inplace=True)
        rankings[ranking].rename(
            columns={
                "Spiele": "Sp",
                "Siege": "S",
                "Niederlagen": "N",
                "Unentschieden": "U",
                "Strafpunkte": "Straf-Pkt.",
                "Tore": "T",
                "Gegentore": "GT",
                "Tordifferenz": "Diff.",
                "Punkte": "Pkt.",
            },
            inplace=True,
        )
        # rankings[ranking]['S%'] = rankings[ranking]['S'].values / \
        #     rankings[ranking]['Sp'].values
        # rankings[ranking]['SW'] = rankings[ranking]['T'].values**2 / \
        #     (rankings[ranking]['T'].values ** 2 +  rankings[ranking]['GT'].values **2)

    return rankings


def clean_alt_list(string_):
    """Cleans lists from whitespaces and newlines"""
    list_ = string_.split(",")

    for i in range(len(list_)):
        list_[i] = list_[i].strip()

        if "Penalty" in list_[i]:
            list_[i] = list_[i].replace("  ", "").replace("\n", "")

        if "Eigentor" in list_[i]:
            list_[i] = list_[i].replace("  ", "").replace("\n", "")

    return list_


def transform_games(games):
    """
    Transforms games 

    Parameters
    ----------
    games : dict
        games for different seasons

    Returns
    -------
    games : dict
        transformed games
    player_stats : dict
        players stats

    """    
    
    player_stats = {
        "games_2021": pd.DataFrame(),
        "games_2020": pd.DataFrame(),
        "games_2019": pd.DataFrame(),
    }

    for season in games.keys():
        games[season] = games[season].drop_duplicates()
        games[season] = games[season].fillna("")

        player_list = []

        for col in games[season].columns:

            if col == "TorschützenHeim":
                games[season][col] = games[season][col].apply(clean_alt_list)

                player_list = player_list + [
                    x for sublist in games[season][col] for x in sublist if x != ""
                ]

            if col == "TorschützenGast":
                games[season][col] = games[season][col].apply(clean_alt_list)

                player_list = player_list + [
                    x for sublist in games[season][col] for x in sublist if x != ""
                ]

        player_list = set(player_list)

        for player in player_list:
            player = player.replace(" (Penalty)", "")
            player = player.replace("Eigentor (", "").replace(")", "")

            goal_home = (
                games[season]["TorschützenHeim"].apply(lambda x: x.count(player)).sum()
            )

            goal_away = (
                games[season]["TorschützenGast"].apply(lambda x: x.count(player)).sum()
            )

            home_penalty = (
                games[season]["TorschützenHeim"]
                .apply(lambda x: x.count(f"{player} (Penalty)"))
                .sum()
            )

            away_penalty = (
                games[season]["TorschützenGast"]
                .apply(lambda x: x.count(f"{player} (Penalty)"))
                .sum()
            )

            home_owngoal = (
                games[season]["TorschützenHeim"]
                .apply(lambda x: x.count(f"Eigentor ({player})"))
                .sum()
            )

            away_owngoal = (
                games[season]["TorschützenGast"]
                .apply(lambda x: x.count(f"Eigentor ({player})"))
                .sum()
            )

            penalty = home_penalty + away_penalty
            owngoal = away_owngoal + home_owngoal

            goal_home = goal_home + home_penalty
            goal_away = goal_away + away_penalty

            goals = goal_home + goal_away

            df = pd.DataFrame(
                [
                    {
                        "Spieler": player,
                        "AnzahlTore": goals,
                        "Heim": goal_home,
                        "Auswärts": goal_away,
                        "Penalty": penalty,
                        "Eigentor": owngoal,
                    }
                ]
            )

            player_stats[season] = pd.concat([player_stats[season], df])

        player_stats[season] = player_stats[season].drop_duplicates()
        player_stats[season].set_index(["Spieler"], drop=True, inplace=True)
        player_stats[season] = player_stats[season].sort_values(
            by=["AnzahlTore"], ascending=False
        )

    return games, player_stats


rankings_transformed = transform_rankings(rankings)
games_transformed, player_stats = transform_games(games)
