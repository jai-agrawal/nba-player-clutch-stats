import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Combining Offensive and Defensive scores to find a total score using different methods,
# final method used was the scaled system

offensive_scores = pd.read_csv('wfg_pts.csv')
defensive_scores = pd.read_csv('defrating.csv')

# SCALED SYSTEM
all_scores = pd.merge(offensive_scores, defensive_scores, how='outer', on='PLAYER_NAME')
scaler = MinMaxScaler()
all_scores['ScaledWFGxPTS'] = scaler.fit_transform(all_scores[['WFG x PTS']])
all_scores['ScaledDefRating'] = scaler.fit_transform(all_scores[['DEF_RATING']])
all_scores['TotalRating'] = (all_scores['ScaledWFGxPTS'] * (2/3)) + (all_scores['ScaledDefRating'] * (1/3))
all_scores.sort_values(ascending=False, by='TotalRating', inplace=True)
all_scores.to_csv('totalrating.csv')


# SCORE SYSTEM
# defensive_scores['def_score'] = defensive_scores['DEF_RATING'] / 100
# all_scores = pd.merge(offensive_scores, defensive_scores, how='outer', on='PLAYER_NAME')
# all_scores['total_score'] = all_scores['def_score'] + all_scores['WFG x PTS']
# all_scores.sort_values(ascending=False, by='total_score', inplace=True)
# print(all_scores.head(10))

# RANK SYSTEM
# defensive_scores.sort_values(ascending=False,by='DEF_RATING',inplace=True)
# offensive_scores.sort_values(ascending=False,by='WFG x PTS',inplace=True)
# defensive_ranks = list()
# offensive_ranks = list()
# for i in range(len(defensive_scores)):
#     defensive_ranks.append(i + 1)
#     offensive_ranks.append(i + 1)
# defensive_scores['defensive_rank'] = defensive_ranks
# offensive_scores['offensive_rank'] = offensive_ranks
# all_scores = pd.merge(offensive_scores, defensive_scores, how='outer', on='PLAYER_NAME')
# all_scores['overall'] = (all_scores['defensive_rank'] + all_scores['offensive_rank']) /2
# all_scores.sort_values(ascending=True, by='overall', inplace=True)
