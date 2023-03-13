import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import sys

'''
# URL of the statistics page for the men's basketball team
url = 'https://www.espn.com/mens-college-basketball/team/stats/_/id/26'

# Optional Meth1: Make a GET request to the URL and get the HTML content
response = requests.get(url)
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')

# Meth2: Pandas uses BeautifulSoup under the hood
dfs = pd.read_html(url)

df = dfs[0].join(dfs[1])
df[['Name','Team']] = df['Name'].str.extract('^(.*?)([A-Z]+)$', expand=True)
#print(df)
'''

# Open json file
f = open('kenpom.json')

# Returns json object as a dictionary
data = json.load(f)

# Create a team dictionary
team_dict = {}
for team in data["kenpom"]:
    team_dict[team['name']] = [team['rk'], team['AdjEM'], team["AdjO"], team["AdjD"]]



url_dict = {
    '1': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/248',
    '2': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/26',
    '3': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/333',
    '4': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/41',
    '5': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2633',
    '6': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/251',
    '7': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2509',
    '8': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2250',
    '9': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2305',
    '10': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/12',
    '11': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2608',
    '12': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/269',
    '13': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/156',
    '14': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/21',
    '15': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/239',
    '16': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2752',
    '17': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/277',
    '18': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/328',
    '19': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/235',
    '20': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/8',
    '21': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/150',
    '22': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/120',
    '23': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/66',
    '24': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2306',
    '25': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/245',
    '26': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2226',
    '27': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2628',
    '28': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/96',
    '29': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2',
    '30': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/84',
    '31': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/68',
    '32': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/127',
    '33': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/356',
    '34': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/258',
    '36': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/30',
    '37': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2294',
    '39': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/213',
    '40': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2390',
    '42': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/77',
    '43': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2440',
    '44': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2507',
    '49': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/344',
    '51': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/142',
    '55': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/152',
    '56': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/198',
    '58': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2670',
    '66': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2181',
    '68': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/9',
    '71': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2309',
    '73': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/232',
    '74': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/314',
    '77': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/221',
    '89': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/231',
    '92': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/309',
    '102': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2540',
    '109': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2253',
    '110': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/147',
    '112': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/163',
    '113': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/261',
    '114': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2142',
    '127': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/338',
    '146': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2427',
    '161': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/94',
    '170': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/357',
    '215': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/47',
    '257': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2546',
    '285': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/2640',
    '312': 'https://www.espn.com/mens-college-basketball/team/stats/_/id/161'
}

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
        dictionary[row['Name'].strip()] = [row['GP'], row['MIN'], row['PTS'], row['REB'], row['FT%'], row['3P%'], row['Team'], row['Kenpom']]
    espn_player_dict.update(dictionary)

print(espn_player_dict)