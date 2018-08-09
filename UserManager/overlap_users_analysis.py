import numpy as np
import csv
import networkx as nx
import pandas as pd
import logging
import pickle

logging.basicConfig(filename='overlap_users_analysis.log',level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

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

if __name__=="__preprare_filterandbasevector__":

    allusernw_withvectors=pd.DataFrame.from_csv("C:\\Users\\Auu\\Desktop\\user_network\\data\\50k_userobjsnw.csv")
    filterd_users=pd.DataFrame.from_csv("C:\\Users\\Auu\\Desktop\\user_network\\data\\filtered_users.csv", index_col=None)
    base = pd.DataFrame.from_csv("C:\\Users\\Auu\\Desktop\\user_network\\data\\base_users.csv", index_col=None)

    # find base users who do not have vectors
    aa = allusernw_withvectors.uid.values.tolist()
    notfound_vector = []
    for i in base.uid.values:
        if i not in aa:
            notfound_vector.append(i)
    print(notfound_vector) #6 users

    # find base users who do not in filtered_users list
    aa = filterd_users.uid.values.tolist()
    notfound = []
    for i in base.uid.values:
        if i not in aa:
            notfound.append(i)

    # get vectors of these base users
    base_not_in_filtered = pd.DataFrame()
    for i in notfound:
        base_not_in_filtered = base_not_in_filtered.append(allusernw_withvectors[allusernw_withvectors.uid == i])

    # concat with the filtered_users, so we'll get the full filtered_users vectors (base+filtered)
    df_filterd_users_and_base_objs = filterd_users.append(base_not_in_filtered)
    df_out = df_filterd_users_and_base_objs[['uid','bitcoin','ethereum','ripple','bitcoincash','eosio','litecoin','cardano','stellar','iota','tron','neo','monero','dash','nem','tether','vechain','ethereumclassic','bytecoin','binancecoin','qtum','zcash','icx','omisego','lisk','zilliqa','bitcoingold','aeternity','ontology','verge','steem','1_crypto_market_news','2_crypto_buzz_ads', '3_general', '4_bussiness_tech', '5_money_trading','others']]
    df_out.to_csv('filterd_users_and_base_users_with_vectors.csv',index=None)

if __name__=="cal_vectors_correlation":
    df_filterd_users_and_base_objs = pd.DataFrame.from_csv("C:\\Users\\Auu\\Desktop\\user_network\\data\\filterd_users_and_base_users_with_vectors.csv")
    pearson = df_filterd_users_and_base_objs.corr('pearson')
    spearman = df_filterd_users_and_base_objs.corr('spearman')
    kendall = df_filterd_users_and_base_objs.corr('kendall')
    pearson.to_csv('uservector_corr//corr_pearson.csv')
    spearman.to_csv('uservector_corr//corr_spearman.csv')
    kendall.to_csv('uservector_corr//corr_kendall.csv')

    # gen for Tableau in |src-target-corr| format
    srclst, tarlst, corrlst = [],[],[]
    for i in pearson.columns:
        for tar, corr in pearson[i].iteritems():
            srclst.append(i)
            tarlst.append(tar)
            corrlst.append(corr)

    pd.DataFrame({'var1':srclst,'var2':tarlst,'corr_pearson':corrlst}).to_csv("uservector_corr//tab_corr_pearson.csv",index=None)

    # Spearman: gen for Tableau in |src-target-corr| format
    srclst, tarlst, corrlst = [],[],[]
    for i in spearman.columns:
        for tar, corr in spearman[i].iteritems():
            srclst.append(i)
            tarlst.append(tar)
            corrlst.append(corr)

    pd.DataFrame({'var1':srclst,'var2':tarlst,'corr_spearman':corrlst}).to_csv("uservector_corr//tab_corr_spearman.csv",index=None)

    # Kendall: gen for Tableau in |src-target-corr| format
    srclst, tarlst, corrlst = [],[],[]
    for i in kendall.columns:
        for tar, corr in kendall[i].iteritems():
            srclst.append(i)
            tarlst.append(tar)
            corrlst.append(corr)

    pd.DataFrame({'var1':srclst,'var2':tarlst,'corr_kendall':corrlst}).to_csv("uservector_corr//tab_corr_kendall.csv",index=None)

