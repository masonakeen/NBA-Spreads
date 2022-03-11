# %%
import pandas as pd
import numpy as np
import seaborn as sns

from sportsipy.ncaab import boxscore

# %%
trimmed_df = pd.read_csv('../data/2019_ncaa_season_boxscores_trimmed.csv')
extended_df = pd.read_csv('../data/2019_ncaa_season_boxscores.csv')
trimmed_df.head()

# %%
extended_df.drop(extended_df.columns.difference(['Unnamed: 0.1','winner']), 1, inplace=True)
extended_df.head()


# %%
len(extended_df)

# %%
trimmed_df.drop(columns=['Unnamed: 0'], index=0, inplace=True)

# %%
trimmed_df['boxscore'] = pd.Series(trimmed_df['Unnamed: 0.1'], dtype="string").tolist()


# %%
trimmed_df.set_index('boxscore')
trimmed_df.drop(['Unnamed: 0.1'], axis=1, inplace=True)

# %%
trimmed_df.set_index('boxscore')
backup_trimmed = trimmed_df

# %%

trimmed_df = trimmed_df.merge(extended_df, left_on='boxscore', right_on='Unnamed: 0.1')


# %%
trimmed_df.drop_duplicates(inplace=True)

# %%
for i in trimmed_df:
    if (trimmed_df['winner'] == 'Home').any():
        trimmed_df['home_team'] = trimmed_df['winning_abbr']
        trimmed_df['away_team'] = trimmed_df['losing_abbr']
    elif (trimmed_df['winner'] == 'Away').any():
        trimmed_df['away_team'] = trimmed_df['winning_abbr']
        trimmed_df['home_team'] = trimmed_df['losing_abbr']
    else:
        print('error')


    
        

# %%
#trimmed_df.to_csv('../data/2019_ncaa_season_boxscores_trimmed.csv')
trimmed_df.head()
trimmed_df = pd.get_dummies(data=trimmed_df, columns = ['winner'], drop_first=True)

# %%
import matplotlib.pyplot as plt
#sns.set()
#fig = plt.figure(figsize=(16,16))
#sns.heatmap(trimmed_df.corr(), annot=True, cmap = "YlGnBu", center = 0)

# %%



