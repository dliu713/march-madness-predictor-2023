import sys
import json
import pprint
import random
pp = pprint.PrettyPrinter(indent=4)

global upset_count_dict
upset_count_dict = {
    'total': 0,
    '64': 0,
    '32': 0,
    '16': 0
}

global first_round_upsets
first_round_upsets = {}

global second_round_upsets
second_round_upsets = {}

global sweet_16_upsets
sweet_16_upsets = {}

class Team:
    def __init__(self, name: str, data: dict):
        self.name = name
        self.id = data[name]['id']
        self.score = data[name]['score']
        self.shooting_score = data[name]['shooting_score']
        self.kenpom = data[name]['kenpom_score']
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

def matchup_simulator(name1, name2, weight1, weight2):
    # game sim
    game = [name1, name2]

    run=True
    while(run):
        winner = random.choices(game, weights=(weight1, weight2), k=2)
        if winner[0] == name1 and winner[1] == name1:
            team = name1
            run = False
        elif winner[0] == name2 and winner[1] == name2:
            team = name2
            run =False
    
    return team

def update_count(winner, name, count, weight):
    if winner == name:
        count+=weight
    return count

def round_of_64(data, region_list):
    # https://www.ncaa.com/news/basketball-men/bracketiq/2018-03-13/heres-how-pick-march-madness-upsets-according-data
    # first round upset probabilities:
    _10_over_7 = 39.5
    _11_over_6 = 37.5
    _12_over_5 = 35.4
    _13_over_4 = 21.5
    _14_over_3 = 15.3
    _15_over_2 = 6.3

    regional_results = []
    for region in region_list:
        # Load the teams
        reg_round_64 = {}
        keys_list = ['1', '8', '5', '4', '6', '3', '7', '2']
        values_list = ['16', '9', '12', '13', '11', '14', '10', '15']
        favorites = []
        underdogs = []
        for i in keys_list:
            for key, val in data.items():
                team = Team(key, data)
                if team.region == region and team.seed == i:
                    favorites.append(team.name)
        for i in values_list:
            for key, val in data.items():
                team = Team(key, data)
                if team.region == region and team.seed == i:
                    underdogs.append(team.name)
        for i in range(len(favorites)):
            reg_round_64[favorites[i]] = underdogs[i]
        #print(reg_round_64)

        # ROUND OF 64
        round_32 = []
        for key, val in reg_round_64.items():
            team1 = Team(key, data)
            team2 = Team(val, data)
            count1 = 0
            count2 = 0

            # Simulation and counts
            # upset_sim -- 4
            if team2.seed == '10':
                winner = matchup_simulator(team1.name, team2.name, 100-_10_over_7, _10_over_7)
            elif team2.seed == '11':
                winner = matchup_simulator(team1.name, team2.name, 100-_11_over_6, _11_over_6)
            elif team2.seed == '12':
                winner = matchup_simulator(team1.name, team2.name, 100-_12_over_5, _12_over_5)
            elif team2.seed == '13':
                winner = matchup_simulator(team1.name, team2.name, 100-_13_over_4, _13_over_4)
            elif team2.seed == '14':
                winner = matchup_simulator(team1.name, team2.name, 100-_14_over_3, _14_over_3)
            elif team2.seed == '15':
                winner = matchup_simulator(team1.name, team2.name, 100-_15_over_2, _15_over_2)
            elif team2.seed == '9':
                if team1.score+team1.kenpom > team2.score+team2.kenpom:
                    winner = team1.name
                else:
                    winner = team2.name
            else:
                winner = team1.name
            count1 = update_count(winner, team1.name, count1, 4)
            count2 = update_count(winner, team2.name, count2, 4)

            # shooting_score->1
            if team1.shooting_score > team2.shooting_score:
                winner = team1.name
            elif team2.shooting_score > team1.shooting_score:
                winner = team2.name
            else:
                winner = matchup_simulator(team1.name, team2.name, team1.shooting_score, team2.shooting_score)
            count1 = update_count(winner, team1.name, count1, 1)
            count2 = update_count(winner, team2.name, count2, 1)
            
            # score->1
            if team1.score > team2.score:
                winner = team1.name
            elif team2.score > team1.score:
                winner = team2.name
            else:
                winner = matchup_simulator(team1.name, team2.name, team1.score, team2.score)
            count1 = update_count(winner, team1.name, count1, 1)
            count2 = update_count(winner, team2.name, count2, 1)
            
            # 538_sim -- 1
            winner = matchup_simulator(team1.name, team2.name, team1.prob, team2.prob)
            count1 = update_count(winner, team1.name, count1, 1)
            count2 = update_count(winner, team2.name, count2, 1)

            # kenpom->2
            if team1.kenpom > team2.kenpom:
                winner = team1.name
            elif team2.kenpom > team1.kenpom:
                winner = team2.name
            else:
                winner = matchup_simulator(team1.name, team2.name, team1.kenpom, team2.kenpom)
            count1 = update_count(winner, team1.name, count1, 2)
            count2 = update_count(winner, team2.name, count2, 2)

            if count2 > count1:
                round_32.append(team2.name)
                upset_count_dict['64'] += 1
                upset_count_dict['total'] += 1
                first_round_upsets.update({team2.name: team1.name})
            else:
                round_32.append(team1.name)
        print(round_32)
        regional_results.append(round_32)

    return regional_results

def round_of_32(data, region_list):
    # ROUND OF 32
    _6_over_3 = 29/36
    _7_over_2 = 26/36
    _10_over_2 = 18/36
    _11_over_3 = 18/36
    _8_over_1 = 14/36
    _12_over_4 = 13/36
    _9_over_1 = 6/36
    regional_results=[]

    for round_32 in region_list:
        # Load the teams
        reg_round_32 = {}
        top = [round_32[0], round_32[2], round_32[4], round_32[6]]
        bottom = [round_32[1], round_32[3], round_32[5], round_32[7]]
        for i in range(len(top)):
            reg_round_32[top[i]] = bottom[i]

        sweet_16 = []
        for key, val in reg_round_32.items():
            team1 = Team(key, data)
            team2 = Team(val, data)
            temp_team = Team(key, data)
            if int(team1.seed) > int(team2.seed):
                temp_team = team1
                team1 = team2
                team2 = temp_team
            count1 = 0
            count2 = 0

            # Simulation and counts
            # upset_sim -- 4
            if team2.seed == '6' and team1.seed == '3':
                winner = matchup_simulator(team1.name, team2.name, 100-_6_over_3, _6_over_3)
            elif team2.seed == '7' and team1.seed == '2':
                winner = matchup_simulator(team1.name, team2.name, 100-_7_over_2, _7_over_2)
            elif team2.seed == '10' and team1.seed == '2':
                winner = matchup_simulator(team1.name, team2.name, 100-_10_over_2, _10_over_2)
            elif team2.seed == '11' and team1.seed == '3':
                winner = matchup_simulator(team1.name, team2.name, 100-_11_over_3, _11_over_3)
            elif team2.seed == '8' and team1.seed == '1':
                winner = matchup_simulator(team1.name, team2.name, 100-_8_over_1, _8_over_1)
            elif team2.seed == '12' and team1.seed == '4':
                winner = matchup_simulator(team1.name, team2.name, 100-_12_over_4, _12_over_4)
            elif team2.seed == '9' and team1.seed == '1':
                winner = matchup_simulator(team1.name, team2.name, 100-_9_over_1, _9_over_1)
            else:
                winner = team1.name
            count1 = update_count(winner, team1.name, count1, 4)
            count2 = update_count(winner, team2.name, count2, 4)

            # shooting_score->1
            if team1.shooting_score > team2.shooting_score:
                winner = team1.name
            elif team2.shooting_score > team1.shooting_score:
                winner = team2.name
            else:
                winner = matchup_simulator(team1.name, team2.name, team1.shooting_score, team2.shooting_score)
            count1 = update_count(winner, team1.name, count1, 1)
            count2 = update_count(winner, team2.name, count2, 1)
            
            # score->1
            if team1.score > team2.score:
                winner = team1.name
            elif team2.score > team1.score:
                winner = team2.name
            else:
                winner = matchup_simulator(team1.name, team2.name, team1.score, team2.score)
            count1 = update_count(winner, team1.name, count1, 1)
            count2 = update_count(winner, team2.name, count2, 1)
            
            # 538_sim -- 1
            winner = matchup_simulator(team1.name, team2.name, team1.prob, team2.prob)
            count1 = update_count(winner, team1.name, count1, 1)
            count2 = update_count(winner, team2.name, count2, 1)

            # kenpom->2
            if team1.kenpom > team2.kenpom:
                winner = team1.name
            elif team2.kenpom > team1.kenpom:
                winner = team2.name
            else:
                winner = matchup_simulator(team1.name, team2.name, team1.kenpom, team2.kenpom)
            count1 = update_count(winner, team1.name, count1, 2)
            count2 = update_count(winner, team2.name, count2, 2)

            if count2 > count1:
                sweet_16.append(team2.name)
                upset_count_dict['32'] += 1
                upset_count_dict['total'] += 1
                second_round_upsets.update({team2.name: team1.name})
            else:
                sweet_16.append(team1.name)
        print(sweet_16)
        regional_results.append(sweet_16)
    return regional_results

def run_sweet_16(data, region_list):
    regional_results=[]
    for sweet_16 in region_list:
        # Load teams
        reg_sweet_16 = {}
        top = [sweet_16[0], sweet_16[2]]
        bottom = [sweet_16[1], sweet_16[3]]
        for i in range(len(top)):
            reg_sweet_16[top[i]] = bottom[i]

        elite_8 = []
        for key, val in reg_sweet_16.items():
            team1 = Team(key, data)
            team2 = Team(val, data)
            temp_team = Team(key, data)
            if int(team1.seed) > int(team2.seed):
                temp_team = team1
                team1 = team2
                team2 = temp_team
            count1 = 0
            count2 = 0

            # Simulation and counts
            # upset_sim -- 4
            if team1.kenpom+team1.score > team2.kenpom+team2.score:
                winner = team1.name
            else:
                winner = team2.name
            count1 = update_count(winner, team1.name, count1, 4)
            count2 = update_count(winner, team2.name, count2, 4)

            # shooting_score->1
            if team1.shooting_score > team2.shooting_score:
                winner = team1.name
            elif team2.shooting_score > team1.shooting_score:
                winner = team2.name
            else:
                winner = matchup_simulator(team1.name, team2.name, team1.shooting_score, team2.shooting_score)
            count1 = update_count(winner, team1.name, count1, 1)
            count2 = update_count(winner, team2.name, count2, 1)
            
            # score->1
            if team1.score > team2.score:
                winner = team1.name
            elif team2.score > team1.score:
                winner = team2.name
            else:
                winner = matchup_simulator(team1.name, team2.name, team1.score, team2.score)
            count1 = update_count(winner, team1.name, count1, 1)
            count2 = update_count(winner, team2.name, count2, 1)
            
            # 538_sim -- 1
            winner = matchup_simulator(team1.name, team2.name, team1.prob, team2.prob)
            count1 = update_count(winner, team1.name, count1, 1)
            count2 = update_count(winner, team2.name, count2, 1)

            # kenpom->2
            if team1.kenpom > team2.kenpom:
                winner = team1.name
            elif team2.kenpom > team1.kenpom:
                winner = team2.name
            else:
                winner = matchup_simulator(team1.name, team2.name, team1.kenpom, team2.kenpom)
            count1 = update_count(winner, team1.name, count1, 2)
            count2 = update_count(winner, team2.name, count2, 2)

            if count2 > count1:
                elite_8.append(team2.name)
                upset_count_dict['16'] += 1
                upset_count_dict['total'] += 1
                sweet_16_upsets.update({team2.name: team1.name})
            else:
                elite_8.append(team1.name)
        print(elite_8)
        regional_results.append(elite_8)
    return regional_results

def run_elite_8(data, region_list):
    regional_results=[]
    for elite_8 in region_list:
        # Load teams
        team1 = Team(elite_8[0], data)
        team2 = Team(elite_8[1], data)
        final_four = ''
        temp_team = Team(elite_8[0], data)
        if int(team1.seed) > int(team2.seed):
            temp_team = team1
            team1 = team2
            team2 = temp_team
        count1 = 0
        count2 = 0

        # Simulation and counts
        # upset_sim -- 4
        if team1.kenpom+team1.score > team2.kenpom+team2.score:
            winner = team1.name
        else:
            winner = team2.name
        count1 = update_count(winner, team1.name, count1, 4)
        count2 = update_count(winner, team2.name, count2, 4)

        # shooting_score->1
        if team1.shooting_score > team2.shooting_score:
            winner = team1.name
        elif team2.shooting_score > team1.shooting_score:
            winner = team2.name
        else:
            winner = matchup_simulator(team1.name, team2.name, team1.shooting_score, team2.shooting_score)
        count1 = update_count(winner, team1.name, count1, 1)
        count2 = update_count(winner, team2.name, count2, 1)
            
        # score->1
        if team1.score > team2.score:
            winner = team1.name
        elif team2.score > team1.score:
            winner = team2.name
        else:
            winner = matchup_simulator(team1.name, team2.name, team1.score, team2.score)
        count1 = update_count(winner, team1.name, count1, 1)
        count2 = update_count(winner, team2.name, count2, 1)
            
        # 538_sim -- 1
        winner = matchup_simulator(team1.name, team2.name, team1.prob, team2.prob)
        count1 = update_count(winner, team1.name, count1, 1)
        count2 = update_count(winner, team2.name, count2, 1)

        # kenpom->2
        if team1.kenpom > team2.kenpom:
            winner = team1.name
        elif team2.kenpom > team1.kenpom:
            winner = team2.name
        else:
            winner = matchup_simulator(team1.name, team2.name, team1.kenpom, team2.kenpom)
        count1 = update_count(winner, team1.name, count1, 2)
        count2 = update_count(winner, team2.name, count2, 2)

        if count2 > count1:
            final_four = team2.name
        else:
            final_four = team1.name
        print(final_four)
        regional_results.append(final_four)
    return regional_results

if __name__ == '__main__': 
    f = open('teams.json')
    data = json.load(f)

    regional_list = ['South', 'East', 'Midwest', 'West']
    regional_results_64 = round_of_64(data, regional_list)
    regional_results_32 = round_of_32(data, regional_results_64)
    regional_results_16 = run_sweet_16(data, regional_results_32)
    final_four = run_elite_8(data, regional_results_16)

