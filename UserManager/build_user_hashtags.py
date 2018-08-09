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
logging.basicConfig(filename='build_user_hashtag.log',level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

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


# =============== Main program ====================================================================
if __name__ == "__main__":

    # Prepare file path to read users
    walk_dir = "G:\\work\\data\\user_nw\\user_twt"
    file_list = []
    for root, subdirs, files in os.walk(walk_dir):
        path, book_name = os.path.split(root)
        all_text = ""
        for filename in files:
            # os.path.join => join str with //
            file_path = os.path.join(root, filename)
            file_list.append(file_path)

    # =============== Main Config =================
    included_nw_user = []
    userobj_count = 0
    user_per_file = 10000
    user_folder = 'user_objs\\'
    user_filename = "user_objs.pkl"
    file_count = 1

    # =============== Processing file =================
    user_objs = dict()
    for filename in file_list:
            # Prepare user-hashtags objects
            #     user_hashtags = {'uid':  {'hashtag': 'count'}}
        # filename = file_list[0]

        # load user_twt
        u_list = load_object(filename)

        printlog("Reading file: %s"%filename)
        # process each user
        for uid, twt_infos in u_list.items():
            printlog("Processing user: %d" % uid)

            # var to keep hashtag count
            hashtag_count_dict = dict()

            # read tweet from each user
            for tweet in twt_infos['tweets']:
                entities = tweet['entities']
                # distinct and lower hashtag
                hashtag_in_tweet = set([tag['text'].lower() for tag in entities['hashtags']])

                # count tag from all tweets of this user
                for tag in hashtag_in_tweet:
                    hashtag_count_dict[tag] = hashtag_count_dict.get(tag, 0)+1

            # assign user_objs
            included_nw_user.append(uid) # keep users in list
            user_objs[uid] = {'retweet_count': twt_infos['retweet_count'],
                              'hashtag_count': hashtag_count_dict,
                              'tweet_count': len(twt_infos['tweets'])}
            userobj_count+=1

            printlog("Assigned user: %d" % uid)

            # save in file every 10,000 users to clear memory
            if userobj_count >= user_per_file:
                save_object(user_objs, user_folder+'%s_%s'%(file_count,user_filename))
                printlog("Save user: %s" % user_folder+'%s_%s'%(file_count,user_filename))

                # update vars
                file_count += 1
                userobj_count=0
                user_objs = dict()

    # save the last processing user_objs
    save_object(user_objs, user_folder+'%s_%s' % (file_count, user_filename))
    save_object(included_nw_user, user_folder+'included_nw_user.pkl')
    print(len(user_objs))
# =============== End main program ====================================================================

