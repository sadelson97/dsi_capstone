import pandas as pd
import numpy as np


def group_dataframe(df):
    '''
    input: season dataframe

    need to group dataframe correctly to do rolling means

    output: dataframe grouped by days, game_id, team
    '''
    games=df.groupby(['days_after_opener','game_id','team']).sum() #group so its ordered on date, then game id, then team
    games['+/-']/=5 #+/- is 5 times too large because there are 5 players on the court at all times
    return games


def get_team_games(df,team):
    '''
    input: grouped season dataframe, team to get games for

    return a dataframe ordered by days and grouped on game_id and team

    output: return the dataframe with only that team
    '''

    team_df = df[df.index.get_level_values('team')==team] #only select games where team index equals team you are looking for
    return team_df


def rolling_means(team_df,games_back=7,needed_games=5):
    '''
    input: team dataframe

    create rolling means for each team

    output: rolling mean
    '''
    roll = team_df.rolling(games_back,needed_games).mean() #rolling means
    roll['PTS_scored']= team_df.groupby(['days_after_opener','game_id','team']).sum()['PTS'] #need to calc score for each team so i can calc difference of average and that
    diffs = roll['PTS']-roll['PTS_scored']  #differences of average - actual
    roll.drop('PTS_scored',axis=1,inplace=True) #only need this feature for previous calculation
    #the order of the differences is wrong. need to switch even and odd places
    diffs_even = diffs[::2].values #even indices
    diffs_odd = diffs[1::2].values #odd indices
    fixed_diff=[]
    for i in range(len(diffs_odd)):
        fixed_diff.append(diffs_odd[i]) #make odd first
        fixed_diff.append(diffs_even[i]) #and even second
    fixed_diff=pd.Series(fixed_diff,index=diffs.index).rolling(games_back,needed_games).mean() #get rolling average of it
    roll['DEF_PTS']=fixed_diff #add in feature
    overtime = team_df['Min']>250 #make overtime so i can not train on these games
    roll=roll.shift(1) #shift it so current game is not taken into account in rolling mean
    roll['overtime']=pd.Series(overtime)
    roll.drop('Total_PTS',axis=1,inplace=True) #dont want rolling average of Total points
    return roll


def all_team_rolling(df,games_back=7,games_needed=5):
    '''
    input: season dataframe

    given season dataframe find the rolling means for all teams

    return: dictionary containing all rolling mean dataframes
    '''
    games = group_dataframe(df) #group the dataframe
    team_roll={}
    for team in games.index.get_level_values('team'): #get each team
        t = get_team_games(games,team) #dataframe for each team
        team_roll[team]=rolling_means(t,games_back,games_needed) #add to dictionary to make dataframe later
    return team_roll


def complete_rolling_means(df,games_back=7,games_needed=5):
    '''
    input: season dataframe

    convert dataframe into a dataframe that can be used for modeling

    output: dataframe with games and rolling means for teams
    '''

    team_roll = all_team_rolling(df,games_back,games_needed) #do previous function
    frames = []
    for team in team_roll: #make the dataframe
        frames.append(team_roll[team])
    roll_means_df = pd.concat(frames)
    df_merged = roll_means_df.groupby([roll_means_df.index.get_level_values('days_after_opener'),
                        roll_means_df.index.get_level_values('game_id'),
                        roll_means_df.index.get_level_values('team')]).sum() #group it so it is in the right order
    scores_df=df[['game_id','team','Total_PTS','days_after_opener']] 
    scores_df = scores_df.groupby(['days_after_opener','game_id','team']).mean() #add scores to the feature matrix so I can train
    return df_merged.join(scores_df)
