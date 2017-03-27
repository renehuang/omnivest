# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 13:49:54 2017

@author: reneh
"""

import math
import numpy as np

#game related functions
#tm1 is away team, tm2 is home team

class Game:
    def __init__(self, tm1, tm2, teams_df, c_home, lmda, times):
        self.tm1=tm1
        self.tm2=tm2
        #value of sum of goals g_i+g_j
        self.teams_df = teams_df
        self.lmda = lmda
        self.c_home=c_home
        self.sgoals=self.teams_df.ix[self.tm1,'sigma_g']+self.teams_df.ix[self.tm2,'sigma_g']-self.lmda
        #mean value of q_ij considering home advantage
        #attention i is away team here
        self.mqij=self.teams_df.ix[self.tm1,'dlt_g']-self.teams_df.ix[self.tm2,'dlt_g']-self.c_home
        self.times= times
        
    #monte carlo simulation for poisson
    def sim_result(self, games):
        temp=0
        game_mqij=games['mqij'].loc[self.tm1+' vs '+self.tm2]
        game_sgoals=games['sgoals'].loc[self.tm1+' vs '+self.tm2]
        a_mean=(game_mqij+game_sgoals)/2
        h_mean=(game_sgoals-game_mqij)/2
        for i in range(self.times):
            t=0 
            I=0
            while t<=1:
                t=t-1/(a_mean+h_mean)*math.log(np.random.random_sample())
                I=I+1
            temp=temp+I
        g_i=round(temp/self.times*a_mean/(a_mean+h_mean))
        g_j=round(temp/self.times*h_mean/(a_mean+h_mean))
        return g_i, g_j