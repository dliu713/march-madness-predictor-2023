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

# BIAS STRUCTURES - manual work knowledge, all wooden lists +5, comment out obsolete bigs
wooden = [
    'Marcus Carr',
    'Kendric Davis',
    'Gradey Dick',
    #'Zach Edey',
    #'Kyle Filipowski',
    'Adam Flagler',
    'Keyonte George',
    #'Trayce Jackson-Davis',
    'Jaime Jaquez Jr.',
    'Keyontae Johnson',
    'Mike Miles Jr.',
    'Brandon Miller',
    'Kris Murray',
    'Adama Sanogo',
    'Markquis Nowell',
    'Jalen Pickett',
    'Marcus Sasser',
    'Terquavion Smith',
    #'Drew Timme',
    #'Oscar Tshiebwe',
    #'Azuolas Tubelis',
    'Jalen Wilson',
    'Isaiah Wong'   
]

# eye test --neural network/ai/manual? go to espn, film, and images to identify biometrics, killers, reasonable jumper 33.5+, role sniper 39.5%+, ppg >= 8-9.5, min >= 12.5
    # for shooters, check attempts if 50% or more and makes

# Eye test on nba_prospects not in wooden +5 - Neural Network eventually?
savage_list = [
    'Nick Smith Jr.',
    'Jarace Walker',
    'Noah Clowney',
    'Jordan Hawkins',
    'Cason Wallace',
    'Julian Strawther',
    'Ricky Council IV',
    'Andre Jackson Jr.',
    'Jalen Hood-Schifino',
    'Terrence Shannon Jr.',
    'Arthur Kaluma',
    'Mark Mitchell',
    'Amari Bailey',
    'Reece Beekman',
    'Julian Phillips',
    'Trey Alexander',
    #'Jaylen Clark',
    'Tramon Mark',
]

# good teams with good guards eye test not nba prospects or wooden +5:
# https://www.sbnation.com/college-basketball/2023/3/14/23629013/march-madness-best-players-ranked-ncaa-tournament-2023-men
primary_guard_list = [
    'Colby Jones',
    'Max Abmas',
    'Matt Bradley',
    'Wade Taylor IV',
    'Boo Buie',
    'Tyson Walker',
    'Grant Singleton',
]

# Possible best shooter in the tourney +1 to shotscore
snipers = [
    'Andrew Funk',
    'Aidan Mahaney',
    'Steven Ashworth',
    'Tucker Richardson'
]

# +2 eye test, be lenient to underrated kenpom and lower seeded teams, ignore if in wooden, primary_guards, savage_list, or snipers, (pick one 16 seed w/ the most savages to add)
dogs = [
    'Chase Audige',

    'Joey Hauser',
    'Jaden Akins',

    'Kobe Brown',
    "D'Moi Hodge",
    'DeAndre Gholston',

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
    'Nicholas Boyd',
    'Bryan Greenlee',

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

    'Taijon Jones',

    'Aaron Deloney',

    'Demetre Roberts',
    'Ansley Almonor',
    'Joe Munden Jr.',
    'Sean Moore',

    'Oliver Lynch-Daniels',

    'Seth Lundy',

    'Alex Karaban',
    'Tristen Newton',

    'Jamal Shead',

    'Dajuan Harris Jr.',

    'Courtney Ramey',

    'Mark Sears',
    'Jahvon Quinerly',

    'Josiah-Jordan James',

    'Tyger Campbell',
    'Adem Bona',

    'LJ Cryer',

    "Sir'Jabarri Rice",
    'Tyrese Hunter',

    'Kam Jones',

    'Souley Boum',

    'Antonio Reeves',
    'Jacob Toppin',

    'Jeremy Roach',

    'Adam Kunkel',

    "Nae'Qwan Tomlin",
    'Desi Stills',

    'Rasir Bolton',
    'Malachi Smith',

    'Armaan Franklin',

    'Ryan Nembhard',

    'Xavier Johnson',

    'Darrion Trammell',
    'Lamont Butler',

    'Alex Ducas',

    'Jordan Miller',
    'Nijel Pack',
    'Norchad Omier',
    'Wooga Poplar',

    'Damion Baugh',
    'Emanuel Miller',
]

# features
SAVloc = [
    'Marcus Carr',
    'Keyontae Johnson',
    'Markquis Nowell',
    'Terquavion Smith',
    'Isaiah Wong',
    'Julian Phillips',
    'Trey Alexander',
    'Marcus Sasser',
    'Tramon Mark',
    'Hakim Hart',
    'Michael Forrest',
    'DJ Horne',
    'Jayden Nunn',
    'Brandon Stroud',
    'Demetre Roberts',
    'Tristen Newton',
    "Sir'Jabarri Rice",
    'Darrion Trammell',
    'Allen Flanigan',
    'Jordan Miller'
]