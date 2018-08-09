import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
import clean as c


def create_clusters(df1=None,df2=None,df3=None,n_clusters = 5):
    """
    input: previous 3 seasons already cleaned

    try to classify teams based off last 3 seasons (or fewer for first few season)

    output: KMeans model and the dataframe containing averages over last 3 seasons
    """
    game_avgs1 = c.get_team_avgs(df1)
    game_avgs2 = c.get_team_avgs(df2)
    game_avgs3 = c.get_team_avgs(df3)
    home_1,away_1 = c.get_avgs_home_vs_away(df1)
    home_2,away_2  = c.get_avgs_home_vs_away(df2)
    home_3,away_3  = c.get_avgs_home_vs_away(df3)
    teams = game_avgs1.index
    s_comb=game_avgs1
    s_comb=s_comb.append(game_avgs2).append(game_avgs1)
    s_comb=s_comb.groupby('team').mean()
    home = home_1
    home=home.append(home_2).append(home_3)
    home=home.groupby('team').mean()
    away = away_1
    away=away.append(away_2).append(away_3)
    away=away.groupby('team').mean()
    s_comb['+/-_diff']=home['+/-']-away['+/-']
    s_comb_norm = s_comb[['3PT_attempts','Possessions','FT_attempts','AST','REB','+/-_diff']]
    s_comb_norm=normalize(s_comb_norm)
    km = KMeans(n_clusters=n_clusters,n_init=20)
    km.fit(s_comb_norm)
    return home,away, km
