import pandas as pd
from nba_api.stats.endpoints.leaguedashplayerclutch import LeagueDashPlayerClutch

# All Data, basic and advanced
def distance(a,b):
    return (a*2 + b*2) ** 1/2

season = '2020-21'
season_type = 'Regular Season'
clutch_time = 'Last 5 Minutes'
point_diff = 5
df = LeagueDashPlayerClutch(season_type_all_star=season_type,
                            clutch_time=clutch_time,
                            measure_type_detailed_defense='Base',
                            point_diff=point_diff,
                            per_mode_detailed='PerGame',
                            season=season
                            ).league_dash_player_clutch.get_data_frame()

df['totalMins'] = df['MIN'] * df['GP']

df = df.loc[(df['totalMins'] > 50) | (df['GP'] > 10)]
df['WFG'] = (((df['FTM'] * (1/3)) + ((df['FGM'] - df['FG3M']) * (2/3)) + (df['FG3M'])) * 100) / ((df['FTA'] * (1/3)) + ((df['FGA'] - df['FG3A']) * (2/3)) + (df['FG3A']))
df_to_show = df[['PLAYER_NAME', 'WFG']]
df_to_show.sort_values(ascending=False,by='WFG',inplace=True)

df2 = LeagueDashPlayerClutch(season_type_all_star=season_type,
                            clutch_time=clutch_time,
                            measure_type_detailed_defense='Advanced',
                            point_diff=point_diff,
                            per_mode_detailed='PerGame',
                            season=season
                            ).league_dash_player_clutch.get_data_frame()

df2.sort_values(ascending=False, by='TS_PCT',inplace=True)
df2 = df2.loc[(df['totalMins'] > 50) | (df2['GP'] > 10)]

df_main = pd.merge(df, df2, how='outer', on='PLAYER_ID')
df_main.to_csv('main.csv')
