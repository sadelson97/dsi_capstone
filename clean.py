import pandas as pd
import numpy as np
from dateutil.parser import parse

def create_hometeam(season):
    """
    input: dataframe of season

    create hometeam feature

    output: none
    """
    grouped = season.groupby('game_id')
    home_team=[]
    for group in list(grouped.groups.fromkeys(season['game_id']).keys()): #need the game_id in the same order as the dataframe
        values = grouped.groups[group].get_values()
        home_team.append([False if season.iloc[values]['team'].iloc[i] ==  season.iloc[values]['team'].iloc[0] else True for i in range(len(values))])
    home_team = [item for sublist in home_team for item in sublist] #need to flatten list of lists into just a single list
    season['home_team']=pd.Series(home_team)

def calc_days_after_opener(season):
    """
    input: dataframe of season

    make days after opener feature to use for rest

    output: none
    """
    season['date']=pd.Series([parse(season['date'][i]) for i in range(len(season))])
    season['days_after_opener'] = season['date']-season['date'].min()

def make_splits(season):
    """
    input: dataframe of season

    split FG, FT, 3PT into makes and attempts

    output: none
    """

    season.fillna('0',inplace=True) #string so it can be split later
    season.replace("DNP-COACH'S DECISION",0,inplace=True)

    season['FT_made']=season['FT'].map(lambda x: x.split('-')[0])
    season['FT_attempts']=season['FT'].map(lambda x: x.split('-')[-1]) #when filled na with '0'

    season['3PT_made']=season['3PT'].map(lambda x: x.split('-')[0])
    season['3PT_attempts']=season['3PT'].map(lambda x: x.split('-')[-1]) #when filled na with '0'

    season['FG_made']=season['FG'].map(lambda x: x.split('-')[0])
    season['FG_attempts']=season['FG'].map(lambda x: x.split('-')[-1]) #when filled na with '0'
