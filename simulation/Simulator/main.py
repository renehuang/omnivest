# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 19:45:43 2017

@author: reneh
"""

import Simulation
import Team
import scraper
import test
import Game

import os
import pandas as pd

       
       
       
def Simulator(seasons, months):
    path = os.getcwd()
    os.chdir(path)
    url_start='http://www.basketball-reference.com/leagues/NBA_'
    url_end='.html'
    
    
    data=[]
    
    for i in range(len(seasons)):
        for j in range(len(months)):
            try:
                temps=scraper.get_table(seasons[i], months[j], url_start, url_end)
                #exclude empty months
                if temps:
                    data=data+temps
            except:
                print(str(seasons[i])+''+months[j]+' not included')
                
    game_data = pd.DataFrame(data, columns=['year', 'month','time', 'away_tm','away_score','home_tm','home_score','del1','del2','del3'])
    game_data = game_data.drop('time',axis=1)
    game_data = game_data.drop('del1',axis=1)
    game_data = game_data.drop('del2',axis=1)
    game_data = game_data.drop('del3',axis=1)
    
    # get the difference & sum data for further calculation
    
    # print(type(game_data['away_score']))
    # os.system("pause")
    
    game_data['diff']=game_data['away_score'].astype(float)-game_data['home_score'].astype(float)
    game_data['sum']=game_data['away_score'].astype(float)+game_data['home_score'].astype(float)
    
    # get the list of NBA teams
    
    teams=game_data['home_tm']
    teams=teams.drop_duplicates()
    teams=teams.values.tolist()
    
    teams_df=pd.DataFrame(data={'name':teams})
    
    
    # create the battle form (get home team & away team)
    temp = []
    temp2 = []
    for item in teams:
        for item2 in teams:
            if item != item2:
                temp.append(item)
                temp2.append(item2)
    games = pd.DataFrame(data={'a_tm':temp, 'h_tm':temp2})
    
    # temp3= []
    games['Battle'] = games['a_tm']+' vs '+games['h_tm']
    games = games.set_index('Battle')
    games.index.name=None
    
    c_home=-game_data['diff'].mean()
    lmda=game_data['sum'].mean()
    
    # \sigma^2_(\delta G)
    # diffvar=game_data['diff'].var()
    
    # variance of q_ij
    # vqij=2*diffvar
    
    # simulation paths
    N=1000
    
    #the \Delta G_i for each team
    
    diff_li=[]
    for row in teams_df['name']:
        temp1=Team.Team(row,game_data)
        diff_li.append(temp1.difscore())
    teams_df['dlt_g']=diff_li
    
    
    #the \Sigma G_i for each team
    
    sum_li=[]
    for row in teams_df['name']:
        temp1=Team.Team(row,game_data)
        sum_li.append(temp1.sscore())
    teams_df['sigma_g']=sum_li
    teams_df = teams_df.set_index('name')
    teams_df.index.name=None
    
    
    temp1=[]
    temp2=[]
    for index, row in games.iterrows():
        one_game=Game.Game(row['a_tm'],row['h_tm'],teams_df, c_home, lmda, N)
        temp1.append(one_game.sgoals)
        temp2.append(one_game.mqij)
    games['sgoals']=temp1
    games['mqij']=temp2
    
    
    Simulation.all_sim(games,teams_df, c_home, lmda, N
                       )
    
    games.to_csv("simulation_result.csv")
    
    pick_accu, mar_accu=test.test(games, game_data)
    print('We pick the right winner for %s percent of time, predict the right margin for %s percent of time'
          %(pick_accu, mar_accu))

    
    
    
# user input seasons & months
seasons=[2015,2016,2017]
months=['october', 'november', 'december', 'january', 'february',
       'march', 'april', 'may','june']

Simulator(seasons, months)
