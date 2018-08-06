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

def calc_days_from_opener(season):
    """
    input: dataframe of season

    make days after opener feature to use for rest

    output: none
    """
    season['date']=pd.Series([parse(season['date'][i]) for i in range(len(season))])
    season['days_after_opener'] = season['date']-season['date'].min()
    season.drop('date',axis=1,inplace=True)

def make_splits(season):
    """
    input: dataframe of season

    split FG, FT, 3PT into makes and attempts

    output: none
    """

    season.fillna('0',inplace=True) #string so it can be split later
    season['Min']=season['Min'].map(lambda x: '0' if x.find('DNP')!= -1 else x)

    season['FT_made']=season['FT'].map(lambda x: x.split('-')[0])
    season['FT_attempts']=season['FT'].map(lambda x: x.split('-')[-1]) #when filled na with '0'

    season['3PT_made']=season['3PT'].map(lambda x: x.split('-')[0])
    season['3PT_attempts']=season['3PT'].map(lambda x: x.split('-')[-1]) #when filled na with '0'

    season['FG_made']=season['FG'].map(lambda x: x.split('-')[0])
    season['FG_attempts']=season['FG'].map(lambda x: x.split('-')[-1]) #when filled na with '0'

    season.drop(['FT','FG','3PT'],axis=1,inplace=True)

def convert_to_int(season):
    """
    input: dataframe of season

    convert numerical stats to into

    output: dataframe with ints
    """
    season=season[season['Min']!='--'] #drop rows where all stats are ---
    season[['+/-','AST','BLK','DREB','Min','OREB','PF','PTS','REB','STL','TO','FT_made',
            'FT_attempts','3PT_made','3PT_attempts','FG_made','FG_attempts']]=season[['+/-',
            'AST','BLK','DREB','Min','OREB','PF','PTS','REB','STL','TO','FT_made',
            'FT_attempts','3PT_made','3PT_attempts','FG_made','FG_attempts']].astype(int)
    return season

def add_total_score(season):
    """
    input: dataframe of season

    add a total score feature to DataFrame

    output: dataframe with total score
    """
    grouped_games_score = season.groupby('game_id')
    game_totals=pd.DataFrame(grouped_games_score.sum()['PTS'])
    game_totals['Total_PTS']=game_totals['PTS']  #These two lines are because name 'PTS' needs to be changed
    game_totals.drop('PTS',axis=1,inplace=True)  #
    season=season.join(game_totals,on='game_id')
    return season

def get_team_avgs(season):
    """
    input: dataframe of season

    get teams average stats

    output: dataframe containing average stats
    """
    grouped_teams = season.groupby('team')
    game_avgs=pd.DataFrame(grouped_teams.sum())
    game_avgs = game_avgs[['AST','BLK','DREB','OREB','PF','REB','STL','TO',
            'FT_made','FT_attempts','3PT_made','3PT_attempts','FG_made','FG_attempts']]/82
    game_avgs['AVG_score']=grouped_teams.sum()['PTS']/82
    return game_avgs
