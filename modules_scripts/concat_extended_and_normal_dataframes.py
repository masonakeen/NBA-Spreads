# %%
# %%
# Key features (include opponent's as well)
#   - Home vs. Away vs. Neutral
#   - Offensive Eff, or Offensive eFG%
#   - Turnover Percentage
#   - Rebounding
#   - Free Throws
#   - Seniority (collective games played for team?)
#   - Streak (last 5 games result)


# %%
import pandas as pd
from datetime import datetime
from sportsipy.ncaab.boxscore import *
from sportsipy.ncaab.schedule import *
from sportsipy.ncaab.teams import *
from sportsipy.ncaab.conferences import *
import seaborn as sns
import matplotlib as plt
from glob import glob
import os



# %%
#set counter
cnt = 0

# pull all files from directory
filenames = sorted(glob('../data/team_csvs/2019-2020/*.csv'))

#loop through all files in glob (~350 files)
for file in filenames:
    try:
        cnt += 1
        print(cnt)
        #create dataframe based on file
        df = pd.read_csv(file)

        # read the team abbreviation from the df column and assign it as team variable
        team_name = df.loc[0,'team_name']

        #replace spaces in team_name with a dash and all caps
        team_abbr = team_name.replace(" ", "-")

        #get the schedule for the team - THIS ISN'T WORKING 
        schedule_df = Schedule(team_abbr, year="2019").dataframe

        #join the schedule DF to the original df that we read from the csv
        df.join(schedule_df, lsuffix='main', rsuffix='other')

        #overwrite the csv - in this case, we are worried about errors so we'll write to a new folder with the same file name
        df.to_csv(f'../data/team_csvs/2019-2020v2/{cnt}_{team_name}_season_boxscores_2019.csv')
    except:
        print(cnt, 'didnt work')


# %%


# %%


# %%



