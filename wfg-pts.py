import pandas as pd
from nba_api.stats.endpoints.leaguedashplayerclutch import LeagueDashPlayerClutch

# Calculate the Weighted Field Goal Percentage and Points - Offensive score
season = '2020-21'
season_type = 'Regular Season'
clutch_time = 'Last 5 Minutes'
point_diff = 5
df = LeagueDashPlayerClutch(season_type_all_star=season_type,
                            clutch_time=clutch_time,
                            measure_type_detailed_defense='Advanced',
                            point_diff=point_diff,
                            per_mode_detailed='PerGame',
                            season=season
                            ).league_dash_player_clutch.get_data_frame()

df2  = LeagueDashPlayerClutch(season_type_all_star=season_type,
                            clutch_time=clutch_time,
                            measure_type_detailed_defense='Base',
                            point_diff=point_diff,
                            per_mode_detailed='PerGame',
                            season=season
                            ).league_dash_player_clutch.get_data_frame()

df_main = pd.merge(df, df2, how='outer', on='PLAYER_ID')
# total mins and filter
df_main['totalMins'] = df_main['MIN_x'] * df_main['GP_x']
df_main = df_main.loc[(df_main['totalMins'] > 50) | (df_main['GP_x'] > 10)]

df_main['numerator'] = (df_main['FTM'] * (1/3)) + (df_main['FGM_y'] - df_main['FG3M'] * (2/3)) + df_main['FG3M']
df_main['denominator'] = (df_main['FTA'] * (1/3)) + (df_main['FGA_y'] - df_main['FG3A'] * (2/3)) + df_main['FG3A']
df_main['WFG'] = df_main['numerator']/df_main['denominator']

df_main['WFG x PTS'] = df_main['WFG'] * df_main['PTS']
df_main.sort_values(ascending=False,by='WFG x PTS',inplace=True)
df_main = df_main[['PLAYER_NAME_x', 'WFG', 'WFG x PTS']]
df_main.columns = ['PLAYER_NAME', 'WFG', 'WFG x PTS']
df_main.to_csv('wfg_pts.csv', index=False)
