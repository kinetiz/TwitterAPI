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
logging.basicConfig(filename='create_user_vector.log', level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")


# =============== Function ====================================================================

class UserNetwork():
    uid = ""
    friends = []
    followers = []

    def __init__(self, uid, friends=[], followers=[]):
        self.uid = uid
        self.friends = friends
        self.followers = followers

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


# =============== Main program ====================================================================
if __name__ == "__main__":

    # =============== Main Config =================
    save_folder = 'user_objs_score//'

    # =============== Coin hashtag config =================
    coin_tag_list = pd.DataFrame.from_csv("C:\\Users\\Auu\\Desktop\\community_compare\\main\\uservector_hashtag_list.csv", header=0, index_col=None)
    dict_cointag_set = dict()

    print(coin_tag_list.shape)
    print(coin_tag_list.columns)
    for coin in coin_tag_list.columns:
        dict_cointag_set[coin] = set(coin_tag_list[coin].dropna())

    # =============== Processing file =================

    file_list = ["user_objs//1_user_objs.pkl",
                 "user_objs//2_user_objs.pkl",
                 "user_objs//3_user_objs.pkl",
                 "user_objs//4_user_objs.pkl",
                 "user_objs//5_user_objs.pkl",
                 "user_objs//6_user_objs.pkl"]

    # Process user_objs file
    for filename in file_list:
        # #* test
        # filename = file_list[0]

        user_objs = load_object(filename)

        for uid, info in user_objs.items():
            # #* test
            # uid = 984047889159737344
            # info = user_objs[uid]

            printlog("Processing user: %d" % uid)

            # prepare user vectors
            interest_scores = dict()

            # get total hashtag to calculate user vector
            total_hashtag_used = sum(info['hashtag_count'].values())
            if total_hashtag_used == 0: total_hashtag_used = 1

            # calculate user vector
            user_hashtag_set = set(info['hashtag_count'].keys())
            for coin_name, coin_tag_set in dict_cointag_set.items():
                # find overlap coin hashtag in user's
                overlap_hashtag = user_hashtag_set.intersection(coin_tag_set)

                # count coin hashtag (from overlap)
                user_coin_tag_count = 0
                for ht in overlap_hashtag:
                    user_coin_tag_count += info['hashtag_count'][ht]

                # calculate interest score of this user to this coin: score = num_coin# / num_total#
                interest_scores[coin_name] = dict()
                interest_scores[coin_name]['prob'] = user_coin_tag_count / total_hashtag_used
                interest_scores[coin_name]['count'] = user_coin_tag_count

            # add score to user_objs
            user_objs[uid]['total_hashtag'] = total_hashtag_used
            user_objs[uid]['scores'] = interest_scores
            printlog("Done calculation user: %d" % uid)
        # save updated user_objs
        save_filename = save_folder + filename.rsplit("//")[-1].rstrip(".pkl") + "_score.pkl"
        save_object(user_objs, save_filename)
        printlog("Save: %s" % save_filename)

    printlog("Done processing file: %s" % filename)

printlog("Done processing all files..")
# =============== End main program ====================================================================


