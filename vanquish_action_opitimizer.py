import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy
import math

path = 'C://Users//ashkan.zarnani//Documents//EPE//Vanquish'

file_collision = 'collisions_v1.1.csv'
file_action = 'actions.csv'

# df_action = pd.read_csv(os.path.join(path, file_action))
df_collision = pd.read_csv(os.path.join(path, file_collision))

budget = 1000

df_action = pd.DataFrame({'action_id': [1, 2, 3],
                          'title': ['A', 'B', 'C'],
                          'cost': [200, 300, 1000],
                          'ratio_senior_day': [0.1, 0.2, 0.4],
                          'ratio_senior_night': [0.2, 0.3, 0.1],
                          'ratio_child_day': [0.5, 0.1, 0.1],
                          'ratio_child_night': [0.1, 0.1, 0.3]})

# df_collision = pd.DataFrame({'location_id': [10, 20, 30, 40],
#                              'latitude': [1, 2, 3, 4],
#                              'longitude': [1, 1, 1, 1],
#                              'count_senior_day': [5, 10, 0, 0],
#                              'count_senior_night': [0, 10, 1, 0],
#                              'count_child_day': [5, 50, 0, 0],
#                              'count_child_night': [7, 7, 1, 1]})
col_key = 'key'
df_action['key'] = 1
df_collision['key'] = 1
col_is_recommended = 'is_recommended'

df_action_location = df_action.merge(df_collision, on=col_key)
df_action_location[col_is_recommended] = 0
budget_remaining = budget


def calculate_gain(row):
    return row['ratio_senior_day']*row['count_senior_day']+\
           row['ratio_senior_night']*row['count_senior_night']+ \
           row['ratio_child_day'] * row['count_child_day']+\
           row['count_child_night']*row['count_child_night']

col_cost = 'cost'
col_gain = 'gain'
col_index = 'index'
df_action_location[col_gain] = df_action_location.apply(calculate_gain, axis=1)
df_action_location.sort_values(by=col_gain, ascending=False, inplace=True)
df_action_location = df_action_location.reset_index(drop=True)

print('all possible action-location combinations #count=' + str(len(df_action_location)))

while budget_remaining > 0:
    print('-'*10)
    print('budget remaining = '+str(budget_remaining))
    df_candidates = df_action_location[df_action_location[col_cost] <= budget_remaining]
    df_candidates = df_candidates[df_candidates[col_is_recommended] == 0]
    print('possible actions #count='+str(len(df_candidates)))
    if len(df_candidates) == 0:
        print('no possible actions available - exiting process')
    df_candidates.sort_values(by=col_gain, ascending=False, inplace=True)
    recommendation = df_candidates.iloc[0]
    index_picked = recommendation.name
    df_action_location.at[index_picked, col_is_recommended] = 1
    # todo: update collision counts after expected ratios are applied
    df_action_location.at[index_picked, col_is_recommended] = 1
    print('action # '+str(recommendation['action_id'])+' for location # '+str(recommendation['location_id']))

    budget_remaining = budget_remaining-recommendation[col_cost]

print('left over budget='+str(budget_remaining))
df_recommendation = df_action_location[df_action_location[col_is_recommended]==1]
print('total gain='+str(df_recommendation[col_gain].sum()))

df_recommendation[['location_id', 'action_id', col_cost, col_gain]]
df_recommendation.to_csv(os.path.join(path, 'recommendation.csv'))