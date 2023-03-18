# march-madness-predictor-2023

Model for predicting the 2023 March Madness bracket.  Combines various sources of online data (kenpom, espn, fivethirtyeight, etc) in order to develop a comprehensive algorithm.  Weighting and built-in trends were applied to fundamental weights extracted from data calculations and manually created structures. Simulation is designed to be run until a full bracket is generated.

Usage:
At command line:
> python3 scraper_final.py > teams.json
> python3 test_sim.py

