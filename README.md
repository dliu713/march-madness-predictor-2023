# march-madness-predictor-2023

Model for predicting the 2023 March Madness bracket.  Combines various sources of online data (kenpom, espn, fivethirtyeight, etc) in order to develop a comprehensive algorithm.  Weighting and built-in trends were applied to fundamental weights extracted from data calculations and manually created structures. Simulation is designed to be run until a full bracket is generated.

Usage:
At command line:
> python3 scraper_final.py > teams.json

> python3 test_sim.py

Results:
Example run:
['Alabama', 'Maryland', 'Charleston', 'Furman', 'Creighton', 'Baylor', 'Utah St.', 'Arizona']
['Purdue', 'Memphis', 'Duke', 'Tennessee', 'Kentucky', 'Kansas St.', 'Michigan St.', 'Vermont']
['Houston', 'Iowa', 'Miami FL', 'Indiana', 'Pittsburgh', 'Xavier', 'Penn St.', 'Texas']
['Kansas', 'Arkansas', "Saint Mary's", 'Connecticut', 'Arizona St.', 'Gonzaga', 'Northwestern', 'UCLA']
['Alabama', 'Charleston', 'Baylor', 'Arizona']
['Memphis', 'Tennessee', 'Kentucky', 'Michigan St.']
['Houston', 'Indiana', 'Xavier', 'Penn St.']
['Arkansas', 'Connecticut', 'Gonzaga', 'UCLA']
['Alabama', 'Arizona']
['Memphis', 'Kentucky']
['Houston', 'Xavier']
['Arkansas', 'UCLA']
['Alabama', 'Kentucky', 'Houston', 'UCLA']
['Alabama', 'Houston']
Houston

Simulation:
First Round Results
{'Alabama': 1000,
 'Maryland': 1000,
 'Baylor': 1000,
 'Memphis': 1000,
 'Duke': 1000,
 'Kentucky': 1000,
 'Michigan St.': 1000,
 'Houston': 1000,
 'Iowa': 1000,
 'Miami FL': 1000,
 'Indiana': 1000,
 'Texas': 1000,
 'Kansas': 1000,
 'Arkansas': 1000,
 'Connecticut': 1000,
 'UCLA': 1000,
 'Purdue': 999,
 'Penn St.': 998,
 'Kansas St.': 997,
 'Pittsburgh': 996,
 'Gonzaga': 992,
 'Arizona': 990,
 'San Diego St.': 896,
 'VCU': 896,
 'Furman': 720,
 'Tennessee': 720,
 'Xavier': 632,
 'Vermont': 610,
 'Boise St.': 579,
 'Missouri': 577,
 'N.C. State': 559,
 'TCU': 555,
 'Arizona St.': 445,
 'Creighton': 441,
 'Utah St.': 423,
 'Northwestern': 421,
 'Marquette': 390,
 'Kennesaw St.': 368,
 'Virginia': 280,
 'Louisiana': 280,
 'Charleston': 104,
 "Saint Mary's": 104,
 'Princeton': 10,
 'Grand Canyon': 8,
 'Iowa St.': 4,
 'Montana St.': 3,
 'Texas A&M': 2,
 'Fairleigh Dickinson': 1}

Second Round Results
{'Alabama': 1000,
 'Kentucky': 1000,
 'Michigan St.': 1000,
 'Houston': 1000,
 'Indiana': 1000,
 'Connecticut': 1000,
 'UCLA': 1000,
 'Baylor': 999,
 'Gonzaga': 987,
 'Arkansas': 983,
 'Arizona': 964,
 'Memphis': 731,
 'Tennessee': 720,
 'San Diego St.': 648,
 'Xavier': 618,
 'Texas': 596,
 'Penn St.': 404,
 'Pittsburgh': 381,
 'Virginia': 280,
 'Duke': 280,
 'Purdue': 269,
 'Charleston': 72,
 'Missouri': 30,
 'Kansas': 17,
 'TCU': 8,
 'Utah St.': 6,
 'Arizona St.': 5,
 'Creighton': 1,
 'Iowa St.': 1}

Sweet 16 Results
{'UCLA': 1000,
 'Alabama': 983,
 'Arkansas': 975,
 'Houston': 966,
 'Arizona': 964,
 'Kentucky': 962,
 'Memphis': 654,
 'Texas': 596,
 'Xavier': 358,
 'Tennessee': 186,
 'Duke': 152,
 'Penn St.': 42,
 'Michigan St.': 38,
 'Baylor': 36,
 'Indiana': 34,
 'Connecticut': 25,
 'Virginia': 17,
 'Purdue': 8,
 'Pittsburgh': 4}

Elite 8 Results
{'Alabama': 980,
 'Houston': 966,
 'UCLA': 962,
 'Kentucky': 410,
 'Memphis': 357,
 'Duke': 117,
 'Tennessee': 109,
 'Arkansas': 26,
 'Texas': 24,
 'Arizona': 17,
 'Connecticut': 12,
 'Xavier': 10,
 'Purdue': 7,
 'Baylor': 3}

Final Four Results
{'Alabama': 973,
 'Houston': 966,
 'UCLA': 27,
 'Arizona': 14,
 'Duke': 6,
 'Kentucky': 4,
 'Connecticut': 3,
 'Texas': 3,
 'Baylor': 2,
 'Xavier': 1,
 'Tennessee': 1}

 Champions
{'Houston': 966, 'Alabama': 30, 'UCLA': 4}
