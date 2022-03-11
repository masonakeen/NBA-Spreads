# %%

# NOTE - the problem with this is that it eventually fails due to an int and str type in the boxscore and home_team - they should both be strs
# NOTE- bigger problem is that the merge creates extra columns on each loop. I think this is because the merge from homestats to merged_df 
#       basically tells the columns on homestats to add a suffix - each consecutive one adds a set of columns
#       can I merge andoverwrite left with right columns?
import pandas as pd
import numpy as np
import seaborn as sns
import os
from sportsipy.ncaab import boxscore
from sportsipy.ncaab.teams import Teams
from sportsipy.ncaab.teams import Team

# %%


# %%
mega_df = pd.read_csv('../data/2019_ncaa_season_boxscores_trimmed.csv')

# %%
mega_df.head()



# %%
mega_df.drop(columns = ['away_defensive_rating', 'away_effective_field_goal_percentage', 'away_free_throw_attempt_rate', 'away_offensive_rating', 'away_three_point_field_goal_percentage', 'away_total_rebound_percentage', 'away_true_shooting_percentage', 'away_turnover_percentage', 'away_win_percentage' ], inplace=True)

# %%
mega_df.drop(columns = ['home_defensive_rating' , 'home_defensive_rating', 'home_effective_field_goal_percentage', 'home_free_throw_attempt_rate', 'home_free_throw_percentage', 'home_offensive_rating' , 'home_three_point_field_goal_percentage', 'home_total_rebound_percentage', 'home_true_shooting_percentage' ], inplace=True )

# %%
#mega_df.drop(columns = ['home_turnover_percentage', 'home_wins'], inplace=True)
mega_df.drop(columns='Unnamed: 0.1', inplace=True)

# %%
#mega_df.drop_duplicates(subset=['boxscore'], keep='first', inplace=True)

# %%
mega_df.reset_index(inplace=True)

# %%
mega_df.drop(columns=['index', 'Unnamed: 0'], inplace=True)

# %%
mega_df.head(10)

# %%


# %%
teamsdf = pd.read_csv('../data/team_csvs/2019-2020/teams.csv')

# %%
teamsdf.drop(teamsdf.columns.difference(['abbreviation', 'name']), axis=1, inplace=True)
teamsdf.head()

# %%
teamsdf['home_team'] = teamsdf['abbreviation']

# %%
teamsdf['away_team'] = teamsdf['abbreviation']

# %%
teamsdf.head()

# %%
merged_df = mega_df.merge(teamsdf, on='home_team', suffixes=(None, '_home'))

# %%
merged_df.rename(columns= {'name': 'home_team_name'}, inplace=True)

# %%
merged_df.drop(columns=['abbreviation', 'away_team_home'], inplace=True)

# %%
merged_df = merged_df.merge(teamsdf, on='away_team', suffixes=(None, '_away'))
merged_df.head()

# %%
merged_df.rename(columns={'name': 'away_team_name'}, inplace=True)
merged_df.drop(columns = ['abbreviation', 'home_team_away'], inplace=True)
merged_df.head()

# %%


# %%
merged_df_copy = merged_df
merged_df_copy.head()

# %%
merged_df.head()

# %%
#merged_df[merged_df['boxscore'] == '2018-11-15-21-texas-christian']

#merged_df.head()

# %%
merged_df.drop_duplicates(subset='boxscore', keep='first', inplace=True)
merged_df['home_team_name'].str.lstrip()
merged_df['homeindex'] = merged_df['boxscore'] + merged_df['home_team_name']
merged_df.head()

merged_df['away_team_name'].str.lstrip()
merged_df['awayindex'] = merged_df['boxscore'] + merged_df['away_team_name']
merged_df.head()

# %%
merged_df.info()

# NEed to make sure that the team's DF columns don't join if they are dupes of the existing ones (boxscore, team_name)

# %%
merged_df[ 'home_pregame_eFG'] = np.nan
merged_df[ 'home_pregame_rebound_percentage'] = np.nan
merged_df[ 'home_pregame_eFG_allowed'] = np.nan
merged_df['home_pregame_win_percentage'] = np.nan

merged_df[ 'away_pregame_eFG'] = np.nan
merged_df[ 'away_pregame_rebound_percentage'] = np.nan
merged_df[ 'away_pregame_eFG_allowed'] = np.nan
merged_df['away_pregame_win_percentage'] = np.nan

# %%
merged_df.head()

# %%
merged_df.reset_index(drop=True, inplace=True)
merged_df.head()


# %%
#merged_df.drop(columns = ['index'], axis = 1, inplace=True)
merged_df.head()

# %%
cnt = 0

#make a copy of the current 0-5000 index and create a new one equal to homeindex
merged_df['uid'] = merged_df.index
merged_df.set_index('awayindex', drop=True, inplace=True)


boxscore_list = merged_df['boxscore'].tolist()
for i in boxscore_list:
    try: 
        #Create the bool mask so that we are only dealing with a subset. This will return a df with only one entry - the one that matches the boxscore
        mask = merged_df[merged_df['boxscore'] == i]
        mask.reset_index(drop=False, inplace=True)
        # get the team name that we're retrieving stats for. You don't need the abbreviation - could remove later
        away_team_name = mask.at[cnt, 'away_team_name']
        away_team_abbrev = mask.at[cnt, 'away_team']
        print(away_team_name)
        print(away_team_abbrev)

        # Pull the dataframe from the team's CSV. You'll then trim down the DF and rename it so it only reflects the home team's stats. These will 
        # join to the main dataframe and appear as home team pregame stats
        awaystats_df = pd.read_csv('../data/team_csvs/2019-2020/{}_season_boxscores_2019.csv'.format(away_team_name))
        awaystats_df = awaystats_df[['boxscore','team_name', 'pregame_eFG','pregame_rebound_percentage','pregame_eFG_allowed','pregame_win_percentage']]
        awaystats_df.rename(columns={'pregame_eFG': 'away_pregame_eFG','pregame_rebound_percentage': 'away_pregame_rebound_percentage','pregame_eFG_allowed': 'away_pregame_eFG_allowed','pregame_win_percentage': 'away_pregame_win_percentage'}, inplace=True)
        
        # Create the special index for this DF to enable the join
        awaystats_df['awayindex'] = homestats_df['boxscore'] + homestats_df['team_name']
        awaystats_df.set_index('awayindex', drop=True, inplace=True)
        # Now we will merge the home team stats onto the main dataframe. Creating a concatenated index column will help make sure we don't
        # assume that the team is home for every boxscore. For instance, TCU stats won't be applied as home stats for every boxscore they played
        # in the main DF
        # Outer join will also leave unimpacted boxscore rows to be filled later

        # if below doesn't work, try taking out the index
        #    merged_df = merged_df.merge(homestats_df, how='left', on='homeindex', suffixes=(None, '_drop'))
        merged_df.update(awaystats_df)
        # above will replace the empty cells in merged_df with the homestats_df values. won't affect other values in the df
        #     #cnt +=1
    except:
        print(away_team_name, ' Didnt Work')
   
# The above will spit out a dataframe that has been saved to /data/backup_dataframe_2019games_pregamehomestats.csv
# It's missing Abilene Christian games only - will need to come back to that, but the script runs really fast and should only need a minute or two once I add the ACU schedule

# %%
mask.head()

# %%
awaystats_df.head()

# %%
merged_df.head(160)

# %%
merged_df.to_csv('../data/backup_dataframe_2019games_pregameawaystats.csv')


# %%
del merged_df
merged_df = pd.read_csv('../data/backup_dataframe_2019games_pregameawaystats.csv')

# %%
merged_df.head()

# %%
home_df = pd.read_csv('../data/backup_dataframe_2019games_pregamehomestats.csv')

home_df.head()

# %%
merged_df[ 'home_pregame_eFG'] = np.nan
merged_df[ 'home_pregame_rebound_percentage'] = np.nan
merged_df[ 'home_pregame_eFG_allowed'] = np.nan
merged_df['home_pregame_win_percentage'] = np.nan

# %%
merged_df.reset_index(drop=False, inplace=True)
merged_df.head()

# %%
merged_df.drop('index', axis=1, inplace=True)
merged_df.set_index('boxscore', drop=True, inplace=True)
home_df.set_index('boxscore', drop=True, inplace=True)

# %%
merged_df.update(home_df)

# %%
merged_df.head()

# %%
merged_df.drop(['uid', 'home_wins', 'home_turnover_percentage', 'awayindex', 'pace'], axis=1, inplace=True)

# %%
merged_df.head()

# %%
merged_df.to_csv('../data/2018-2019_pregamestatsfinal.csv')

# %%
merged_df.hist(bins=10)


