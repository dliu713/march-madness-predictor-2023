import sys
import os
import json
import pprint
from scraper import *
pp = pprint.PrettyPrinter(indent=4)

class Team:
    def __init__(self, name: str, data: dict):
        self.name = name
        self.id = data[name]['id']
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

if __name__ == '__main__': 
    f = open('teams.json')
    data = json.load(f)
    #pp.pprint(data)

    #team = Team(name, data)
    '''Template: 
    team = Team('Houston', team_dict)
    print(team.AdjEM)
    print(team.players)
    for player in team.players:
        if(int(player.athleticism) >= 8):
            print(player.name)'''

    