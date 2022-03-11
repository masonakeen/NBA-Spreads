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





# %%
#create dataframe of all NCAAB team schedules in 2009/2010 season - over 10k games
schedule_df = []
teams2016 = Teams(year="2016")
for team in teams2016:
    schedule = Schedule(team.abbreviation, year="2016").dataframe_extended
    schedule_df.append(schedule)

# %%
schedule_df = pd.concat(schedule_df)
schedule_df.describe()

# %%
# Write dataframe to a new CSV before we start chopping it up
schedule_df.to_csv("../data/2016schedule_allteams.csv")

# %%
# Pull a new dataframe from what we just created, so that we have something to fall back on
schedule_df = pd.read_csv("../data/2016schedule_allteams.csv")

# Drop unnecessary and edge case columns and rows
schedule_df.drop(columns=['time'], axis=1, inplace=True)
schedule_df.dropna(axis=0, subset=['boxscore_index'], inplace=True)
schedule_df.drop(columns=['opponent_rank'], inplace=True)

# %%
schedule_df.isnull().sum()

# %%
# Drop all games against non-D1 opponents
schedule_df = schedule_df[schedule_df.opponent_conference != "Non-DI School"]

# %%
schedule_df.head()


