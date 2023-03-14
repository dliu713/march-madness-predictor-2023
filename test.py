import sys
import os
import pprint
from scraper import *
pp = pprint.PrettyPrinter(indent=4)

if __name__ == '__main__': 
    # Construct final team data structure
    nba_dict = create_nba_dict()
    probs_dict = FiveThirtyEight()
    url_dict = create_espn_urls(probs_dict)
    team_dict = create_team_dict(probs_dict)
    espn_dict = create_espn_dict(url_dict, probs_dict, nba_dict)

    for player, val in espn_dict.items():
        team_dict[val['tm_name']]["roster"].update({player: val})
    
# dataset composition: espn_player_dict, probs_dict, nba_dict, team_dict, wooden
# Acquire bias data structures

#for team_rk, team_list in team_dict.items():
    #for i in team_list

'''
class Team:
    def __init__(self, player):
        self.player

class Player:
    def __init__(self, height, ppg, rpg, three, three_p, ft, ftp):
        self.height
        self.ppg
        self.rpg
        self.three
        self.three_p
        self.ft
        self.ftp

if __name__ == '__main__':
'''
