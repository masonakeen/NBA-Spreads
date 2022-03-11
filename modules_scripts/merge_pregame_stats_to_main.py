

for i in merged_df['boxscore']:
    uri = merged_df['boxscore']

    # get the team name that we're retrieving stats for. You don't need the abbreviation - could remove later
    team_name = merged_df.at[i, 'home_team_name']
    team_abbrev = merged_df['home_team']
    print(team_name)
    print(team_abbrev)
    # Pull the dataframe from the team's CSV. You'll then trim down the DF and rename it so it only reflects the home team's stats. These will 
    # join to the main dataframe and appear as home team pregame stats
    homestats_df = pd.read_csv('../data/team_csvs/2019-2020/{}_season_boxscores_2019.csv'.format(team_name))
    homestats_df.drop(homestats_df.columns.difference(['boxscore','team_name', 'pregame_eFG','pregame_rebound_percentage','pregame_eFG_allowed','pregame_win_percentage']), inplace=True)
    homestats_df.rename(columns={'pregame_eFG': 'home_pregame_eFG','pregame_rebound_percentage': 'home_pregame_rebound_percentage','pregame_eFG_allowed': 'pregame_eFG_allowed','pregame_win_percentage': 'pregame_win_percentage'}, inplace=True)
    # Create the special index for this DF to enable the join
    homestats_df['homeindex'] = homestats_df['boxscore'] + homestats_df['team_name']

    # Now we will merge the home team stats onto the main dataframe. Creating a concatenated index column will help make sure we don't
    # assume that the team is home for every boxscore. For instance, TCU stats won't be applied as home stats for every boxscore they played
    # in the main DF
    # Outer join will also leave unimpacted boxscore rows to be filled later
    merged_df = merged_df.merge(homestats_df, on='homeindex', how='outer')
   

# Then, you'll just join the two datafrmames, specifying the columns you want to keep from the team's dataframe

# Repeat for the away team. You'll call a 


# 