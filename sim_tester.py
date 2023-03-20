import sys
import random
from Experimental_approaches.weighted_sim import *

f = open('teams.json')
data = json.load(f)

matchup = ['Kansas', 'Arkansas']

team1 = Team(matchup[0], data)
team2 = Team(matchup[1], data)
print(team1.name) #score-1, score+kenpom-4, shooting_score-1
print(team1.score) #1
print(team1.shooting_score) #1
print(team1.prob) #1
print(team1.kenpom) #2
print(team1.score+team1.kenpom) #tiebreak
print('---------------')
print(team2.name) #prob-1, kenpom-2
print(team2.score) #1
print(team2.shooting_score) #1
print(team2.prob) #1
print(team2.kenpom) #2
print(team2.score+team1.kenpom) #tb