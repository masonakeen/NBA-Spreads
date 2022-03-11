# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sportsipy.nfl import *

# %%
squares_df = pd.read_csv('../data/superbowlsquares_final.csv')

# %%
squares_df.head()

#create another df called cumul_squares to do a valuations on all occurrences

# %%
# %%
# I need to take the individual events and transform them
# count occurrences of each combination of home and away q4 scores
#change into a longform 
#      home/away        0     1       2       3       4
#        3              7     2       3
#       7               0     0       4

# Setting our two variables that together will define a unique occurrence. Only games with matching results will count as an occurrence
g_q1 = squares_df.groupby(['home_endq1', 'away_endq1'])
g_q2 = squares_df.groupby(['home_endq2', 'away_endq2'])
g_q3 = squares_df.groupby(['home_endq3', 'away_endq3'])
g_q4 = squares_df.groupby(['home_endq4', 'away_endq4'])

# get number of unique combinations of home and away for each boxscore URI - mostly a dedup for lazy data cleaning
q1_score_count = g_q1.boxscore.nunique()
q2_score_count = g_q2.boxscore.nunique()
q3_score_count = g_q3.boxscore.nunique()
q4_score_count = g_q4.boxscore.nunique()




# %%
# Create a pivot table with Q1-Q4 scores. Define the values (unique entries) as the boxscore URIs
q1_score_count = q1_score_count.reset_index().pivot(index='home_endq1', columns='away_endq1', values='boxscore')
q2_score_count = q2_score_count.reset_index().pivot(index='home_endq2', columns='away_endq2', values='boxscore')
q3_score_count = q3_score_count.reset_index().pivot(index='home_endq3', columns='away_endq3', values='boxscore')
q4_score_count = q4_score_count.reset_index().pivot(index='home_endq4', columns='away_endq4', values='boxscore')


# %%

# We need 0s instead of nulls where there weren't any occurrences. Repeat for all Qs
q1_score_count.fillna(0, inplace=True)
q1_score_count.describe()
q2_score_count.fillna(0, inplace=True)
q2_score_count.describe()
q3_score_count.fillna(0, inplace=True)
q3_score_count.describe()
q4_score_count.fillna(0, inplace=True)
q4_score_count.describe()

# %%

# %%
# Reindexing the score_count so that it has a defined range on each axis, as an integer, and doesn't make jumps where we have a gap.
q1_score_count = q1_score_count.reindex(range(0,10), axis=0, fill_value=0).astype(int)
q1_score_count = q1_score_count.reindex(range(0,10), axis=1, fill_value=0).astype(int)
q2_score_count = q2_score_count.reindex(range(0,10), axis=0, fill_value=0).astype(int)
q2_score_count = q2_score_count.reindex(range(0,10), axis=1, fill_value=0).astype(int)
q3_score_count = q3_score_count.reindex(range(0,10), axis=0, fill_value=0).astype(int)
q3_score_count = q3_score_count.reindex(range(0,10), axis=1, fill_value=0).astype(int)
q4_score_count = q4_score_count.reindex(range(0,10), axis=0, fill_value=0).astype(int)
q4_score_count = q4_score_count.reindex(range(0,10), axis=1, fill_value=0).astype(int)


# %%


# %%
sns.set()

fig = plt.figure(figsize=(20,20))
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)
ax4 = fig.add_subplot(2, 2, 4)



sns.heatmap(q1_score_count, ax=ax1, linewidths = 1, linecolor = "gray", cmap="YlGnBu", annot=True, vmin=0, vmax=6, square=True)
sns.heatmap(q2_score_count, ax=ax2, linewidths = 1, linecolor = "gray", cmap="YlGnBu", annot=True, vmin=0, vmax=6, square=True)
sns.heatmap(q3_score_count, ax=ax3, linewidths = 1, linecolor = "gray", cmap="YlGnBu", annot=True, vmin=0, vmax=6, square=True)
sns.heatmap(q4_score_count, ax=ax4, linewidths = 1, linecolor = "gray", cmap="YlGnBu", annot=True, vmin=0, vmax=6, square=True)


# %%
homeq1list = list(squares_df['home_endq1'])
homeq2list = list(squares_df['home_endq2'])
homeq3list = list(squares_df['home_endq3'])
homeq4list = list(squares_df['home_endq4'])
awayq1list = list(squares_df['away_endq1'])
awayq2list = list(squares_df['away_endq2'])
awayq3list = list(squares_df['away_endq3'])
awayq4list = list(squares_df['away_endq4'])

# %%
homescores = [*homeq1list, *homeq2list, *homeq3list, *homeq4list]
awayscores = [*awayq1list, *awayq2list, *awayq3list, *awayq4list]


# %%
print(homescores)

# %%
print(len(awayscores))

# %%
allscoresdict = {'homescores': homescores, 'awayscores':awayscores}

allscores_df = pd.DataFrame(allscoresdict)

# %%
allscores_df.head()

# %%
import uuid 
for i in range(0,121):
    allscores_df.loc[i, 'unique_id'] = uuid.uuid4()


allscores_df.head()

# %%
print(allscores_df)

# %%
allscores_df.dropna(axis=0, how='any', inplace=True)

allscores_df.tail()

# %%

g_allscores = allscores_df.groupby(['homescores', 'awayscores'])

allscores_count = g_allscores.unique_id.nunique()

allscores_count = allscores_count.reset_index().pivot(index='homescores', columns='awayscores', values='unique_id')





# %%
print(allscores_count)

# %%
allscores_count.fillna(0, inplace=True)
allscores_count.isnull().sum()



# %%
allscores_count = allscores_count.reindex(range(0,9), axis=0, fill_value=0).astype(int)

# %%
sns.set()

fig = plt.figure(figsize=(20,20))
ax1 = fig.add_subplot(3, 2, 1)
ax2 = fig.add_subplot(3, 2, 2)
ax3 = fig.add_subplot(3, 2, 3)
ax4 = fig.add_subplot(3, 2, 4)
ax5 = fig.add_subplot(3, 2, 5)


sns.heatmap(q1_score_count, ax=ax1, linewidths = 1, linecolor = "gray", cmap="YlGnBu", annot=True, vmin=0, vmax=6, square=True)
sns.heatmap(q2_score_count, ax=ax2, linewidths = 1, linecolor = "gray", cmap="YlGnBu", annot=True, vmin=0, vmax=6, square=True)
sns.heatmap(q3_score_count, ax=ax3, linewidths = 1, linecolor = "gray", cmap="YlGnBu", annot=True, vmin=0, vmax=6, square=True)
sns.heatmap(q4_score_count, ax=ax4, linewidths = 1, linecolor = "gray", cmap="YlGnBu", annot=True, vmin=0, vmax=6, square=True)
sns.heatmap(allscores_count, ax=ax5, linewidths = 1, linecolor = "gray", cmap="YlGnBu", annot=True, square=True)
#plt.savefig('SB_Squares_Heatmaps.png', dpi=120)

# %%
allscores_df.head()

# %%
superbowls = pd.read_csv('../data/superbowlsquares_final.csv')

# %%
superbowls.head()

# %%
q1_score_count_ev = q1_score_count
q2_score_count_ev = q2_score_count
q3_score_count_ev = q3_score_count
q4_score_count_ev = q4_score_count

# %%
q1_score_count_ev = q1_score_count.multiply(50/28)
q2_score_count_ev = q2_score_count.multiply(100/28)
q3_score_count_ev = q3_score_count.multiply(50/28)
q4_score_count_ev = q4_score_count.multiply(200/28)

# %%
q1_score_count_ev.head()

# %%
sns.set()

fig = plt.figure(figsize=(20,20))
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)
ax4 = fig.add_subplot(2, 2, 4)
#ax5 = fig.add_subplot(3, 2, 5)


sns.heatmap(q1_score_count_ev, ax=ax1, linewidths = 1, linecolor = "gray", cmap="YlGnBu", annot=True, vmax=16, square=True)
sns.heatmap(q2_score_count_ev, ax=ax2, linewidths = 1, linecolor = "gray", cmap="YlGnBu", annot=True, vmax=16, square=True)
sns.heatmap(q3_score_count_ev, ax=ax3, linewidths = 1, linecolor = "gray", cmap="YlGnBu", annot=True, vmax=16, square=True)
sns.heatmap(q4_score_count_ev, ax=ax4, linewidths = 1, linecolor = "gray", cmap="YlGnBu", annot=True, vmax=16, square=True)
#sns.heatmap(allscores_count, ax=ax5, linewidths = 1, linecolor = "gray", cmap="YlGnBu", annot=True, square=True)
#plt.savefig('SB_Squares_Heatmaps.png', dpi=120)

# %%
overall_ev = q1_score_count_ev + q2_score_count_ev + q3_score_count_ev + q4_score_count_ev



# %%
sns.set()

fig = plt.figure(figsize=(20,20))
ax1 = fig.add_subplot(3, 2, 1)
ax2 = fig.add_subplot(3, 2, 2)
ax3 = fig.add_subplot(3, 2, 3)
ax4 = fig.add_subplot(3, 2, 4)
ax5 = fig.add_subplot(3, 2, 5)


sns.heatmap(q1_score_count_ev, ax=ax1, linewidths = 1, linecolor = "gray", cmap="YlGnBu", annot=True, vmax=16, square=True)
sns.heatmap(q2_score_count_ev, ax=ax2, linewidths = 1, linecolor = "gray", cmap="YlGnBu", annot=True, vmax=16, square=True)
sns.heatmap(q3_score_count_ev, ax=ax3, linewidths = 1, linecolor = "gray", cmap="YlGnBu", annot=True, vmax=16, square=True)
sns.heatmap(q4_score_count_ev, ax=ax4, linewidths = 1, linecolor = "gray", cmap="YlGnBu", annot=True, vmax=16, square=True)
sns.heatmap(overall_ev, ax=ax5,  linewidths = 1, linecolor = "gray", cmap="YlGnBu", annot=True, square=True)

ax5.set_xlabel('Away Score')
ax5.set_ylabel('Home Score')

plt.savefig('SB_Squares_EV_Heatmaps.png', dpi=120)


# %%
overall_ev.values.sum()

# %%
allscores_count.values.sum()

# %%



