import logging
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np
import operator
# setup logging
logging.basicConfig(filename='user_manager.log',level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")


def load_object(filename):
    with open(filename, 'rb') as input:
        obj = pickle.load(input)
    return obj

def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

# excluded_users = load_object("user//excluded_users.pkl")
# user_postcount_noRT = load_object("user//user_postcount_no-RT.pkl")
# len(user_postcount_noRT) - len(excluded_users)
#
# included_users = {}
# for user, count in user_postcount_noRT.items():
#     if user not in excluded_users:
#         included_users[user] = count
#
# save_object(included_users,"user//included_users.pkl")
# included_users = load_object("user//included_users.pkl")
# sort = sorted(included_users.items(),key=operator.itemgetter(1), reverse=True)
# df_included_users = pd.DataFrame(list(sort), columns=['uid', 'num_twt'])
# df_included_users.to_csv("user//df_included_users.csv")

df_included_users = pd.DataFrame.from_csv("user//df_included_users.csv")

top = 1000
top_rows = df_included_users.loc[0:top-1]
lower_top_rows = df_included_users.loc[top:df_included_users.shape[0]-1]
max = np.max(df_included_users['num_twt'])
# log log scale
fig = plt.figure(); ax = fig.add_subplot(1, 1, 1)
h = ax.hist(lower_top_rows.num_twt.values,bins=np.logspace(np.log10(0.1),np.log10(max), 100), log = True,cumulative=False, color='grey',alpha=0.5)
ax.set_xscale('log')
h = ax.hist(top_rows.num_twt.values,bins=np.logspace(np.log10(0.1),np.log10(max), 100), log = True,cumulative=False, color='green', alpha=1)
# # log y scale
# h = ax.hist(df_included_users['num_twt'],bins=100, log = True,cumulative=False,normed=True)
plt.vlines(lower_top_rows.num_twt.values[0]-1,0 ,df_included_users.shape[0], 'r','dashed')
plt.xlabel('Num. tweets')
plt.ylabel('Frequency')
plt.title('Distribution of User Tweet')

#
# # no scale
# fig = plt.figure(); ax = fig.add_subplot(1, 1, 1)
# h = ax.hist(df_included_users.num_twt.values,bins=100, log = True,cumulative=False, color='green')
# # # log y scale
# # h = ax.hist(df_included_users['num_twt'],bins=100, log = True,cumulative=False,normed=True)
# plt.vlines(lower_top_rows.num_twt.values[0]-1,0 ,max, 'r','dashed')
# plt.xlabel('Log num. tweets of each user)')
# plt.ylabel('Log Frequency')
# plt.title('Distribution of User tweets')