from sklearn.preprocessing import MinMaxScaler
import copy
import pandas as pd
import json
import os
import logging
import datetime
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import operator
import pickle

# =============== Global Config ====================================================================
logging.basicConfig(filename='generate_user_network.log',level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

# =============== Function ====================================================================

def load_object(filename):
    with open(filename, 'rb') as input:
        obj = pickle.load(input)
    return obj

def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def printlog(m):
    print(m)
    logging.info(m)

class UserNetwork():
    uid = ""
    friends = []
    followers = []

    def __init__(self, uid, friends=[], followers=[]):
        self.uid = uid
        self.friends = friends
        self.followers = followers


# =============== Main program ====================================================================
# if __name__ == "__main__":
df_userinfo = pd.DataFrame.from_csv("data//df_userinfo.csv")
df_user_objs = pd.DataFrame.from_csv("data//df_user_objs.csv")


included_nw_user = load_object("data//included_nw_user.pkl")
len(included_nw_user)

# load base users with all connected users
usernw = load_object("data//top1000_combined_fri-fol_users.pkl")
all_nw_user = set([user.uid for user in usernw])

#*** Get based users who have no info -> will get later
included_nw_user = set(included_nw_user)
user_objs = set(df_user_objs.uid.values)
# base_user_no_info = set(df_user_objs.uid.values).intersection(all_nw_user)
# pd.DataFrame({"uid":base_user_no_info}).to_csv('base_user_no_info.csv')
base_user_no_info = list(set(all_nw_user).difference(user_objs))
pd.DataFrame({"uid":base_user_no_info}).to_csv('base_user_no_info.csv')

# # union base users with included_users
# union = included_nw_user.union(all_nw_user)
#
#
#
# # generate node file
# df_NODE = pd.DataFrame(data={'label': list(union)})
# df_NODE.to_csv("data//unw_node.csv")

#generate edge file




# ============= Adhoc - Find missing user in df_userinfo.csv ===================
if __name__ == "__find_missing_users__":
    tenlinks = load_object("data//overlap_10_links_plus_user.pkl")
    uten = set(tenlinks.keys())
    uinfo = set(df_userinfo.uid.values)
    diff = uten.difference(uinfo)
    pd.DataFrame({"uid":list(diff)}).to_csv("missing_user_info.csv")

    len(tenlinks)
    len(df_userinfo)+len(diff)#66411