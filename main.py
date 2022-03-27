from turtle import home
from numpy import append
from scipy.stats import poisson
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import time
import csv
import colorama
from colorama import Fore, Back, init 
init(autoreset=True)

league_gf = 3.092


def read_csv():
    #Date,Visitor,G,Home,G,,Att.,LOG,Notes
    with open('data.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
        data.remove(data[0])
    return data

def getTeamRecords(data,team):
    teamsData={} 
    useful_data=0
    for i in range(len(data)):
        if data[i][2]!='':
            useful_data+=1
            if data[i][1] not in teamsData.keys():
                    teamsData[data[i][1]]={'GF':0,'GA':0,"Attack Strength":0,"Defense Strength":0,"Games Played":0}
            if data[i][3] not in teamsData.keys():
                teamsData[data[i][3]]={'GF':0,'GA':0,"Attack Strength":0,"Defense Strength":0,"Games Played":0}
            teamsData[data[i][1]]['GF']=teamsData[data[i][1]]['GF']+int(data[i][2])
            teamsData[data[i][1]]['GA']=teamsData[data[i][1]]['GA']+int(data[i][4])
            teamsData[data[i][1]]['Games Played']=teamsData[data[i][1]]['Games Played']+1
            teamsData[data[i][3]]['GF']=teamsData[data[i][3]]['GF']+int(data[i][4])
            teamsData[data[i][3]]['GA']=teamsData[data[i][3]]['GA']+int(data[i][2])
            teamsData[data[i][3]]['Games Played']=teamsData[data[i][3]]['Games Played']+1
    
    leagueGF=0
    leagueGamesPlayed=0
    for i in teamsData:
        leagueGF=leagueGF+teamsData[i]['GF']
        leagueGamesPlayed=leagueGamesPlayed+teamsData[i]['Games Played']
        print(i,teamsData[i])
    leagueGF=leagueGF/leagueGamesPlayed
    print(leagueGF)
        
getTeamRecords(read_csv(),'Boston Bruins')


class matchup:
    def __init__(self,home,away) -> None: #param type: tuple (name,gf,ga,attack strength, defense strength)
        self.home=home
        self.away=away
    def calculate_score(self):
        return(league_gf*(self.home[3]*self.away[4]),league_gf*(self.away[3]*self.home[4])) #home, away
    def poisson_calculator(self):
        home_predicted,away_predicted = self.calculate_score()
        print(home_predicted,away_predicted)
        poisson_home=[]
        poisson_away=[]
        home_odds=0
        away_odds=0
        tie_odds=0
        column=0
        row=0
        outof=10
        for i in range(outof+1):
            x = poisson.pmf(k=i, mu=home_predicted)
            poisson_home.append(x)
        for i in range(outof+1):
            x = poisson.pmf(k=i, mu=away_predicted)
            poisson_away.append(x)
        for chance in poisson_home:
            for chance2 in poisson_away:
                if row>column:
                    home_odds=home_odds+(chance*chance2)
                elif column>row:
                    away_odds=away_odds+(chance*chance2)
                else: 
                    tie_odds=tie_odds+(chance*chance2)

                print(column,row,'|',chance*chance2)
                row+=1
            column+=1
            row=0
        print(Back.RED+"Real Odds")
        print(self.home[0]+" : "+str(round(home_odds*100,3))+"%")
        print(self.away[0]+' : '+str(round(away_odds*100,3))+'%')
        print("Tie Odds: "+str(round(tie_odds*100,3))+'%')
        print('-----------------------------------------------------')
        print((1-away_odds)*100,away_odds*100)

#matchup(("Calgary Flames",3.4,2.29,1.100,0.798),("Edmonton Oilers",3.3,3.06,1.067,1.067)).poisson_calculator()
