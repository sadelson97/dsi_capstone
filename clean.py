import pandas as pd
import numpy as np
from dateutil.parser import parse

def change_pos_position(season): #some season have position labeled as pos
    try:
        season['Position']=season['Pos']
        season.drop('Pos',axis=1,inplace=True)
    except:
        pass

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
    season['Min']=season['Min'].map(lambda x: '0' if x.find('Did')!= -1 else x)

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
    season['+/-']=season['+/-'].map(lambda x: '0' if x == '--' else x) #some seasons don't have +/-
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
    game_avgs['Possessions']=game_avgs['FG_attempts']+game_avgs['TO'] #add estimate for possessions
    return game_avgs

def get_team_avgs_2012(season): #for 2011/2012 season (nba lock out)
    """
    input: dataframe of season

    get teams average stats

    output: dataframe containing average stats
    """
    grouped_teams = season.groupby('team')
    game_avgs=pd.DataFrame(grouped_teams.sum())
    game_avgs = game_avgs[['AST','BLK','DREB','OREB','PF','REB','STL','TO',
            'FT_made','FT_attempts','3PT_made','3PT_attempts','FG_made','FG_attempts']]/66
    game_avgs['AVG_score']=grouped_teams.sum()['PTS']/66
    game_avgs['Possessions']=game_avgs['FG_attempts']+game_avgs['TO'] #add estimate for possessions
    return game_avgs

def get_avgs_home_vs_away(season):
    """
    input: dataframe of season

    get team average stats based on away vs home games

    output: dataframe containing these stats
    """
    small_df=season[['game_id','team','home_team','Total_PTS']]
    grouped_teams_home = season.groupby(['team','home_team'])
    avgs = grouped_teams_home.sum()[['AST','BLK','DREB','OREB','PF','REB','STL','TO',
            'FT_made','FT_attempts','3PT_made','3PT_attempts','FG_made','FG_attempts']]/41
    avgs['AVG_score']=grouped_teams_home.sum()['PTS']/41
    joined_data = small_df.join(avgs,on=['team','home_team'])
    grouped_join = joined_data.groupby(['game_id','team']).mean()
    return grouped_join

def get_avgs_home_vs_away_2012(season):
    """
    input: dataframe of season

    get team average stats based on away vs home games

    output: dataframe containing these stats
    """
    small_df=season[['game_id','team','home_team','Total_PTS']]
    grouped_teams_home = season.groupby(['team','home_team'])
    avgs = grouped_teams_home.sum()[['AST','BLK','DREB','OREB','PF','REB','STL','TO',
            'FT_made','FT_attempts','3PT_made','3PT_attempts','FG_made','FG_attempts']]/41
    avgs['AVG_score']=grouped_teams_home.sum()['PTS']/33
    joined_data = small_df.join(avgs,on=['team','home_team'])
    grouped_join = joined_data.groupby(['game_id','team']).mean()
    return grouped_join

def change_teamname(season):
    """
    input: dataframe of season

    Supersonics switched cities and names to Thunder, Bobcats to Hornets

    output: none
    """

    season['team']=season['team'].map(lambda x: 'Thunder' if x == 'SuperSonics' else x)
    season['team']=season['team'].map(lambda x: 'Hornets' if x == 'Bobcats' else x)

def change_hornets_pelicans(season): #use for 2004-2013
    """
    input: dataframe of season

    The Hornets refer to two different teams. From 2002-2013 it was
    New Orleans, which are now the pelicans

    output: none
    """
    season['team']=season['team'].map(lambda x: 'Pelicans' if x == 'Hornets' else x)

def all_clean(season):
    """
    input: dataframe of season

    combine all functions into one

    output: cleaned dataframe
    """
    change_pos_position(season)
    change_teamname(season)
    create_hometeam(season)
    calc_days_from_opener(season)
    make_splits(season)
    season=convert_to_int(season)
    season=add_total_score(season)
    return season

def all_clean_pels(season):
    """
    input: dataframe of season

    combine all functions into one for when the pelicans were the hornets

    output: cleaned dataframe
    """
    change_pos_position(season)
    change_hornets_pelicans(season)
    change_teamname(season)
    create_hometeam(season)
    calc_days_from_opener(season)
    make_splits(season)
    season=convert_to_int(season)
    season=add_total_score(season)
    return season
