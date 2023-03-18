import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import sys
from lxml import etree
import os
import pprint
from create_ds import *
pp = pprint.PrettyPrinter(indent=4)

def scrape_espn(url_dict):
    espn_player_dict = {}
    for key, val in url_dict.items():
        dfs = pd.read_html(val)
        df = dfs[0].join(dfs[1])
        df[['Name','Team']] = df['Name'].str.extract('^(.*?)([A-Z]+)$', expand=True)
        for i in range(len(df.index)):
            df['id'] = key

        data = df.iloc[:-1]  # remove the last row which contains totals
        dictionary = {}
        for i, row in data.iterrows():
            dictionary[row['Name'].strip()] = {
                'gp': row['GP'],
                'min': row['MIN'],
                'pts': row['PTS'],
                'reb': row['REB'],
                'ft%': row['FT%'],
                '3p%': row['3P%'],
                'pos': row['Team'],
                'id': row['id']
            }
        espn_player_dict.update(dictionary)

    return espn_player_dict

def get_nba_attr(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    dom = etree.HTML(str(soup))
    name_val_list = [1, 3]
    ele_list = []
    for i in range(1, 13):
        for j in name_val_list:
            ele = dom.xpath(f'//*[@id="content"]/div[1]/div[1]/div/div/div/div/div[1]/div[3]/div[1]/div/div/div[{i}]/div[{j}]')[0].text
            ele_list.append(ele)

    attr_dict = {}
    for i in range(len(ele_list)):
        if ele_list[i] != ' NA':
            try: 
                int(ele_list[i])
            except ValueError:
                attr_dict[ele_list[i].strip()] = ele_list[i+1].strip()
    #print(attr_dict)
    return attr_dict

def create_nba_dict():
    # Load NBA Prospect json
    f = open('nba_prospects.json')
    data = json.load(f)
    nba_dict = {}
    for player in data['player']:
        nba_dict[player['name']] = [player['url'], player['rank'], player['height'], player['position'], player['team'], player["yr"]]

    # Create NBA Prospect dictionary
    for player, val in nba_dict.items():
        url = val[0]
        attr_dict = get_nba_attr(url)
        attr_dict['stock'] = val[1]
        attr_dict['height'] = val[2]
        attr_dict['position'] = val[3]
        attr_dict['team'] = val[4]
        attr_dict['yr'] = val[5]
        nba_dict[player] = attr_dict
    
    for player, val in nba_dict.items():
        for key in val.keys():
            if val[key] == 'NA':
                val[key] = '0'

    #pp.pprint(nba_dict)
    return nba_dict

def FiveThirtyEight():
    # Load FiveThirtyEight json
    # manually edit fivethirtyeight.json to match kenpom.json (all State to St., etc)
    f = open('fivethirtyeight.json')
    data = json.load(f)
    probs_dict = {}
    for team in data:
        probs_dict[team["team_id"]] = [team["team_name"], team["rd7_win"], team["team_region"], team["team_slot"], team["playin_flag"]]
    #pp.pprint(probs_dict)
    return probs_dict

def create_espn_urls(probs_dict):
    url_dict = {}
    for id, val in probs_dict.items():
        url_dict.update({id: f'https://www.espn.com/mens-college-basketball/team/stats/_/id/{id}'})
    #pp.pprint(url_dict)
    return url_dict

# Scrape ESPN and create espn_dict
def create_espn_dict(url_dict, probs_dict, nba_dict):
    espn_player_dict = scrape_espn(url_dict)

    for player, attrs in espn_player_dict.items():
        for id, team in probs_dict.items():
            if attrs["id"] == id:
                espn_player_dict[player].update({"tm_name": team[0]})
    
    for player in espn_player_dict.keys():
        espn_player_dict[player].update({"Wooden": "no"})

    for player in wooden:
        espn_player_dict[player]["Wooden"] = "yes"

    for player in espn_player_dict.keys():
        espn_player_dict[player].update(update_dict)

    for player, attrs in nba_dict.items():
        espn_player_dict[player].update(attrs)
        espn_player_dict[player].update({'prospect': 1})

    # min cutoff: 12.5
    delete_list = []
    for player, attrs in espn_player_dict.items():
        if float(attrs['min']) < 12.5:
            delete_list.append(player)
    
    for i in delete_list:
        del espn_player_dict[i]

    #pp.pprint(espn_player_dict)
    return espn_player_dict

def create_team_dict(probs_dict, espn_dict):
    # Open json file
    f = open('kenpom.json')

    # Returns json object as a dictionary
    data = json.load(f)

    # Create a team dictionary (or instances?)
    team_dict = {}
    for team in data["kenpom"]:
        team_dict[team['name']] = {
            "rk": team['rk'],
            "AdjEM": team['AdjEM'],
            "AdjO": team["AdjO"],
            "AdjD": team["AdjD"],
            "seed": team["seed"],
            "Conf": team["Conf"],
            "roster": {}
        }

    for id, val in probs_dict.items():
        team_dict[val[0]].update({"id": id})

    for player, val in espn_dict.items():
        team_dict[val['tm_name']]["roster"].update({player: val})

    for id, val in probs_dict.items():
        team_dict[val[0]].update({
            'prob': val[1],
            'region': val[2],
            'slot': val[3],
            'ffour': val[4]
        })

    #pp.pprint(team_dict)
    return team_dict

if __name__ == '__main__': 
    # Construct final team data structure
    nba_dict = create_nba_dict()
    probs_dict = FiveThirtyEight()
    url_dict = create_espn_urls(probs_dict)
    espn_dict = create_espn_dict(url_dict, probs_dict, nba_dict)
    team_dict = create_team_dict(probs_dict, espn_dict)

    # Use data structure to calculate the score for each team
    for stats in team_dict.values():
        stats.update({'shooting_score': 0})
        stats.update({'score': 0})
        stats.update({'kenpom_score': 0})
    
    for team, stats in team_dict.items():
        stats['kenpom_score'] += float(stats['AdjEM']) 
        if team == 'Providence':
            cinderella_boost = 10
            stats['score']+=cinderella_boost
        elif stats['ffour'] == 1:
            playin_boost = 5
            stats['score']+=playin_boost
        for player, attributes in stats['roster'].items():
            if (player in savage_list and float(attributes['3p%']) >= 33.5):
                stats['score']+=5
            if attributes['height'] == '7-0' or attributes['height'] == '7-1' or attributes['height'] == '7-2' or attributes['height'] == '7-3' or attributes['height'] == '7-4' or attributes['height'] == '7-5' or int(attributes['Athleticism'])>=8:
                stats['score']+=2
            if attributes['height'] == '6-8' or attributes['height'] == '6-9' or attributes['height'] == '6-10' or attributes['height'] == '6-11':
                stats['score'] += 1
            if float(attributes['3p%']) >= 40.0 or int(attributes['Jump Shot'])>=7:
                stats['shooting_score'] += 2
                stats['score'] += 2
            if float(attributes['3p%']) >= 33.5 or player in snipers:
                stats['shooting_score'] += 1
                stats['score'] += 1
            if attributes['prospect'] == 1 or player in clutch:
                stats['score'] += 2
            if attributes['Wooden'] == 'yes':
                stats['score'] += 5
            if player in primary_guard_list:
                stats['score']+=5

    # data dump for simulation
    JSON_obj = json.dumps(team_dict, indent = 4)
    print(JSON_obj)
    #pp.pprint(team_dict)
    # dataset composition: espn_player_dict, probs_dict, nba_dict, team_dict, wooden