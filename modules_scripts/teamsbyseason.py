# %%
# This script will pull all active teams in the seasons defined below, along with a 
# series of attributes describing season-long stats.

# This list of teams and seasons should be used to pull individual game box scores, to be stored in a new
# csv file 

import pandas as pd
import numpy as np
from sportsipy.ncaab.schedule import *
from sportsipy.ncaab.teams  import *

#create series of all NCAAB teams in 2009/2010 season

#Create a series of seasons to be included
seasons = ["2010", "2011", "2012", "2013"]
#Create an empty series to be filled with iterative team/season combos
teamsBySeason = []

for i in seasons:
    teams = Teams(i).dataframes
    teamsBySeason.append(teams)



# %%
teamsBySeason=pd.concat(teamsBySeason)

# %%
teamsBySeason.to_csv("../data/teams_2010_2014.csv")


