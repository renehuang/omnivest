# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 13:48:14 2017

@author: reneh
"""

# Create class team for calculating the scores & average scores

import numpy as np

class Team:
    def __init__(self, name, data):
        self.name=name
        self.data=data
        
        #the lines that include team=name as the away/home team
        self.a_games=data.loc[data['away_tm']==name]
        self.h_games=data.loc[data['home_tm']==name]
        
        #average sum of scores for all games
        self.lmda=data['sum'].mean()
        self.sumvar=data['sum'].var()
        self.diffvar=data['diff'].var()
        
        
    #the average sum of scores scored and conceded by team=name
    def sscore(self):
        tp1=self.a_games['sum'].values.tolist()
        tp1.extend(self.h_games['sum'].values.tolist())
        tp2=np.mean(tp1)
        b_n=1/(1+3/(len(tp1)*self.sumvar))
        tp3=self.lmda+b_n*(tp2-self.lmda)
        return tp3
    
    
    #the average (scored-conceded) per game for team=name
    def difscore(self):
        tp1=self.a_games['diff'].values.tolist()
        tp1.extend([-x for x in self.h_games['diff'].values.tolist()])
        tp2=np.mean(tp1)
        a_n=1/(1+3/(len(tp1)*self.diffvar))
        tp3=a_n*tp2
        return tp3