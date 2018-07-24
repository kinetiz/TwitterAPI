

### count user from json
#Get json file path
import json
import os
import pickle
import operator
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def load_object(filename):
    with open(filename, 'rb') as input:
        obj = pickle.load(input)
    return obj

def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

df = pd.read_csv('gephi_upper-mean_normalised_cotag.csv')
noneng_list = []
# df_eng = pd.DataFrame(columns=['source','target','weight'])
for index, row in df.iterrows():
    # list row that is non-eng
    if not isEnglish(row[0]) or not isEnglish(row[1]):
        noneng_list.append(index)

# drop non-eng row
df_eng = df.drop(noneng_list)




################3

############################################################################################
# Build probability matrix of hashtag - to normalise co-occurrence network
############################################################################################
set_name = 'mean'
included_hashtags = load_object('G:\\work\\TwitterAPI\\Hash2Hash\\20180513-0626\\%s_included_hashtags.pkl'% set_name)
dict_co_hashtag = load_object('G:\\work\\TwitterAPI\\Hash2Hash\\20180513-0626\\%s_dict_co_hashtag.pkl' % set_name)

## remove non-eng
df_tag = pd.DataFrame.from_dict(included_hashtags,orient='index')
noneng_list=[]
for index, row in df_tag.iterrows():
    # list row that is non-eng
    if not isEnglish(index):
        noneng_list.append(index)

# drop non-eng row
df_eng = df_tag.drop(noneng_list)
included_hashtags_eng = pd.DataFrame.to_dict(df_eng)[0]
save_object(included_hashtags_eng, 'G:\\work\\TwitterAPI\\Hash2Hash\\20180513-0626\\%s_included_hashtags_eng.pkl'% set_name)

##
d = {'a': [], 'b': [], 'p(a)': [], 'p(b)': [], 'p(a)p(b)': [], 'p(a,b)': [], 'p(a,b)-p(a)p(b)': []}
df_cotag = pd.DataFrame(data=d)
total_tag = np.sum(list(included_hashtags_eng.values()))

for a, b_list in dict_co_hashtag.items():

    # process only eng hashtag
    if isEnglish(a):
        # prepare list to assign data
        a_list, b_list_eng, prob_a_list, prob_b_list, prob_a_prob_b_list, prob_ab_list, norm_weight_list = [],[], [], [], [], [], []

        # print(1)
        prob_a = included_hashtags_eng[a] / total_tag
        for b, count in b_list.items():
            # process only eng hashtag
            if isEnglish(b):
                prob_b = included_hashtags_eng[b] / total_tag
                # print(2)
                prob_a_prob_b = prob_a * prob_b
                prob_ab = count / total_tag
                a_list.append(a)
                b_list_eng.append(b)
                prob_a_list.append(prob_a)
                prob_b_list.append(prob_b)
                prob_a_prob_b_list.append(prob_a_prob_b)
                prob_ab_list.append(prob_ab)
                # normalise weight by p(a,b) - p(a)p(b) means minus by prob that happen by chance
                norm_weight_list.append(prob_ab - prob_a_prob_b)
                # print(3)
        df = pd.DataFrame(
            {'a': a_list, 'b': list(b_list_eng), 'p(a)': prob_a_list, 'p(b)': prob_b_list,
             'p(a)p(b)': prob_a_prob_b_list, 'p(a,b)': prob_ab_list, 'p(a,b)-p(a)p(b)': norm_weight_list})

        # concat to the main df
        df_cotag = pd.concat([df_cotag, df])

# Keep only P(a,b) > P(a)P(b). Thus, not co-occur by chance
df_normalised_cotag = df_cotag.loc[df_cotag['p(a,b)'] > df_cotag['p(a)p(b)']]
df_exclued_cotag = df_cotag.loc[df_cotag['p(a,b)'] <= df_cotag['p(a)p(b)']]

df_cotag.to_csv('%s_full_cotag_eng.csv' % set_name, encoding='utf-8', index=False)
df_normalised_cotag.to_csv('%s_normalised_cotag_eng.csv' % set_name, encoding='utf-8', index=False)
df_exclued_cotag.to_csv('%s_excluded_cotag_eng.csv' % set_name, encoding='utf-8', index=False)

# write file for Gephi
df_gephi = df_normalised_cotag[['a', 'b', 'p(a,b)-p(a)p(b)']]
df_gephi.columns = ['source', 'target', 'weight']
scaler = MinMaxScaler(feature_range=(1, 10))
scaler.fit(df_gephi[['weight']])
df_gephi.loc[:, 'weight'] = scaler.transform(df_gephi[['weight']])
df_gephi.to_csv('gephi_%s_normalised_cotag_eng.csv' % set_name, encoding='utf-8', index=False)

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + 'Done ' + set_name)