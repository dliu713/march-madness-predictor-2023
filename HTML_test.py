import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import sys
from lxml import etree
import os

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

# Load NBA Prospect json
f = open('nba_prospects.json')
data = json.load(f)
nba_dict = {}
for player in data['player']:
    nba_dict[player['name']] = [player['url'], player['rank'], player['height'], player['position'], player['team'], player["yr"]]
#print(nba_dict)

for player, val in nba_dict.items():
    url = val[0]
    attr_dict = get_nba_attr(url)
    attr_dict['stock'] = val[1]
    attr_dict['height'] = val[2]
    attr_dict['position'] = val[3]
    attr_dict['team'] = val[4]
    attr_dict['yr'] = val[5]
    nba_dict[player] = attr_dict

print(nba_dict)

