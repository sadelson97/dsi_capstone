import rolling_mean as rm
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.model_selection import GridSearchCV


def get_train_test(season,games_back=7,games_needed=5):
    roll_season = rm.complete_rolling_means(season,games_back,games_needed)
    roll_season['PTS_scored']= season.groupby(['days_after_opener','game_id','team']).sum()['PTS']
    diffs = roll_season['PTS']-roll_season['PTS_scored']
    roll_season.drop('PTS_scored',axis=1,inplace=True)
    diffs_even = diffs[::2].values
    diffs_odd = diffs[1::2].values
    fixed_diff=[]
    for i in range(len(diffs_odd)):
        fixed_diff.append(diffs_odd[i])
        fixed_diff.append(diffs_even[i])
    fixed_diff=pd.Series(fixed_diff,index=diffs.index)
    roll_season['DEF_PTS']=fixed_diff
    mat = roll_season.as_matrix()
    df_mat = []
    for i in range(int(len(mat)/2)):
        df_mat.append(list(mat[2*i])+(list(mat[2*i+1])))
    cols = ('team1_'+roll_season.columns).append('team2_'+roll_season.columns)
    roll_season.index.get_level_values('game_id')[::2]
    df = pd.DataFrame(df_mat,columns=cols,index=roll_season.index.get_level_values('game_id')[::2])
    df.drop(['team2_Total_PTS','team1_Min','team2_Min','team1_home_team','team2_home_team',
            'team1_starter','team2_starter'],axis=1,inplace=True)
    df_use = df[100:]
    return roll_season,df, train_test_split(df_use.drop('team1_Total_PTS',axis=1),df_use['team1_Total_PTS'],test_size=.5)


def find_params(X_train,y_train):
    parameters = {'alpha':[.93,.95,.97,.96,.94,.9,.91,.99], 'normalize':[True, False],'tol':[.001,.002,.003,.00008,.00001,.0001]}
    las = Lasso()
    clf = GridSearchCV(las, parameters)
    clf.fit(X_train,y_train)
    return clf.best_estimator_

def model(X_train,X_test,y_train,y_test,alpha,tol):
    las = Lasso(alpha,tol)
    las.fit(X_train,y_train)
    rsqr=las.score(X_test,y_test)
    preds = las.predict(X_test)
    comp_df = pd.DataFrame(y_test.values,columns=['real'],index = y_test.index.get_level_values('game_id'))
    comp_df['predictions']=preds
    comp_df['differences']=comp_df['real']-comp_df['predictions']
    avg_diff=sum(np.abs(y_test-preds))/len(preds)
    return rsqr,avg_diff,comp_df
