"""Displays Rankins an Topscorers for Seasons 2019, 2020 an 2021"""

import pandas as pd
import plotly.express as px
import streamlit as st

from transform import player_stats, rankings_transformed

st.set_page_config(layout="wide")

st.image(r"jannes-glas-cuhQcfp3By4-unsplash_cut_2.jpg")

st.title(
    """
Swiss Amateur Soccer Topscorer
"""
)

st.write(
    """

"""
)

st.sidebar.header(
    """
Select Season and set goals treshhold or filter for players
"""
)

st.header(
    """
5. Liga
"""
)

seasons = ["2021", "2020", "2019"]
selected_season = st.sidebar.selectbox("Select Season", (seasons))


@st.cache
def load_season_data(selected_season):
    """Load data from selected season"""

    selected_season_data = rankings_transformed[f"ranking_{selected_season}"]
    return selected_season_data


selected_season_data = load_season_data(selected_season)
st.subheader(f"Saison {selected_season}")
st.write("Rangliste")
st.dataframe(selected_season_data)

goals_slider = st.sidebar.slider(
    "Goals Treshhold",
    1,
    int(player_stats[f"games_{selected_season}"]["AnzahlTore"].max()),
    key="goals_slider",
)


@st.cache
def load_topscorer_data(goals_treshold, selected_season):

    """Load topscorer data from selected goals treshold"""

    topscorer_data = player_stats[f"games_{selected_season}"][
        player_stats[f"games_{selected_season}"]["AnzahlTore"] >= goals_treshold
    ]
    topscorer_data = topscorer_data.sort_values(by=["AnzahlTore"], ascending=False)

    return topscorer_data


topscorer_data = load_topscorer_data(goals_slider, selected_season)

players_selection = player_stats[f"games_{selected_season}"].reset_index()
players_selection = players_selection[players_selection["AnzahlTore"] > 0]
default = pd.DataFrame(
    {
        "Spieler": "<select>",
        "AnzahlTore": 0,
        "Heim": 0,
        "Auswärts": 0,
        "Penalty": 0,
        "Eigentor": 0,
    },
    index=["Spieler"],
)

players_selection = pd.concat([players_selection, default])
players_selection = players_selection.set_index(["Spieler"])
players_selection = players_selection.sort_values(by=["AnzahlTore"], ascending=True)

selected_player = st.sidebar.selectbox(
    "Players", (players_selection.index), key="default_player"
)


@st.cache
def load_player_data(selected_player):

    """Load player stats from selected player"""

    player_stat = player_stats[f"games_{selected_season}"].reset_index()
    player_stat = player_stat[player_stat["Spieler"] == selected_player]
    player_stat = player_stat.set_index(["Spieler"])

    return player_stat


player_stat = load_player_data(selected_player)


def reset_selections():
    """Reset selections of goalstreshold and player"""

    st.session_state.default_player = "<select>"
    st.session_state.goals_slider = 1


reset = st.sidebar.button("reset", on_click=reset_selections)


def load_bar_charts(topscorer_data, selected_player, player_stat):
    """Load bar charts"""

    if reset or selected_player == "<select>":
        fig = px.bar(
            topscorer_data,
            x=topscorer_data.index,
            y=["Heim", "Auswärts"],
            hover_data=["Penalty"],
            labels={"value": "Tore"},
            title="Torschützen",
        )
        fig.update_traces(width=0.5)

    else:

        fig = px.bar(
            player_stat,
            x=player_stat.index,
            y=["Heim", "Auswärts"],
            hover_data=["Penalty"],
            labels={"value": "Tore", "Index": selected_player},
            title="Topscorer",
        )

        fig.update_traces(width=0.2)

    return fig


st.plotly_chart(
    load_bar_charts(topscorer_data, selected_player, player_stat),
    use_container_width=True,
)

st.write("Torschützen-Liste")
topscorer_list = topscorer_data.reset_index()
topscorer_list.index = topscorer_list.index + 1
if selected_player == '<select>':
    st.dataframe(topscorer_list[topscorer_list['AnzahlTore'] >= goals_slider])
else:
    st.dataframe(player_stat)
