"""Scraps data from SFVBJ Website"""
from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup
import re
from web_driver import driver

base_link = "https://www.fvbj-afbj.ch/fussballverband-bern-jura/spielbetrieb-fvbj/"

season_ranking_links = [
    base_link
    + "meisterschaft-fvbj.aspx/oid-6/s-2021/ln-13040/ls-19023/sg-55340/a-mrr/",
    base_link
    + "meisterschaft-fvbj.aspx/oid-6/s-2020/ln-13040/ls-18117/sg-52982/a-mrr/",
    base_link
    + "meisterschaft-fvbj.aspx/oid-6/s-2019/ln-13040/ls-17083/sg-50320/a-mrr/",
]

season_games_links = [
    base_link
    + "meisterschaft-fvbj.aspx/oid-6/s-2020/ln-13040/ls-18117/sg-52982/a-msp/",
    base_link
    + "meisterschaft-fvbj.aspx/oid-6/s-2021/ln-13040/ls-19023/sg-55340/a-msp/",
    base_link
    + "meisterschaft-fvbj.aspx/oid-6/s-2019/ln-13040/ls-17083/sg-50320/a-msp/",
]

base_url = "https://www.fvbj-afbj.ch/"


def extract_rankings(season_ranking_links):
    """Extrats data for  seasosn 2019, 2020 and 2021"""

    rankings = {
        "ranking_2021": pd.DataFrame(),
        "ranking_2020": pd.DataFrame(),
        "ranking_2019": pd.DataFrame(),
    }

    print("Get Ratings Data")
    for link in tqdm(season_ranking_links):
        driver.get(link)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "lxml")

        seed = [
            seed.text.replace(".", "")
            for seed in soup.find_all(attrs={"class": "ranCrang"})
        ]
        team = [team.text for team in soup.find_all(attrs={"class": "ranCteam"})]
        games = [games.text for games in soup.find_all(attrs={"class": "ranCsp"})]
        wins = [wins.text for wins in soup.find_all(attrs={"class": "ranCs"})]
        losses = [losses.text for losses in soup.find_all(attrs={"class": "ranCu"})]
        draws = [draws.text for draws in soup.find_all(attrs={"class": "ranCn"})]
        violation_points = [
            violation_points.text.replace("(", "").replace(")", "")
            for violation_points in soup.find_all(attrs={"class": "ranCstrp"})
        ]
        golas_made = [
            golas_made.text for golas_made in soup.find_all(attrs={"class": "ranCtg"})
        ]
        goals_against = [
            goals_against.text
            for goals_against in soup.find_all(attrs={"class": "ranCte"})
        ]
        goal_difference = [
            goal_difference.text
            for goal_difference in soup.find_all(attrs={"class": "ranCtdf"})
        ]
        points = [points.text for points in soup.find_all(attrs={"class": "ranCpt"})]

        ranking = pd.DataFrame(
            {
                "Rang": seed,
                "Team": team,
                "Spiele": games,
                "Siege": wins,
                "Niederlagen": losses,
                "Unentschieden": draws,
                "Strafpunkte": violation_points,
                "Tore": golas_made,
                "Gegentore": goals_against,
                "Tordifferenz": goal_difference,
                "Punkte": points,
            }
        )

        if "2021" in link:
            rankings["ranking_2021"] = ranking

        if "2020" in link:
            rankings["ranking_2020"] = ranking

        if "2019" in link:
            rankings["ranking_2019"] = ranking

    return rankings


def get_games_links(base_url):
    """Gets links for every game of seasosn 2019, 2020 and 2021"""

    games_links_cleaned = {
        "season_2021": [],
        "season_2020": [],
        "season_2019": [],
    }

    for game_link in tqdm(season_games_links):
        driver.get(game_link)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "lxml")
        links = soup.find_all(href=True)

        print("Clean Games Links")
        pattern = "fussballverband-bern-jura/spielbetrieb-fvbj/meisterschaft-fvbj.aspx/ln-13040/v-0"
        games_links = [link["href"] for link in links if re.search(pattern, str(link))]

        if "2021" in game_link:
            games_links_cleaned["season_2021"] = [
                base_url + link for link in games_links
            ]

        if "2020" in game_link:
            games_links_cleaned["season_2020"] = [
                base_url + link for link in games_links
            ]

        if "2019" in game_link:
            games_links_cleaned["season_2019"] = [
                base_url + link for link in games_links
            ]

    return games_links_cleaned


def extract_games(games_links_cleaned):
    """Extrats games data for seasosn 2019, 2020 and 2021"""

    games = {
        "games_2021": pd.DataFrame(),
        "games_2020": pd.DataFrame(),
        "games_2019": pd.DataFrame(),
    }

    for season in games_links_cleaned.keys():

        print("Get Games Data")

        for link in tqdm(games_links_cleaned[season]):
            driver.get(link)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "lxml")

            result = soup.find(attrs={"class": "shortResults"})
            try:
                result = result.text
            except:
                result = "-"

            home_team = soup.find(attrs={"class": "shortTeamHeim"})
            try:
                home_team = home_team.text
            except:
                home_team = "-"

            away_team = soup.find(attrs={"class": "shortTeamGast"})
            try:
                away_team = away_team.text
            except:
                away_team = "-"

            try:
                home_scorers = [
                    home_scorer.text
                    for home_scorer in soup.find_all(
                        attrs={"class": "shortSpielerHome"}
                    )
                ]
                home_scorers = ",".join(home_scorers)
            except:
                home_scorers = "-"

            try:
                away_scorers = [
                    away_scorer.text
                    for away_scorer in soup.find_all(
                        attrs={"class": "shortSpielerGast"}
                    )
                ]
                away_scorers = ",".join(away_scorers)
            except:
                away_scorers = "-"

            df = pd.DataFrame(
                [
                    {
                        "Heimteam": home_team,
                        "Gastteam": away_team,
                        "Resultat": result,
                        "TorschützenHeim": home_scorers,
                        "TorschützenGast": away_scorers,
                    }
                ]
            )

            if season == "season_2021":
                games["games_2021"] = pd.concat([games["games_2021"], df])

            if season == "season_2020":
                games["games_2020"] = pd.concat([games["games_2020"], df])

            if season == "season_2019":
                games["games_2019"] = pd.concat([games["games_2019"], df])

            print(f"{season} Games")

    return games


rankings = extract_rankings(season_ranking_links)
games = extract_games(get_games_links(base_url))
