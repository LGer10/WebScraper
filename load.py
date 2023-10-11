"""
Webscraping Project for Swiss Amateur Soccer
============================================

load.py
----------
Loads extracted data to excel files

"""

import pandas as pd
from extract import rankings, games


def load_rankings(rankings):
    """
    Loads rankings to excel file

    Parameters
    ----------
    rankings : dict
        rankings for different seasons

   """

    for ranking in rankings.keys():

        if ranking == "ranking_2021":
            rankings[ranking].to_csv(r"WebScraper\data_files\ranking_2021.csv")

        if ranking == "ranking_2020":
            rankings[ranking].to_csv(r"WebScraper\data_files\ranking_2020.csv")

        if ranking == "ranking_2019":
            rankings[ranking].to_csv(
                r"WebScraper\data_files\ranking_2019.csv")


def load_games(games):

    """
    Loads games to excel file

    Parameters
    ----------
    games : gamesings for different seasons

    """

    for season in games.keys():

        if season == "games_2021":
            games[season].to_csv(r"WebScraper\data_files\games_2021.csv")

        if season == "games_2020":
            games[season].to_csv(r"WebScraper\data_files\games_2020.csv")

        if season == "games_2019":
            games[season].to_csv(r"WebScraper\data_files\games_2019.csv")


load_rankings(rankings)
load_games(games)
