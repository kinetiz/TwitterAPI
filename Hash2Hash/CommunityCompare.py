# Description: Generate file format: |h1,h2,count| for visualisation in Gelphi
# Input: json file
# Output: csv file |h1,h2,count|
######
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
# setup logging
logging.basicConfig(filename='community_compare.log',level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

def load_object(filename):
    with open(filename, 'rb') as input:
        obj = pickle.load(input)
    return obj

def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

## Code here
file_small = 'community_compare\\4000.csv'
file_big = 'community_compare\\10000.csv'
df_small = pd.read_csv(file_small, encoding='utf-8')
df_big = pd.read_csv(file_big, encoding='utf-8')

# get all modules exists in big data set
big_modules = set(df_big['modularity_class'])
df_prop = pd.DataFrame(columns=list(big_modules))

small_modules = set(df_small['modularity_class'])
for sm in small_modules:
    # get nodes in community
    small_community = df_small.loc[df_small['modularity_class'] == sm]['Id']

    # prepare array to count proportion of community of small in big set
    count_node_prop = [0 for i in range(len(big_modules))]

    for node in small_community:
        # check which module this node belong to
        for bm in big_modules:
            if node in df_big.loc[df_big['modularity_class'] == bm]['Id'].values:
                count_node_prop[bm] +=1
                break #break if found module that contain this node

    df_prop = pd.concat([df_prop, pd.DataFrame([count_node_prop])], ignore_index=True)


df_prop.to_csv('community_compare\\top4000in10000.csv', encoding='utf-8', index=True)
