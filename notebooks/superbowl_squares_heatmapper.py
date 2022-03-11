# %%
import pandas as pd
import numpy as np
from sportsipy.nfl.schedule import *
from sportsipy.nfl.boxscore import *


# %%
#Get the URI of the super bowl-
superbowls = pd.DataFrame(columns = ['boxcore', 'away_name', 'away_abbr', 'away_score', 'home_name', 'home_abbr', 'away_score', 'winning_name', 'winning_abbr', 'losing_name', 'losing_abbr'])
for i in range(1990, 2020):
    try:
        season = str(i)
        week21_games = Boxscores(21, season)
        df = pd.concat({k: pd.DataFrame(v) for k, v in week21_games.games.items()}, axis=0)
        superbowls = pd.concat([superbowls, df], sort=False)
    except:
        print(i, " didn't work")
# Boxscore(uri).summary returns a dictionary of home and away scores by quarter {'away': [0,7,3, 14], 'home': [7, 7, 3, 0]}

# %%
superbowls.head()

# %%
# Remove the NaN boxscore column 
superbowls.dropna(axis=1, how='all', inplace=True)

# %%
superbowls.head()

# %%
# Get a List of boxscore URIs that we will use to request game summaries 
boxscorelist = list(superbowls['boxscore'].values)
print(boxscorelist)

# %%
# Clear the scoringsummary variable, then loop through all boxscore URIs
del scoringsummary
scoringsummary = pd.DataFrame()
for i in boxscorelist:
    try: 
        print(i)
        uri = str(i)

        # get the scoring summary by quarter for the given game. Returns a dict
        gameDict = Boxscore(uri).summary
        print(gameDict)

        # turn the dict into a pair of dataframes for home and away, transpose to columns and rename them. Create column for boxscore string
        home_quarters = pd.DataFrame(gameDict.get('home')).T
        away_quarters = pd.DataFrame(gameDict.get('away')).T
        home_quarters.rename(columns ={0: "home_q1", 1: "home_q2", 2: "home_q3", 3: "home_q4"}, inplace=True)
        home_quarters['boxscore'] = uri
        away_quarters.rename(columns ={0: "away_q1", 1: "away_q2", 2: "away_q3", 3: "away_q4"}, inplace=True)
        away_quarters['boxscore'] = uri
        print(home_quarters)
        print(away_quarters)

        # now i have 2 dataframes with the boxscore string and I need to concat them horizontally. Should create 1 row with 8-10 columns
        game_df = pd.concat([home_quarters, away_quarters], axis=1)
        print(game_df)
        
        #concat the empty dataframe with the new row, basically an append
        scoringsummary = pd.concat([scoringsummary, game_df])
    except:
        print(i, " didn't work")


# %%
scoringsummary.describe()

# %%
scoringsummary.to_csv('../data/superbowl_scoringsummaries.csv')

# %%
# dropping duplicate column 
scoringsummary = scoringsummary.loc[:,~scoringsummary.columns.duplicated()]

# %%
scoringsummary.to_csv('../data/superbowl_scoringsummaries.csv')

# %%
superbowls.head()
superbowls.to_csv('../data/superbowl_gamescores.csv')

# %%
# now that I have a dataframe of the scoring summary, I can join it back to the main df
superbowls = pd.read_csv('../data/superbowl_gamescores.csv')
superbowls = superbowls.join(scoringsummary.set_index('boxscore'), on='boxscore')


# %%
superbowls.to_csv('../data/superbowls_detailedscoring.csv')

# %%
superbowls.head()

# %%
# Creating new columns to represent the score at end of each quarter. This will help us get our heatmap for squares
superbowls['home_endq1'] = superbowls['home_q1']
superbowls['home_endq2'] = superbowls['home_q1'] + superbowls['home_q2'] 
superbowls['home_endq3'] = superbowls['home_q1'] + superbowls['home_q2'] + superbowls['home_q3']
superbowls['home_endq4'] = superbowls['home_q1'] + superbowls['home_q2'] + superbowls['home_q3'] + superbowls['home_q4']

# %%
superbowls['away_endq1'] = superbowls['away_q1']
superbowls['away_endq2'] = superbowls['away_q1'] + superbowls['away_q2'] 
superbowls['away_endq3'] = superbowls['away_q1'] + superbowls['away_q2'] + superbowls['away_q3']
superbowls['away_endq4'] = superbowls['away_q1'] + superbowls['away_q2'] + superbowls['away_q3'] + superbowls['away_q4']

# %%
superbowls.head()

# %%
# I need to take the individual events and transform them
# count occurrences of each combination of home and away q4 scores
#change into a longform 
#      home/away        0     1       2       3       4
#        3              7     2       3
#       7               0     0       4

# Setting our two variables that together will define a unique occurrence. Only games with matching results will count as an occurrence
g = superbowls.groupby(['home_endq1', 'away_endq1'])

# %%
# get number of unique combinations of home and away for each boxscore URI - mostly a dedup for lazy data cleaning
q4_score_count = g.boxscore.nunique()

# %%
q4_score_count.head()

# %%
# Create a pivot table with Q1 scores. Define the values (unique entries) as the boxscore URIs
score_count = q1_score_count.reset_index().pivot(index='home_q1', columns='away_q1', values='boxscore')


# %%
# We need 0s instead of nulls where there weren't any occurrences
score_count.fillna(0, inplace=True)
score_count.describe()

# %%
# Reindexing the score_count so that it has a defined range on each axis, as an integer, and doesn't make jumps where we have a gap.
score_count = score_count.reindex(range(0,14), axis=0, fill_value=0).astype(int)
score_count = score_count.reindex(range(0,14), axis=1, fill_value=0).astype(int)




# %%

sns.heatmap(score_count, linewidths = 1, linecolor = "gray", cmap="Blues", annot=True)


# %%


# %%


# %%


# %%

for i in squares_df['home_scores']:
    print(i)
    if 10<= i <=19:
        squares_df.loc[i, 'home_scores'] -= 10
    elif 20<= i <=29:
        squares_df.loc[i, 'home_scores'] -= 20
    elif 30<= i <=39:
        squares_df.loc[i, 'home_scores'] -= 30
    elif 40<= i <= 49:
        squares_df.loc[i, 'home_scores'] -= 40
    elif 50<= i <=59:
        squares_df.loc[i, 'home_scores'] -= 50
    elif 0<= i <= 9:
        pass
    else: 
        print('error')

    

# %%
import seaborn as sns
import matplotlib.pyplot as plt

# %%
plt.figure(figsize=(10,6))
plt.style.use('ggplot')
superbowls['total_q4'] = superbowls['away_q4'] + superbowls['home_q4']
superbowls['total_q3'] = superbowls['away_q3'] + superbowls['home_q3']
superbowls['total_q2'] = superbowls['away_q2'] + superbowls['home_q2']
superbowls['total_q1'] = superbowls['away_q1'] + superbowls['home_q1']

sns.histplot(superbowls, x='total_q1', binwidth=1, stat='percent', cumulative=True)


# %%



