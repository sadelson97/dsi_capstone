import rolling_mean as rm
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.model_selection import GridSearchCV


def get_train_test(season,games_back=7,games_needed=5,train=False):
    '''
    input: season dataframe, games in rolling mean, and required games in rolling mean, and if this is to be trained on

    get the rolling mean of a season and tell whether it is to be trained on or not

    output: dataframe to use for model
    '''
    roll_season = rm.complete_rolling_means(season,games_back,games_needed) #get rolling means
    mat = roll_season.as_matrix() #to pair rows
    df_mat = []
    for i in range(int(len(mat)/2)): #need to pair rows of the same game
        df_mat.append(list(mat[2*i])+(list(mat[2*i+1])))
    cols = ('team1_'+roll_season.columns).append('team2_'+roll_season.columns) #make feature names
    df = pd.DataFrame(df_mat,columns=cols,index=roll_season.index.get_level_values('game_id')[::2])#index is game id for that game
    if train:
        df = df[df['team1_overtime']==False] #take overtime games out if being trained upon
    df.drop(['team2_Total_PTS','team1_Min','team2_Min','team1_home_team','team2_home_team','team2_overtime','team1_overtime',
            'team1_starter','team2_starter'],axis=1,inplace=True)
    df_use = df[100:] #first 5 games for each team are all 0's. Being safe and just removing first 100 games from dataframe
    return df_use#, train_test_split(df_use.drop('team1_Total_PTS',axis=1),df_use['team1_Total_PTS'],test_size=.5)


def find_params(X_train,y_train):
    '''
    input: train set

    find the parameters for the lasso model

    output: the best estimator for the lasso model
    '''
    parameters = {'alpha':[.9,.92,.94,.96,.98,1,1.02,1.04,1.06,1.08,1.1,1.5],'tol':[.001,.002,.003,.00005,.00001,.0005,.0001]} #gridsearch these parameters
    las = Lasso()
    clf = GridSearchCV(las, parameters)
    clf.fit(X_train,y_train) #fit it to the train set
    return clf.best_estimator_

def model(X_train,X_test,y_train,y_test,alpha,tol):
    '''
    input: train and test sets, alpha and tol to use for lasso model

    train a model and get scores

    output: lasso model, r-squared, average differences, and dataframe for comparing predictions to real
    '''
    las = Lasso(alpha,tol) #lasso model using alpha and tol from previous function
    las.fit(X_train,y_train)
    rsqr=las.score(X_test,y_test) #save r-squared
    preds = las.predict(X_test) #make predictions
    comp_df = pd.DataFrame(y_test.values,columns=['real'],index = y_test.index.get_level_values('game_id'))
    comp_df['predictions']=preds
    comp_df['differences']=comp_df['real']-comp_df['predictions'] #comparison dataframe
    avg_diff=sum(np.abs(y_test-preds))/len(preds) #how far off my predictions are from the true value, on average
    return las,rsqr,avg_diff,comp_df
