# march-madness-predictor-2023

Model for predicting the 2023 March Madness bracket.  Combines various sources of online data (kenpom, espn, fivethirtyeight, etc) in order to develop a comprehensive algorithm.  Weighting and built-in trends were applied to fundamental weights extracted from data calculations. Simulation is designed to be run by the user until a full bracket is generated.

test.py sim example run:
{'Alabama': 'Texas A&M Corpus Chris', 'Maryland': 'West Virginia', 'San Diego St.': 'Charleston', 'Virginia': 'Furman', 'Creighton': 'N.C. State', 'Baylor': 'UC Santa Barbara', 'Missouri': 'Utah St.', 'Arizona': 'Princeton'}
['Alabama', 'West Virginia', 'Charleston', 'Virginia', 'Creighton', 'Baylor', 'Missouri', 'Arizona']
['Alabama', 'Virginia', 'Baylor', 'Arizona']
['Alabama', 'Baylor']
Alabama
{'Houston': 'Northern Kentucky', 'Iowa': 'Auburn', 'Miami FL': 'Drake', 'Indiana': 'Kent St.', 'Iowa St.': 'Mississippi St.', 'Xavier': 'Kennesaw St.', 'Texas A&M': 'Penn St.', 'Texas': 'Colgate'}
['Houston', 'Auburn', 'Drake', 'Kent St.', 'Mississippi St.', 'Xavier', 'Penn St.', 'Texas']
['Auburn', 'Drake', 'Xavier', 'Penn St.']
['Auburn', 'Penn St.']
Penn St.
{'Purdue': 'Texas Southern', 'Memphis': 'Florida Atlantic', 'Duke': 'Oral Roberts', 'Tennessee': 'Louisiana', 'Kentucky': 'Providence', 'Kansas St.': 'Montana St.', 'Michigan St.': 'USC', 'Marquette': 'Vermont'}
['Purdue', 'Oral Roberts', 'Tennessee', 'Providence', 'Kansas St.', 'Michigan St.', 'Marquette']
Trends not passed, please run again
(base) davidliu@Davids-MacBook-Pro march-madness-predictor-2023 % python3 test.py
{'Alabama': 'Texas A&M Corpus Chris', 'Maryland': 'West Virginia', 'San Diego St.': 'Charleston', 'Virginia': 'Furman', 'Creighton': 'N.C. State', 'Baylor': 'UC Santa Barbara', 'Missouri': 'Utah St.', 'Arizona': 'Princeton'}
['Alabama', 'West Virginia', 'San Diego St.', 'Virginia', 'Creighton', 'Baylor', 'Missouri', 'Princeton']
['Alabama', 'Virginia', 'Baylor', 'Princeton']
['Alabama', 'Baylor']
Alabama
{'Houston': 'Northern Kentucky', 'Iowa': 'Auburn', 'Miami FL': 'Drake', 'Indiana': 'Kent St.', 'Iowa St.': 'Mississippi St.', 'Xavier': 'Kennesaw St.', 'Texas A&M': 'Penn St.', 'Texas': 'Colgate'}
['Houston', 'Auburn', 'Drake', 'Indiana', 'Iowa St.', 'Kennesaw St.', 'Texas A&M', 'Texas']
['Houston', 'Drake', 'Kennesaw St.', 'Texas']
['Houston', 'Texas']
Houston
{'Purdue': 'Texas Southern', 'Memphis': 'Florida Atlantic', 'Duke': 'Oral Roberts', 'Tennessee': 'Louisiana', 'Kentucky': 'Providence', 'Kansas St.': 'Montana St.', 'Michigan St.': 'USC', 'Marquette': 'Vermont'}
['Purdue', 'Memphis', 'Duke', 'Tennessee', 'Kentucky', 'Kansas St.', 'Michigan St.', 'Vermont']
['Purdue', 'Tennessee', 'Kansas St.', 'Vermont']
['Tennessee', 'Kansas St.']
Kansas St.
{'Kansas': 'Howard', 'Arkansas': 'Illinois', "Saint Mary's": 'VCU', 'Connecticut': 'Iona', 'TCU': 'Nevada', 'Gonzaga': 'Grand Canyon', 'Northwestern': 'Boise St.', 'UCLA': 'UNC Asheville'}
['Kansas', 'Arkansas', "Saint Mary's", 'Connecticut', 'TCU', 'Gonzaga', 'Northwestern', 'UCLA']
['Kansas', 'Connecticut', 'Gonzaga', 'UCLA']
['Connecticut', 'UCLA']
Connecticut
['Alabama', 'Houston']
Houston