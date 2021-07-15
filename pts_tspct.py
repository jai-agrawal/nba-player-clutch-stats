import pandas as pd
from nba_api.stats.endpoints.leaguedashplayerclutch import LeagueDashPlayerClutch
from matplotlib import pyplot as plt

# True-Shooting Percentage and Points

def distance(a,b):
    return (a*2 + b*2) ** 1/2

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
# df_main.to_csv('main.csv')
# total mins and filter
df_main['totalMins'] = df_main['MIN_x'] * df_main['GP_x']
df_main = df_main.loc[(df_main['totalMins'] > 50) | (df_main['GP_x'] > 10)]
df2 = df_main[['PLAYER_NAME_x', 'PTS', 'TS_PCT']]

df2['DISTANCE'] = df2.apply(lambda x: distance(x['PTS'], x['TS_PCT']), axis=1)
df2.sort_values(ascending=False,by='DISTANCE',inplace=True)
df2 = df2.head(10)
df2 = df2.reset_index()
df2.to_csv('pts_tspct.csv')
plt.scatter(df2['PTS'], df2['TS_PCT'])


for i in range(len(df2)):
    plt.text(df2['PTS'][i], df2['TS_PCT'][i], df2['PLAYER_NAME_x'][i])
plt.xlabel("PTS")
plt.ylabel("TS(%)")
plt.show()