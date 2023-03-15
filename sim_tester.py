import sys
import random
from weighted_sim import *

f = open('teams.json')
data = json.load(f)

championship = ['Alabama', 'Houston']

national_champ = ''
team1 = Team(championship[0], data)
team2 = Team(championship[1], data)
print('Alabama') #score-1, score+kenpom-4, shooting_score-1
print(team1.score) #1
print(team1.score+team1.kenpom) #4
print(team1.shooting_score) #1
print(team1.prob) #1
print(team1.kenpom) #2
print('---------------')
print('Houston') #prob-1, kenpom-2
print(team2.score) #1
print(team2.score+team1.kenpom) #4
print(team2.shooting_score) #1
print(team2.prob) #1
print(team2.kenpom) #2
'''
myList = ["Oral Roberts", "Drake", "Providence"]

newList = random.choices(myList, weights = [30, 10, 20], k=100)
print(newList)

freq = {}
for i in newList:
    if i in freq:
        freq[i] += 1
    else:
        freq[i] = 1

for key, value in freq.items():
    print(f'{key} {value}')'''