import sys
import random
from test import *

f = open('teams.json')
data = json.load(f)

championship = ['Houston', 'UCLA']

national_champ = ''
team1 = Team(championship[0], data)
team2 = Team(championship[1], data)
game = [team1.name, team2.name]

'''# Seed bias
seed_bias = abs(int(team2.seed) - int(team1.seed))
if int(team1.seed) < int(team2.seed):
    team1.score += seed_bias
else:
    team2.score+=seed_bias'''

#print(f'First score: {team1.score}')
#print(f'Second score: {team2.score}')

# game sim
count1 = 0
count2 = 0
run=True
while(run):
    winner = random.choices(game, weights=(10, 15), k=2)
    if winner[0] == team1.name and winner[1] == team1.name:
        count1+=1
        run = False
    elif winner[0] == team2.name and winner[1] == team2.name:
        count2+=1
        run =False

#print(count1)
#print(count2)

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
    print(f'{key} {value}')