import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
import clean as c


def create_clusters(df1=None,df2=None,df3=None):
    """
    input: previous 3 seasons already cleaned

    try to classify teams based off last 3 seasons (or fewer for first few season)

    output: KMeans model and the dataframe containing averages over last 3 seasons
    """

    game_avgs1 = c.get_team_avgs(df1)
    game_avgs2 = c.get_team_avgs(df2)
    game_avgs3 = c.get_team_avgs(df3)
    teams = game_avgs1.index
    s_comb=game_avgs3
    s_comb=s_comb.append(game_avgs2).append(game_avgs1)
    s_comb=s_comb.groupby('team').mean()
    s_comb_norm = s_comb.drop(['FT_made','3PT_made','FG_made'],axis=1)
    s_comb_norm=normalize(s_comb_norm)
    km = KMeans(n_clusters=5,n_init=20)
    km.fit(s_comb_norm)
    return s_comb, km
