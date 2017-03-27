# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 13:43:43 2017

@author: reneh
"""
import requests
from bs4 import BeautifulSoup


def get_table(year,month, url_start, url_end):
    temp=[]
    url_var=str(year)+'_games-'+month
    url=url_start+url_var+url_end
    r=requests.get(url)
    soup=BeautifulSoup(r.content, 'lxml')
    table = soup.find('table', attrs={'class':'suppress_glossary sortable stats_table'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        temp2=[ele for ele in cols if cols[2] and ele]
        #excluding unfinished games
        if temp2:
            temp.append([year,month]+temp2)
    return temp
