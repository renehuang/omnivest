# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 13:52:11 2017

@author: reneh
"""

import time
import Game

#the time needed is 354 sec
#Get for each game the simulation result

def all_sim(games,teams_df, c_home, lmda, N):
    t1=time.time()
    tp_1=[]
    tp_2=[]
    for index, row in games.iterrows():
        one_game=Game.Game(row['a_tm'],row['h_tm'],teams_df, c_home, lmda, N)
        rlt1, rlt2=one_game.sim_result(games)
        tp_1.append(rlt1)
        tp_2.append(rlt2)
    games['sim_ascore']=tp_1
    games['sim_hscore']=tp_2
    t2=time.time()-t1
    print('Time used for this simulation is '+str(t2)+' seconds')
    return 