# NBA-Spreads
Project with the goal of identifying high-confidence Moneyline predictions and disparities between Vegas spreads and projections


Columns dropped for trimmed boxscore csv: ncaa_boxscore_df.drop(columns=['away_block_percentage', 'away_field_goal_percentage', 'away_defensive_rebounds', 'away_field_goals', 'away_free_throw_attempts', 'away_free_throw_percentage', 'home_win_percentage'], inplace=True)

ncaa_boxscore_df.drop(columns=['away_free_throws', 'away_minutes_played', 'away_offensive_rebounds', 'home_two_point_field_goals'], inplace=True)

ncaa_boxscore_df.drop(columns= ['away_offensive_rebound_percentage', 'away_personal_fouls', 'away_points', 'away_ranking', 'home_two_point_field_goal_percentage'], inplace=True)

ncaa_boxscore_df.drop(columns = ['away_three_point_field_goal_attempts', 'away_steals', 'away_steal_percentage', 'away_wins', 'away_losses', 'away_two_point_field_goal_percentage', 'away_two_point_field_goals', 'home_assist_percentage', 'home_assists', 'home_block_percentage', 'home_blocks', 'home_defensive_rebound_percentage', 'home_defensive_rebounds', 'home_field_goal_attempts', 'home_field_goal_percentage', 'home_field_goals', 'home_free_throw_attempts', 'home_free_throws', 'home_losses', 'home_minutes_played', 'home_offensive_rebound_percentage', 'home_offensive_rebounds', 'home_personal_fouls', 'home_ranking', 'home_steal_percentage', 'home_steals', 'home_three_point_attempt_rate', 'home_three_point_field_goal_attempts', 'home_three_point_field_goals', 'home_total_rebounds', 'home_turnovers', 'home_two_point_field_goal_attempts'], inplace=True)

ncaa_boxscore_df.drop(columns= ['away_three_point_attempt_rate', 'away_three_point_field_goals', 'away_total_rebounds', 'home_points', 'away_three_point_field_goals', 'away_total_rebounds', 'away_turnovers', 'away_two_point_field_goal_attempts'], inplace=True)


# get home win percentage back (requires home losses and home wins)
# get away free throw percentage
# maybe get home and away points back
# home 3pt attempt rate
# 

# Set counter to watch progress
cnt = 0
# Loop through all teams in database (353 teams)
for team in Teams("2019"):
    cnt += 1
    # 3 Teams caused an error so do try/except so the loop doesnt stop
    try:
        print(cnt)
# Returns a Pandas DataFrame of all metrics for all game Boxscores for a season
        df = team.schedule.dataframe_extended
        
        # add team name to dataframe
        df['team_name'] = team.name
        
        
        # add conference name to dataframe
        df['conf'] = team.conference
                
        # send to csv
        df.to_csv(f'./NCAA_Team_Boxscores/2019-2020/{cnt}_{team.name}_season_boxscores_2019.csv')
    except:
        print(cnt,'did not work')


Missing from 2019-2020v2: (39, 55, 58, 61, 67, 69, 84, 85, 95, 104, 107, 123, 124, 126, 127, 128, 179, 180, 182, 183, 207, 214, 215, 216, 218, 229, 230, 231, 232, 234, 235, 236, 257, 272, 290, 291, 292, 293, 298, 307, 309, 342, 346)