from numpy import append
from scipy.stats import poisson
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import time
import csv
from teams import teams
import random
import colorama
from colorama import Fore, Back, init 
init(autoreset=True)


def read_csv():
    #Date,Visitor,G,Home,G,,Att.,LOG,Notes
    with open('data.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
        data.remove(data[0])
    return data

data_list=read_csv()


def getTeamRecords(data):
    global leagueGF
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
    leagueGA=0
    leagueGamesPlayed=0
    for i in teamsData:
        leagueGF=leagueGF+teamsData[i]['GF']
        leagueGA=leagueGA+teamsData[i]['GA']
        leagueGamesPlayed=leagueGamesPlayed+teamsData[i]['Games Played']

    leagueGF=leagueGF/leagueGamesPlayed
    leagueGA=leagueGA/leagueGamesPlayed

    for i in teamsData:
        teamsData[i]['Attack Strength']=(teamsData[i]['GF']/teamsData[i]['Games Played'])/leagueGF
        teamsData[i]['Defense Strength']=(teamsData[i]['GA']/teamsData[i]['Games Played'])/leagueGA
        #print(i,teamsData[i])
    return teamsData
    

class matchup:                            #                    0    1  2    3             4
    def __init__(self,home,away,homeName,awayName) -> None: #param type: tuple (name,gf,ga,attack strength, defense strength)
        self.home=home
        self.away=away
        self.homeName=homeName
        self.awayName=awayName
    def calculate_score(self):
        t1=leagueGF*(self.home['Attack Strength']*self.away["Defense Strength"])
        t2=leagueGF*(self.away['Attack Strength']*self.home["Defense Strength"])
        return(t1,t2) #home, away
    def poisson_calculator(self):
        temp=self.calculate_score()
        home_predicted=temp[0]
        away_predicted=temp[1]
        poisson_home=[]
        poisson_away=[]
        all_chances=[]
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

                #print(column,row,'|',chance*chance2)
                all_chances.append(chance*chance2)
                row+=1
            column+=1
            row=0
        home_odds=home_odds+0.5*(tie_odds)
        away_odds=away_odds+0.5*(tie_odds)
        print(Back.RED+"Odds")
        print(self.homeName+" : "+str(home_odds*100)+"%"+" - "+str(home_predicted)+" Points")
        print(self.awayName+' : '+str(away_odds*100)+'%'+" - "+str(away_predicted)+" Points")
        
        for i in range(len(poisson_home)):
            plt.plot(i, poisson_home[i]*100,'xb-')
        plt.xlabel(f'Goals Scored ({self.homeName})')
        plt.ylabel('% Chance')
        plt.savefig('plots/'+self.homeName+' vs '+self.awayName+f'({self.homeName[0:5]}).png')
        plt.clf()


        for i in range(len(poisson_away)):
            plt.plot(i, poisson_away[i]*100,'xb-')
        plt.xlabel(f'Goals Scored ({self.awayName})')
        plt.ylabel('% Chance')
        plt.savefig('plots/'+self.homeName+' vs '+self.awayName+f'({self.awayName[0:5]}).png')
        plt.clf()
        return(home_odds,away_odds)

    def ridge_regression():
        pass


all=getTeamRecords(data_list)
homeTeamName=input("Home Team : ")
awayTeamName=input("Away Team : ")
for i in all.keys():
    if i.lower().find(homeTeamName.lower())!=-1:
        homeTeamName=i
    if i.lower().find(awayTeamName.lower())!=-1:
        awayTeamName=i


homeTeam=all[homeTeamName]
awayTeam=all[awayTeamName]

matchup(homeTeam,awayTeam,homeTeamName,awayTeamName).poisson_calculator()
'''
with open('predictions.txt','w+') as f:
    for i in range(len(all.keys())):
        try:
            t1Name=random.choice(list(all.keys()))
            t2Name=random.choice(list(all.keys()))
            result=matchup(all[t1Name],all[t2Name],t1Name,t2Name).poisson_calculator()
            f.write(t1Name+' '+str(result[0])+'  ||||   '+t2Name+' '+str(result[1])+'\n')
        except KeyError:
            print(teams[i])

'''
