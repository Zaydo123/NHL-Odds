# NHL-Odds Calculator
In an attempt to make quick money against friends, we created this computer program that analyzes current season trends and uses math/statistics to predict scores and win percentages. 

## Authors: [Zayd Alzein](https://github.com/Zaydo123) and [Andrew Isenhart](https://github.com/aisenhart) 

## Poisson Distribution and Win Percentage Calculation

We created a [Poisson Distribution](https://en.wikipedia.org/wiki/Poisson_distribution) in the python code using [SciPy](https://scipy.org/)

Heatmapping the values from each poisson calculation would give us a graph similar to this:
  <img width="962" alt="Screen Shot 2022-08-17 at 1 29 25 AM" src="https://user-images.githubusercontent.com/26662362/185050262-642381b6-fa95-4bb2-9276-e8a573fd27d2.png">
Using all the data from the distribution, we are able to find the win percentage by summing the percentages of the situations where one team scores higher than another. Afterwards we calculate tie percentages using the same method.

Visual of cells that would be added together in order to find a win percentage.
<img width="963" alt="Screen Shot 2022-08-17 at 1 38 23 AM" src="https://user-images.githubusercontent.com/26662362/185051857-f3962598-68eb-4238-9033-ff9ad72f6a04.png">

 



## Score Prediction
```
    def calculate_score(self):
        t1=leagueGF*(self.home['Attack Strength']*self.away["Defense Strength"])
        t2=leagueGF*(self.away['Attack Strength']*self.home["Defense Strength"])
        return(t1,t2) #home, away
        
```

$$ Score = League Average GF * {Attack Strength*Defense Strength} $$
***
## Attack Strength / Defensive Strength Calculation
```
    for i in teamsData:
        teamsData[i]['Attack Strength']=(teamsData[i]['GF']/teamsData[i]['Games Played'])/leagueGF
        teamsData[i]['Defense Strength']=(teamsData[i]['GA']/teamsData[i]['Games Played'])/leagueGA
    return teamsData
    
```
$$ Attack Strength = {Average Goals Count\over League Average GF}$$


$$ Defensive Strength = {Average Goals Against Count\over League Average GA} $$

