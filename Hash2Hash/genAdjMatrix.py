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
# # setup logging
# logging.basicConfig(filename='spam_detection.log',level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

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
filename = "C:\\Users\\Auu\\Desktop\\community compare\\scale1-10\\merged\\edge.csv"

df_edge = pd.read_csv(filename, encoding='utf-8')
nodes = set(df_edge['Source'].values)
df_adj = pd.DataFrame(columns=nodes)
index_name = dict()
for idx, n in enumerate(nodes):
    index_name[idx] = n
    adj1 = df_edge[df_edge['Source']==n][['Target','Weight']]
    adj1.columns=['node','weight']
    adj2 = df_edge[df_edge['Target'] == n][['Source', 'Weight']]
    adj2.columns = ['node', 'weight']
    adj = pd.concat([adj1, adj2])
    dict_tmp = dict()
    for i, row in adj.iterrows():
        dict_tmp[row.node] = row.weight
    df_adj = df_adj.append(dict_tmp, ignore_index=True)
df_adj = df_adj.rename(index=index_name)
# sort by col and index name
df_adj = df_adj.sort_index(axis=0).sort_index(axis=1)

df_adj.to_csv('adj_matrix.csv', encoding='utf-8', index=True)
