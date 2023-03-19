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

# BIAS STRUCTURES - manual work knowledge
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
# eye test --neural network/ai/manual? go to espn, film, and images to identify biometrics, killers, reasonable jumper 33.5+, role sniper 39.5%+, ppg >= 9.5, min >= 12.5
    # for shooters, check attempts if 50% or more and makes
# good teams with good guards eye test:
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
    'Cason Wallace',
]

# cinderella/underrated eye test based on seeds 7+ and kenpom underseeds, ignore if in primary_guards or snipers, pick one 16 seed w/ the most savages to add
savage = [
    'Alex Karaban',
    'Tristen Newton',
    'Adama Sanogo',
    'Chase Audige',
    'Joey Hauser',
    'Jaden Akins',
    'Kobe Brown',
    "D'Moi Hodge",
    'DeAndre Gholston',
    'Wade Taylor IV',
    'Andrew Funk',
    'Max Rice',
    'Chibuzo Agbo',
    'Boogie Ellis',
    'Hakim Hart',
    'Jahmir Young',
    'Keonte Kennedy',
    'DeAndre Williams',
    'Davonte Davis',
    'Kedrian Johnson',
    'Joe Toussaint',
    'Allen Flanigan',
    'Wendell Green Jr.',
    'Johnell Davis',
    'Alijah Martin',
    'Michael Forrest',
    'Jarkel Joiner',
    'Casey Morsell',
    'Jamarius Burton',
    'Blake Hinson',
    'Bryce Hopkins',
    'Noah Locke',
    'Desmond Cambridge Jr.',
    'DJ Horne',
    'Frankie Collins',
    'Devan Cambridge',
    'Claudell Harris Jr.',
    'Tahlik Chavez',
    'Tyeree Bryan',
    'Tucker DeVries',
    'Isaiah McBride',
    'Adrian Baldwin Jr.',
    'Jayden Nunn',
    'Greg Williams Jr.',
    'Walter Clayton Jr.',
    'Daniss Jenkins',
    'Mike Bothwell',
    'Jalen Slawson',
    'JP Pegues',
    'Marcus Foster',
    'Malique Jacobs',
    'Chris Youngblood',
    'Terrell Burden',
    'Brandon Stroud',
    'Tosan Evbuomwan',
    'Matt Allocco',
    'Miles Norris',
    'RaeQuan Battle',
    'Chance McMillian',
    'Taijon Jones'
    'Aaron Deloney'
    'Oliver Lynch-Daniels'
    'Josiah-Jordan James',
    'Jaylen Clark',
    "Sir'Jabarri Rice",
    'Kam Jones',
    'Souley Boum',
    'Antonio Reeves',
    'Jacob Toppin',
    'Demetre Roberts',
    'Grant Singleton',
    'Ansley Almonor',
    'Joe Munden Jr.',
    'Sean Moore',
    'Jeremy Roach'
]


# Possible best shooter in the tourney
snipers = [
    'Gradey Dick',
    'Aidan Mahaney',
    'Steven Ashworth',
    'Tucker Richardson'
]

# Eye test of nba_prospects - Neural Network eventually?
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
    'Jaime Jaquez Jr.',
    'Amari Bailey',
    'Reece Beekman',
    'Julian Phillips',
    'Trey Alexander',
    'Tramon Mark',
    'Tyrese Hunter',
    'Chris Livingston',
]