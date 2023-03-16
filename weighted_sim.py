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

def add_upsets(regional_results, possible_upsets, priority_add, round, round_upsets_dict, target_upsets):
        num_to_add = target_upsets - upset_count_dict[round]
        priority_queue = []
        for i in list(priority_add):
            if i not in list(round_upsets_dict):
                priority_queue.append(i)
        add_list = []
        for i in range(num_to_add):
            add_list.append(priority_queue[i])
        # get dict values
        add_dict ={}
        for upset, fav in possible_upsets.items():
            if upset in add_list:
                add_dict.update({fav: upset})
        for i in range(len(regional_results)):
            for j in range(len(regional_results[i])):
                if regional_results[i][j] in list(add_dict):
                    regional_results[i][j] = add_dict[regional_results[i][j]]
        upset_count_dict[round] += num_to_add
        upset_count_dict['total']+= num_to_add
        return regional_results

def remove_upsets(regional_results, possible_upsets, priority_remove, round, round_upsets_dict, target_upsets):
    num_to_remove = upset_count_dict[round] - target_upsets
    priority_queue = []
    for i in list(priority_remove):
        if i in list(round_upsets_dict):
            priority_queue.append(i)
    remove_list = []
    for i in range(num_to_remove):
        remove_list.append(priority_queue[i])
    remove_dict = {}
    for upset, fav in possible_upsets.items():
        if upset in remove_list:
            remove_dict.update({upset: fav})
    for i in range(len(regional_results)):
        for j in range(len(regional_results[i])):
            if regional_results[i][j] in list(remove_dict):
                regional_results[i][j] = remove_dict[regional_results[i][j]]
    upset_count_dict[round] -= num_to_remove
    upset_count_dict['total'] -= num_to_remove
    return regional_results

def simulate_upsets(upsetList, weights_list):
    sim_upsets = random.choices(upsetList, weights = weights_list, k = 100)
    freq = {}
    for i in sim_upsets:
        if i in freq:
            freq[i] += 1
        else:
            freq[i] = 1
    return freq

def round_of_64(data, region_list):
    # https://www.ncaa.com/news/basketball-men/bracketiq/2018-03-13/heres-how-pick-march-madness-upsets-according-data
    # first round upset probabilities:
    _10_over_7 = 39.5
    _11_over_6 = 37.5
    _12_over_5 = 35.4
    _13_over_4 = 21.5
    _14_over_3 = 15.3
    _15_over_2 = 6.3
    possible_upsets = {}
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
        for fav, und in reg_round_64.items():
            id = Team(fav, data)
            if id.seed != '1' and id.seed != '8':
                possible_upsets.update({und: fav})

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
                if (team2.seed != '9'):
                    upset_count_dict['64'] += 1
                    upset_count_dict['total'] += 1
                    first_round_upsets.update({team2.name: team1.name})
            else:
                round_32.append(team1.name)
        #print(round_32)
        regional_results.append(round_32)

    # Create Priority Queue for upsets
    upsetList = []
    for upset in possible_upsets.keys():
        upsetList.append(upset)

    weights_list = [0]*len(upsetList)
    for i in range(len(upsetList)):
        upset = Team(upsetList[i], data)
        if upset.seed == '10':
            weights_list[i] = _10_over_7
        elif upset.seed == '11':
            weights_list[i] = _11_over_6
        elif upset.seed == '12':
            weights_list[i] = _12_over_5
        elif upset.seed == '13':
            weights_list[i] = _13_over_4
        elif upset.seed == '14':
            weights_list[i] = _14_over_3
        elif upset.seed == '15':
            weights_list[i] = _15_over_2

    freq = simulate_upsets(upsetList, weights_list)
    for team, score in freq.items():
        id1 = Team(team, data)
        for upset, fav in possible_upsets.items():
            id2 = Team(fav, data)
            if upset == id1.name:
                freq[team]=score+id1.score+id1.kenpom-id2.score-id2.kenpom
    priority_add = dict(sorted(freq.items(), key=lambda x:x[1], reverse = True))
    priority_remove = dict(sorted(freq.items(), key=lambda x:x[1]))
    
    if upset_count_dict['64'] < 7:
        regional_results = add_upsets(regional_results, possible_upsets, priority_add, '64', first_round_upsets, 7)
    elif upset_count_dict['64'] > 7:
        regional_results = remove_upsets(regional_results, possible_upsets, priority_remove, '64', first_round_upsets, 7)
    else:
        regional_results = regional_results
    #for i in regional_results:
        #print(i)
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
    possible_upsets = {}
    regional_results=[]

    for round_32 in region_list:
        # Load the teams
        reg_round_32 = {}
        top = [round_32[0], round_32[2], round_32[4], round_32[6]]
        bottom = [round_32[1], round_32[3], round_32[5], round_32[7]]
        for i in range(len(top)):
            reg_round_32[top[i]] = bottom[i]
        for key, val in reg_round_32.items():
            top = Team(key, data)
            bottom = Team(val, data)
            if int(top.seed) > int(bottom.seed) and top.seed != '5' and bottom.seed !='4':
                possible_upsets.update({top.name: bottom.name})
            elif int(top.seed) < int(bottom.seed) and top.seed != '5' and bottom.seed !='4':
                possible_upsets.update({bottom.name: top.name})

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
                if int(team2.seed) - int(team1.seed) > 1:
                    upset_count_dict['32'] += 1
                    upset_count_dict['total'] += 1
                    second_round_upsets.update({team2.name: team1.name})
            else:
                sweet_16.append(team1.name)
       #print(sweet_16)
        regional_results.append(sweet_16)

    #print(possible_upsets)
    # Create Priority Queue for upsets
    upsetList = []
    for upset in possible_upsets.keys():
        upsetList.append(upset)

    weights_list = [0]*len(upsetList)
    for i in range(len(upsetList)):
        upset = Team(upsetList[i], data)
        if upset.seed == '6':
            weights_list[i] = _6_over_3
        elif upset.seed == '7':
            weights_list[i] = _7_over_2
        elif upset.seed == '10':
            weights_list[i] = _10_over_2
        elif upset.seed == '11':
            weights_list[i] = _11_over_3
        elif upset.seed == '8':
            weights_list[i] = _8_over_1
        elif upset.seed == '12':
            weights_list[i] = _12_over_4
        elif upset.seed == '9':
            weights_list[i] = _9_over_1

    freq = simulate_upsets(upsetList, weights_list)
    for team, score in freq.items():
        id1 = Team(team, data)
        for upset, fav in possible_upsets.items():
            id2 = Team(fav, data)
            if upset == id1.name:
                freq[team]=score+id1.score+id1.kenpom-id2.score-id2.kenpom
    priority_add = dict(sorted(freq.items(), key=lambda x:x[1], reverse = True))
    priority_remove = dict(sorted(freq.items(), key=lambda x:x[1]))
    #print(priority_add)
    # generate target_upsets
    target_upsets = random.randint(3, 4)
    if upset_count_dict['32'] < target_upsets:
        regional_results = add_upsets(regional_results, possible_upsets, priority_add, '32', second_round_upsets, target_upsets)
    elif upset_count_dict['32'] > target_upsets:
        regional_results = remove_upsets(regional_results, possible_upsets, priority_remove, '32', second_round_upsets, target_upsets)
    else:
        regional_results = regional_results
    #for i in regional_results:
        #print(i)
    return regional_results

def run_sweet_16(data, region_list):
    possible_upsets = {}
    regional_results=[]
    for sweet_16 in region_list:
        # Load teams
        reg_sweet_16 = {}
        top = [sweet_16[0], sweet_16[2]]
        bottom = [sweet_16[1], sweet_16[3]]
        for i in range(len(top)):
            reg_sweet_16[top[i]] = bottom[i]
        for key, val in reg_sweet_16.items():
            top = Team(key, data)
            bottom = Team(val, data)
            if int(top.seed) > int(bottom.seed) and top.seed != '3' and bottom.seed != '2':
                possible_upsets.update({top.name: bottom.name})
            elif int(bottom.seed) > int(top.seed) and top.seed != '3' and bottom.seed != '2':
                possible_upsets.update({bottom.name: top.name})

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
                if int(team2.seed) - int(team1.seed) > 1:
                    upset_count_dict['16'] += 1
                    upset_count_dict['total'] += 1
                    sweet_16_upsets.update({team2.name: team1.name})
            else:
                elite_8.append(team1.name)
        #print(elite_8)
        regional_results.append(elite_8)
    
    # Create Priority Queue for upsets
    upsetList = []
    for upset in possible_upsets.keys():
        upsetList.append(upset)
    
    weights_list = [1]*len(upsetList)
    freq = simulate_upsets(upsetList, weights_list)
    for team, score in freq.items():
        id1 = Team(team, data)
        for upset, fav in possible_upsets.items():
            id2 = Team(fav, data)
            if upset == id1.name:
                freq[team]=score+id1.score+id1.kenpom-id2.score-id2.kenpom
    priority_add = dict(sorted(freq.items(), key=lambda x:x[1], reverse = True))
    priority_remove = dict(sorted(freq.items(), key=lambda x:x[1]))
    #print(possible_upsets)
    print(priority_add)
    if upset_count_dict['16'] < 2:
        regional_results = add_upsets(regional_results, possible_upsets, priority_add, '16', sweet_16_upsets, 2)
    elif upset_count_dict['16'] > 2:
        regional_results = remove_upsets(regional_results, possible_upsets, priority_remove, '16', sweet_16_upsets, 2)
    else:
        regional_results = regional_results
    #for i in regional_results:
        #print(i)
    return regional_results

def run_elite_8(data, region_list):
    possible_upsets = {}
    seed_losers = {}
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
        if(int(team2.seed) >= 7 and int(team1.seed) < 7):
            possible_upsets.update({team2.name: team1.name})
        
        '''if(team1.seed == '6'):
            seed_losers.update({team1.name: team1.name})
        if(team2.seed == '6'):
            seed_losers.update({team2.name: team1.name})'''

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
        #print(final_four)
        regional_results.append(final_four)

    #print(possible_upsets)
    #print(seed_losers)
    upset_found = False
    for i in regional_results:
        find_tm = Team(i, data)
        if int(find_tm.seed) >= 7:
            upset_found = True
    # If possible and necessary, call one big upset into final four
    if len(possible_upsets) > 0 and upset_found == False:
        pull_index = random.randint(0, len(possible_upsets)-1)
        for i, (key, val) in enumerate(possible_upsets.items()):
            if i == pull_index:
                upset_tm = key
                upsetted = val
        for i in range(len(regional_results)):
            if regional_results[i] == upsetted:
                regional_results[i] = upset_tm
    
    #print(regional_results)
    return regional_results

def init_gamefeed_simulator(data, one, two):
    team1 = Team(one, data)
    team2 = Team(two, data)
    # Simulation and counts
    count1=0
    count2=0
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
        result = team2.name
    else:
        result = team1.name
    
    return result

def run_final_four(data, final_four):
    # left
    left = init_gamefeed_simulator(data, final_four[0], final_four[1])
    # right
    right = init_gamefeed_simulator(data, final_four[2], final_four[3])
    championship = [left, right]
    #print(championship)
    return championship

def run_championship(data, championship):
    champion = init_gamefeed_simulator(data, championship[0], championship[1])
    #print(champion)
    return champion

def flatten(nestedlist):
    flatlist=[element for sublist in nestedlist for element in sublist]
    return flatlist

def run_SIMUL(data):
    n=1000
    regional_list = ['South', 'East', 'Midwest', 'West']
    final_second_round = {}
    final_sweet_16 = {}
    final_elite_8 = {}
    final_4 = {}
    final_game={}
    final_champion={}

    while( n > 0 ):
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

        regional_results_64 = round_of_64(data, regional_list)
        for team in flatten(regional_results_64):
            if team in final_second_round:
                final_second_round[team] += 1
            else:
                final_second_round[team] = 1
        
        regional_results_32 = round_of_32(data, regional_results_64)
        for team in flatten(regional_results_32):
            if team in final_sweet_16:
                final_sweet_16[team] += 1
            else:
                final_sweet_16[team] = 1

        regional_results_16 = run_sweet_16(data, regional_results_32)
        for team in flatten(regional_results_16):
            if team in final_elite_8:
                final_elite_8[team] += 1
            else:
                final_elite_8[team] = 1

        final_four = run_elite_8(data, regional_results_16)
        for team in final_four:
            if team in final_4:
                final_4[team] += 1
            else:
                final_4[team] = 1

        championship = run_final_four(data, final_four)
        for team in championship:
            if team in final_game:
                final_game[team] += 1
            else:
                final_game[team] = 1
        
        national_champion = run_championship(data, championship)
        if national_champion in final_champion:
            final_champion[national_champion]+=1
        else:
            final_champion[national_champion]= 1
        n = n - 1

    pprint.pprint(dict(sorted(final_second_round.items(), key=lambda x:x[1], reverse = True)), sort_dicts = False)
    pprint.pprint(dict(sorted(final_sweet_16.items(), key=lambda x:x[1], reverse = True)), sort_dicts = False)
    pprint.pprint(dict(sorted(final_elite_8.items(), key=lambda x:x[1], reverse = True)), sort_dicts = False)
    pprint.pprint(dict(sorted(final_4.items(), key=lambda x:x[1], reverse = True)), sort_dicts = False)
    pprint.pprint(dict(sorted(final_game.items(), key=lambda x:x[1], reverse = True)), sort_dicts = False)
    pprint.pprint(dict(sorted(final_champion.items(), key=lambda x:x[1], reverse = True)), sort_dicts = False)

if __name__ == '__main__': 
    f = open('teams.json')
    data = json.load(f)

    # Sample run:
    regional_list = ['South', 'East', 'Midwest', 'West']
    regional_results_64 = round_of_64(data, regional_list)
    for i in regional_results_64:
        print(i)
    regional_results_32 = round_of_32(data, regional_results_64)
    for i in regional_results_32:
        print(i)
    regional_results_16 = run_sweet_16(data, regional_results_32)
    for i in regional_results_16:
        print(i)
    final_four = run_elite_8(data, regional_results_16)
    print(final_four)
    championship = run_final_four(data, final_four)
    print(championship)
    national_champion = run_championship(data, championship)
    print(national_champion)
    
    print(upset_count_dict)
    #print(first_round_upsets)
    #print(second_round_upsets)
    #print(sweet_16_upsets)

    #run_SIMUL(data)
    
    

