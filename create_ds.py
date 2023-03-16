import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from lxml import etree
import os

update_dict = {   
    'Athleticism': '0',
    'Ball Handling': '0',
    'Defense': '0',
    'Intangibles': '0',
    'Jump Shot': '0',
    'Leadership': '0',
    'NBA Ready': '0',
    'Passing': '0',
    'Potential': '0',
    'Quickness': '0',
    'Size': '0',
    'Strength': '0',
    'height': '0',
    'position': '0',
    'stock': '0',
    'team': '0',
    'yr': '0',
    'prospect': 0
}

# BIAS STRUCTURES
wooden = [
    'Zach Edey',
    'Trayce Jackson-Davis',
    'Jaime Jaquez Jr.',
    'Keyontae Johnson',
    'Mike Miles Jr.',
    'Brandon Miller',
    'Kris Murray',
    'Jalen Pickett',
    'Marcus Sasser',
    'Drew Timme',
    'Oscar Tshiebwe',
    'Azuolas Tubelis',
    'Jalen Wilson',
    'Isaiah Wong'   
]

# https://www.sbnation.com/college-basketball/2023/3/14/23629013/march-madness-best-players-ranked-ncaa-tournament-2023-men
primary_guard_list = [
    'Marcus Sasser',
    'Jalen Pickett',
    'Keyonte George',
    'Terrence Shannon Jr.',
    'Isaiah Wong',
    'Colby Jones',
    'Max Abmas',
    'Mike Miles Jr.',
    'Marcus Carr',
    'Kendric Davis',
    'Markquis Nowell',
    'Wade Taylor IV',
    'Nick Smith Jr.',
    'Terquavion Smith',
    'Reece Beekman',
    'Boo Buie',
    'Julian Strawther',
    'Tyson Walker',
    'Grant Singleton',
    'Jalen Hood-Schifino',
    'Jordan Hawkins',
    'Cason Wallace'
]

# ESPN eye test based on kenpom underseeds
stepup_clutch = [
    'Jarkel Joiner',
    'Tristen Newton',
    'Keonte Kennedy',
    'Desmond Cambridge Jr.',
    'DJ Horne',
    'Frankie Collins',
    'Kedrian Johnson',
    'Joe Toussaint',
    'Josiah-Jordan James',
    'Jaylen Clark',
    "Sir'Jabarri Rice",
    'Kam Jones',
    'Souley Boum',
    'Johnell Davis',
    'Alijah Martin',
    'Michael Forrest',
    'Allen Flanigan',
    'Wendell Green Jr.',
    'Noah Locke',
    'Bryce Hopkins',
    'Jamarius Burton',
    'Boogie Ellis',
    'Marcus Shaver Jr.',
    'Hakim Hart',
    'Jahmir Young'
]

snipers = [
    'Gradey Dick',
    'Aidan Mahaney',
    'Steven Ashworth',
    'Tucker Richardson'
]

# Eye test - Neural Network eventually?
savage_list = [
    'Brandon Miller',
    'Nick Smith Jr.',
    'Jarace Walker',
    'Noah Clowney',
    'Keyonte George',
    'Terquavion Smith',
    'Jordan Hawkins',
    'Cason Wallace',
    'Adam Flagler',
    'Ricky Council IV',
    'Jalen Hood-Schifino',
    'Keyontae Johnson',
    'Marcus Sasser',
    'Terrence Shannon Jr.',
    'Seth Lundy',
    'Isaiah Wong',
    'Mark Mitchell',
    'Dariq Whitehead',
    'Jaime Jaquez Jr.',
    'Amari Bailey',
    'Reece Beekman',
    'Julian Phillips',
    'Trey Alexander',
    'Tramon Mark',
    'Tyrese Hunter',
    'Adama Sanogo',
]