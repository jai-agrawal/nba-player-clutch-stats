from nba_api.stats.endpoints.leaguedashplayerclutch import LeagueDashPlayerClutch

# Defensive Rating

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
df['totalMins'] = df['MIN'] * df['GP']
df = df.loc[(df['totalMins'] > 50) | (df['GP'] > 10)]
df.sort_values(ascending=False,by='DEF_RATING',inplace=True)
df = df.reset_index()
df = df[['PLAYER_NAME', 'DEF_RATING']]
df.to_csv('defrating.csv',index=False)