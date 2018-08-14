import pandas as pd
import numpy as np


def group_dataframe(df):
    '''
    input: season dataframe

    need to group dataframe correctly to do rolling means

    output: dataframe grouped by days, game_id, team
    '''
    games=df.groupby(['days_after_opener','game_id','team']).sum()
    games['+/-']/=5
    return games


def get_team_games(df,team):
    '''
    input: grouped season dataframe, team to get games for

    return a dataframe ordered by days and grouped on game_id and team

    output: return the dataframe with only that team
    '''

    team_df = df[df.index.get_level_values('team')==team]
    return team_df


def rolling_means(team_df,games_back=7,needed_games=5):
    '''
    input: team dataframe

    create rolling means for each team

    output: rolling mean
    '''
    roll = team_df.rolling(games_back,needed_games).mean()
    roll['PTS_scored']= team_df.groupby(['days_after_opener','game_id','team']).sum()['PTS']
    diffs = roll['PTS']-roll['PTS_scored']
    roll.drop('PTS_scored',axis=1,inplace=True)
    diffs_even = diffs[::2].values
    diffs_odd = diffs[1::2].values
    fixed_diff=[]
    for i in range(len(diffs_odd)):
        fixed_diff.append(diffs_odd[i])
        fixed_diff.append(diffs_even[i])
    fixed_diff=pd.Series(fixed_diff,index=diffs.index).rolling(games_back,needed_games).mean()
    roll['DEF_PTS']=fixed_diff
    roll.drop('Total_PTS',axis=1,inplace=True)
    return roll.shift(1)


def all_team_rolling(df,games_back=7,games_needed=5):
    '''
    input: season dataframe

    given season dataframe find the rolling means for all teams

    return: dictionary containing all rolling mean dataframes
    '''
    games = group_dataframe(df)
    team_roll={}
    for team in games.index.get_level_values('team'):
        t = get_team_games(games,team)
        team_roll[team]=rolling_means(t,games_back,games_needed)
    return team_roll


def complete_rolling_means(df,games_back=7,games_needed=5):
    '''
    input: season dataframe

    convert dataframe into a dataframe that can be used for modeling

    output: dataframe with games and rolling means for teams
    '''

    team_roll = all_team_rolling(df,games_back,games_needed)
    frames = []
    for team in team_roll:
        frames.append(team_roll[team])
    roll_means_df = pd.concat(frames)
    df_merged = roll_means_df.groupby([roll_means_df.index.get_level_values('days_after_opener'),
                        roll_means_df.index.get_level_values('game_id'),
                        roll_means_df.index.get_level_values('team')]).sum()
    scores_df=df[['game_id','team','Total_PTS','days_after_opener']]
    scores_df = scores_df.groupby(['days_after_opener','game_id','team']).mean()
    return df_merged.join(scores_df)
