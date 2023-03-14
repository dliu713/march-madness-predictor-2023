import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import sys
from lxml import etree
import os
import pprint
from manual_ds import espn_url_dict as url_dict
from manual_ds import wooden

pp = pprint.PrettyPrinter(indent=4)

def scrape_espn(url_dict):
    espn_player_dict = {}
    for key, val in url_dict.items():
        dfs = pd.read_html(val)
        df = dfs[0].join(dfs[1])
        df[['Name','Team']] = df['Name'].str.extract('^(.*?)([A-Z]+)$', expand=True)
        for i in range(len(df.index)):
            df['Kenpom'] = key

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
                'kenpom': row['Kenpom']
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

# Open json file
f = open('kenpom.json')

# Returns json object as a dictionary
data = json.load(f)

# Create a team dictionary (or instances?)
team_dict = {}
for team in data["kenpom"]:
    team_dict[team['rk']] = {
        "name": team['name'], 
        "AdjEM": team['AdjEM'], 
        "AdjO": team["AdjO"], 
        "AdjD": team["AdjD"], 
        "seed": team["seed"], 
        "Conf": team["Conf"]
    }
#pp.pprint(team_dict)

# Scrape ESPN
espn_player_dict = scrape_espn(url_dict)
#pp.pprint(espn_player_dict)

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

#pp.pprint(nba_dict)

# Load FiveThirtyEight json
f = open('fivethirtyeight.json')
data = json.load(f)
probs_dict = {}
for team in data:
    probs_dict[team["team_id"]] = [team["team_name"], team["rd7_win"]]
#pp.pprint(probs_dict)

# Construct final team data structure
for player, attrs in nba_dict.items():
    espn_player_dict[player].update(attrs)

for player, val in espn_player_dict.items():
    team_dict[val['kenpom']].update({player: val})
pp.pprint(team_dict)

# Acquire bias data structures
savage_bias = []
for key, val in nba_dict.items():
    if val['Athleticism'] != 'NA' and val['Jump Shot'] != 'NA':
        if int(val['Athleticism']) >= 8 and int(val['Jump Shot']) >= 7:
            savage_bias.append(key)
#print(savage_bias)

# datasets: espn_player_dict, probs_dict, nba_dict, team_dict, savage_bias, wooden