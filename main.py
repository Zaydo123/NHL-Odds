from turtle import home
from numpy import append
from scipy.stats import poisson
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import time

league_gf = 3.092

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
                print(column,row,'|',chance*chance2)
                row+=1
            column+=1
            row=0
        print(((1-away_odds)*100),away_odds*100)

matchup(("Vegas Golden Knights",3,2.83,0.970,0.986),("Nashville Predators",3.3,2.61,1.067,0.910)).poisson_calculator()
