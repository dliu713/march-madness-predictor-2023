import sys
import os
import json
import pprint
import random
from scraper import *
pp = pprint.PrettyPrinter(indent=4)

global upset_count_dict
upset_count_dict = {
    'total': 0,
    '64': 0,
    '32': 0,
    '16': 0
}

class Team:
    def __init__(self, name: str, data: dict):
        self.name = name
        self.id = data[name]['id']
        self.score = data[name]['score']
        self.seed = data[name]['seed']
        self.kprk = data[name]['rk']
        self.prob = data[name]['prob']
        self.region = data[name]['region']
        self.slot = data[name]['slot']
        self.conf = data[name]['Conf']
        self.AdjEM = data[name]['AdjEM']
        self.AdjO = data[name]['AdjO']
        self.AdjD = data[name]['AdjD']
        self.players = []
        for player, attributes in data[name]["roster"].items():
            self.players.append(Player(player, attributes))
        self.ffour = data[name]['ffour']

class Player:
    def __init__(self, player, attributes: dict):
        self.name = player
        self.pos = attributes['pos']
        self.team = attributes['tm_name']
        self.team_id = attributes['id']
        self.gp = attributes['gp']
        self.min = attributes['min']
        self.pts = attributes['pts']
        self.three_p = attributes['3p%']
        self.ftp = attributes['ft%']
        self.reb = attributes['reb']
        self.height = attributes['height']
        self.athleticism = attributes['Athleticism']
        self.jumper = attributes['Jump Shot']
        self.quickness = attributes['Quickness']
        self.wooden = attributes['Wooden']
        self.yr = attributes['yr']

def road_to_ff_sim(data, region, upset_count_dict):
    # Load the teams
    reg_round_64 = {}
    keys_list = ['1', '8', '5', '4', '6', '3', '7', '2']
    values_list = ['16', '9', '12', '13', '11', '14', '10', '15']
    favorites = []
    underdogs = []
    for i in keys_list:
        for key, val in data.items():
            team = Team(key, data)
            if team.region == region:
                if team.seed == i:
                    favorites.append(team.name)
    for i in values_list:
        for key, val in data.items():
            team = Team(key, data)
            if team.region == region:
                if team.seed == i:
                    underdogs.append(team.name)
    for i in range(len(favorites)):
        reg_round_64[favorites[i]] = underdogs[i]
    print(reg_round_64)
    # Simulate round of 64
    round_32 = []
    for key, val in reg_round_64.items():
        team1 = Team(key, data)
        team2 = Team(val, data)
        weight1 = team1.score
        weight2 = team2.score

        # BIAS METRICS
        # Seed bias
        seed_bias = abs(int(team2.seed) - int(team1.seed))
        weight1 += seed_bias
        # Upset trend weighting
        if team1.seed == '7' or team1.seed == '6' or team1.seed == '5' or team1.seed == '4':
            weight2 += 10
        elif team1.seed == '3':
            weight2 += 5
        if team1.ffour == 1:
            weight1 += 5
        elif team2.ffour == 1:
            weight2 += 5
        # conf trends
        if team1.conf == 'CUSA' or team1.conf == 'MAC':
            weight1 += 1
        if team2.conf == 'CUSA' or team2.conf == 'MAC':
            weight2 += 1

        # game simulation
        game = [team1.name, team2.name]
        count1 = 0
        count2 = 0
        for i in range(7):
            winner = random.choices(game, weights=(weight1, weight2), k=2)
            if winner[0] == team1.name and winner[1] == team1.name:
                count1+=1
            elif winner[0] == team2.name and winner[1] == team2.name:
                count2+=1
        
        # FINAL BIAS METRICS
        # Team trends
        if team2.name == 'Auburn':
            round_32.append(team2.name)
            continue
        elif team1.name == 'Arkansas':
            round_32.append(team1.name)
            continue
        elif team2.name == 'Furman':
            round_32.append(team1.name)
            continue
        elif team1.name == 'Gonzaga':
            round_32.append(team1.name)
            continue
        elif team1.name == 'Misouri':
            round_32.append(team2.name)
            upset_count_dict['64']+=1
            upset_count_dict['total']+=1
            continue
        elif team2.name == 'West Virginia':
            round_32.append(team2.name)
            continue
        # Track upsets and pick winners
        elif upset_count_dict['64'] > 7 or upset_count_dict['total'] > 13:
            round_32.append(team1.name)
            continue
        elif count1 > count2:
            round_32.append(team1.name)
            continue
        elif team1.seed != '8':
            round_32.append(team2.name)
            upset_count_dict['64'] += 1
            upset_count_dict['total']+= 1
    print(round_32)

    # Load the teams
    reg_round_32 = {}
    top = [round_32[0], round_32[2], round_32[4], round_32[6]]
    bottom = [round_32[1], round_32[3], round_32[5], round_32[7]]
    for i in range(len(top)):
        reg_round_32[top[i]] = bottom[i]
    # Simulate round of 32
    sweet_16 = []
    for key, val in reg_round_32.items():
        team1 = Team(key, data)
        team2 = Team(val, data)
        game = [team1.name, team2.name]
        weight1 = team1.score
        weight2 = team2.score

        # Trends
        if team2.name == 'Marquette':
            weight2 -= 10
        if team2.name == 'Gonzaga':
            weight2 += 10
        if team1.ffour == 1:
            weight1 += 5
        elif team2.ffour == 1:
            weight2 += 5 
        if team1.seed == '2' or team1.seed == '3':
            weight1 -=5
        elif team2.seed == '2' or team2.seed == '3':
            weight2 -= 5
        if team1.seed == '11':
            weight1 += 5
        elif team2.seed == '11':
            weight2 += 5
        if team1.seed == '3' and team2.seed == '11':
            weight2 += 5
        elif team1.seed == '11' and team2.seed == '3':
            weight1 += 5
        # conf trends
        if team1.conf == 'ACC':
            weight1 += 1
        elif team2.conf == 'ACC':
            weight2 += 1
        
        # game sim
        count1 = 0
        count2 = 0
        for i in range(7):
            winner = random.choices(game, weights=(weight1, weight2), k=2)
            if winner[0] == team1.name and winner[1] == team1.name:
                count1+=1
            elif winner[0] == team2.name and winner[1] == team2.name:
                count2+=1

        # FINAL BIAS METRICS
        # Track upsets and pick winners
        if team1.name == 'Creighton':
            sweet_16.append(team2.name)
            if int(team2.seed) > int(team1.seed):
                upset_count_dict['32']+=1
                upset_count_dict['total'] += 1
            continue
        if upset_count_dict['32'] > 4 or upset_count_dict['total'] > 13:
            if int(team1.seed) > int(team2.seed):
                sweet_16.append(team1.name)
            else:
                sweet_16.append(team2.name)
            continue
        if count1 > count2:
            sweet_16.append(team1.name)
            if int(team1.seed) < int(team2.seed):
                upset_count_dict['32'] += 1
                upset_count_dict['total']+= 1 
            continue
        else:
            sweet_16.append(team2.name)
            if int(team2.seed) < int(team1.seed):
                upset_count_dict['32'] += 1
                upset_count_dict['total']+= 1 
    print(sweet_16)

    # Load teams
    reg_sweet_16 = {}
    top = [sweet_16[0], sweet_16[2]]
    bottom = [sweet_16[1], sweet_16[3]]
    for i in range(len(top)):
        reg_sweet_16[top[i]] = bottom[i]
    # Simulate the sweet 16
    elite_8 = []
    for key, val in reg_sweet_16.items():
        team1 = Team(key, data)
        team2 = Team(val, data)
        weight1 = team1.score
        weight2 = team2.score
        game = [team1.name, team2.name]

        # BIAS METRICS Trends
        if team1.name == 'Kansas':
            weight1 -= 10
        elif team2.name == 'Kansas':
            weight2 -= 10
        if team1.conf == 'SEC':
            weight1 += 5
        if team2.conf == 'SEC':
            weight2 += 5
        if int(team1.seed) <= 6:
            weight1 += 5
        if int(team2.seed) <=6:
            weight2 += 5
        
        # game sim
        count1 = 0
        count2 = 0
        for i in range(7):
            winner = random.choices(game, weights=(weight1, weight2), k=2)
            if winner[0] == team1.name and winner[1] == team1.name:
                count1+=1
            elif winner[0] == team2.name and winner[1] == team2.name:
                count2+=1
        
        # FINAL BIAS METRICS
        # Track upsets and pick winners
        if team1.conf == 'MWC':
            elite_8.append(team2.name)
            if int(team2.seed) > int(team1.seed):
                upset_count_dict['16'] += 1
                upset_count_dict['total']+= 1  
            continue
        if team2.conf == 'MWC':
            elite_8.append(team1.name)
            if int(team1.seed) > int(team2.seed):
                upset_count_dict['16'] += 1
                upset_count_dict['total']+= 1  
            continue
        if upset_count_dict['16'] > 2 or upset_count_dict['total'] > 13:
            if int(team1.seed) > int(team2.seed):
                elite_8.append(team1.name)
            else:
                elite_8.append(team2.name)
            continue
        if count1 > count2:
            elite_8.append(team1.name)
            if int(team1.seed) < int(team2.seed):
                upset_count_dict['16'] += 1
                upset_count_dict['total']+= 1 
            continue
        else:
            elite_8.append(team2.name)
            if int(team2.seed) < int(team1.seed):
                upset_count_dict['16'] += 1
                upset_count_dict['total']+= 1 
    print(elite_8)

    # Simulate the elite 8
    final_four = ''
    team1 = Team(elite_8[0], data)
    team2 = Team(elite_8[1], data)
    weight1 = team1.score
    weight2 = team2.score
    game = [team1.name, team2.name]

    # BIAS
    if team1.name == 'Arizona':
        weight1 -= 10
    if team2.name == 'Arizona':
        weight2 -= 10
    if team1.seed == '3' or int(team1.seed) <= 7 or team1.seed == '1':
        weight1 += 10
    if team2.seed == '3' or int(team1.seed) <= 7 or team2.seed == '1':
        weight2 += 10

    # game sim
    count1 = 0
    count2 = 0
    for i in range(7):
        winner = random.choices(game, weights=(team1.score, team2.score), k=2)
        if winner[0] == team1.name and winner[1] == team1.name:
            count1+=1
        elif winner[0] == team2.name and winner[1] == team2.name:
            count2+=1

    # FINAL TRENDS
    if team1.name == 'Xavier' or team1.name == 'Purdue' or team1.name == 'Marquette':
        final_four = team2.name
    elif team2.name == 'Xavier' or team1.name == 'Purdue' or team1.name == 'Marquette':
        final_four = team1.name
    
    if count1 > count2:
        final_four = team1.name
    else:
        final_four = team2.name
    print(final_four)

    return final_four

def final_four_sim(data, south, midwest, east, west):
    championship = []
    team1 = Team(south, data)
    team2 = Team(east, data)
    team3 = Team(midwest, data)
    team4 = Team(west, data)
    weight1 = team1.score
    weight2 = team2.score
    weight3 = team3.score
    weight4 = team4.score
    left_game = [team1.name, team2.name]
    right_game = [team3.name, team4.name]

    # leftgame sim
    count1 = 0
    count2 = 0
    for i in range(7):
        winner = random.choices(left_game, weights=(weight1, weight2), k=2)
        if winner[0] == team1.name and winner[1] == team1.name:
            count1+=1
        elif winner[0] == team2.name and winner[1] == team2.name:
            count2+=1
    # rightgame sim
    count3 = 0
    count4 = 0
    for i in range(7):
        winner = random.choices(right_game, weights=(weight3, weight4), k=2)
        if winner[0] == team3.name and winner[1] == team3.name:
            count3+=1
        elif winner[0] == team4.name and winner[1] == team4.name:
            count4+=1
    
     # FINAL TRENDS
    if count1 > count2:
        if int(team1.seed) <= 3:
            championship.append(team1.name)
    else:
        if int(team2.seed) <=3:
            championship.append(team2.name)
    
    if count3 > count4:
        if int(team3.seed) <=3:
            championship.append(team3.name)
    else:
        if int(team4.seed) <=3:
            championship.append(team4.name)
    print(championship)

    national_champ = ''
    team1 = Team(championship[0], data)
    team2 = Team(championship[1], data)
    weight1 = team1.score
    weight2 = team2.score
    game = [team1.name, team2.name]

    # game sim
    count1 = 0
    count2 = 0
    for i in range(7):
        winner = random.choices(game, weights=(weight1, weight2), k=2)
        if winner[0] == team1.name and winner[1] == team1.name:
            count1+=1
        elif winner[0] == team2.name and winner[1] == team2.name:
            count2+=1
    #FINAL

    if count1 > count2:
        national_champ = team1.name
    else:
        national_champ = team2.name

    if team1.seed == '5':
        national_champ = team2.name
    elif team2.seed == '5':
        national_champ = team1.name
    
    if national_champ not in ['Houston', 'Alabama', 'Kansas']:
        print('Trends not passed, please run again')
        return IndexError

    print(national_champ)
    return national_champ

if __name__ == '__main__': 
    f = open('teams.json')
    data = json.load(f)
    #pp.pprint(data)

    try:
        south = road_to_ff_sim(data, "South", upset_count_dict)
        midwest = road_to_ff_sim(data, "Midwest", upset_count_dict)
        east = road_to_ff_sim(data, "East", upset_count_dict)
        west = road_to_ff_sim(data, "West", upset_count_dict)

        champion = final_four_sim(data, south, midwest, east, west)

    except IndexError:
        print('Trends not passed, please run again')

    