import clean as c
import clusters as clu
import pandas as pd
import numpy as np
from sklearn.linear_model import Lasso

class MyModel():

    def __init__(self,train_size=130):
        self.train_size=train_size
        #self.season=None
        self.home_avgs=None
        self.away_avgs=None
        self.model=None

    def add_clusters(self,season1,season2,season3,n_clusters=4):
        '''
        input: dataframe for previous 3 seasons

        get the average stats for the last 3 seasons and then append clusters

        output: dataframe with clusters
        '''

        avg,home,away,clusters = clu.create_clusters(season1,season2,season3,n_clusters)

        home['cluster']=clusters.labels_
        home=pd.concat((home,pd.get_dummies(home['cluster'],prefix='cluster')),axis=1)
        home.drop('cluster',axis=1,inplace=True)
        away'cluster']=clusters.labels_
        away=pd.concat((away,pd.get_dummies(away['cluster'],prefix='cluster')),axis=1)
        away.drop('cluster',axis=1,inplace=True)
        self.home_avgs = home
        self.away_avgs = away

    def simple_model(self,season_for_model,season1,season2,season3,n_clusters=4):
        #self.season=season_for_model
        add_clusters(season1,season2,season3,n_clusters)
        model = season_for_model[['game_id','home_team','team','Total_PTS','days_after_opener']]
        hmodel=model[model['home_team']==1].join(self.home_avgs,on='team')
        amodel=model[model['home_team']==0].join(self.away_avgs,on='team')
        amodel=amodel.groupby(['days_after_opener','game_id']).mean()
        hmodel=hmodel.groupby(['days_after_opener','game_id']).mean()
        model = amodel.join(hmodel,lsuffix='_away',rsuffix='_home')
        model.drop(['home_team_away','home_team_home','Total_PTS_home'],axis=1,inplace=True)
        model_train = model[:self.train_size]
        las = Lasso(alpha = 2.25, tol=.000005)
        las.fit(model_train.drop('Total_PTS_away',axis=1),model_train['Total_PTS_away'])
        self.model = las

    def predict(self,season_for_model):
        model = season_for_model[['game_id','home_team','team','Total_PTS','days_after_opener']]
        hmodel=model[model['home_team']==1].join(self.home_avgs,on='team')
        amodel=model[model['home_team']==0].join(self.away_avgs,on='team')
        amodel=amodel.groupby(['days_after_opener','game_id']).mean()
        hmodel=hmodel.groupby(['days_after_opener','game_id']).mean()
        model = amodel.join(hmodel,lsuffix='_away',rsuffix='_home')
        model_test = model[self.train_size:]
        return self.model.predict(model_test.drop('Total_PTS_away',axis=1))
