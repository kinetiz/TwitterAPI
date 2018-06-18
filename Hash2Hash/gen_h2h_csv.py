# Description: Generate file format: |h1,h2,count| for visualisation in Gelphi
# Input: json file
# Output: csv file |h1,h2,count|
######
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
def load_object(filename):
    with open(filename, 'rb') as input:
        obj = pickle.load(input)
    return obj

def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


data = {
    "tweets": [
        {
            "hashtags": [
                "bitcoin",
                "ethereum"
            ],
            "tid": 1
        },
        {
            "hashtags": [
                "bitcoin",
                "ethereum",
                "omg"
            ],
            "tid": 2
        },
        {
            "hashtags": [
                "bitcoin",
                "ethereum",
                "omg",
                "ltc"
            ],
            "tid": 3
        }
    ]
}

#######################################
### Config
#######################################
min_count_threshold = 0 # will be set below
spam_users = list(dict(load_object('excluded_user.pkl')).keys())

start = datetime.datetime.now()
print(str(start) + ' - Cleaning..')
#######################################
# 1) Clean and prepare 2 objects
#   - hashtag_count = dict of each hashtag in cleaned tweet with its count
#   - clean_tweet_hashtag = list of hashtag contained in each cleaned tweets
#######################################
clean_tweet_hashtag = []
main_hashtags = []
hashtag_count = {}

# Prepare cleaned hashtag
#Get json file path
walk_dir = "G:\\work\\TwitterAPI\\data\\cleaned_data"
file_list = []
for root, subdirs, files in os.walk(walk_dir):
    path, book_name = os.path.split(root)
    all_text = ""
    for filename in files:
        # os.path.join => join str with //
        file_path = os.path.join(root, filename)
        file_list.append(file_path)


for file_name in file_list:
    print('Loading: ' + file_name + '..')
    with open(file_name) as f:
        data = json.load(f)

    # Prepare 2 obj (cleaned hashtag in tweet and count of hashtag)
    for twt in data['tweets']:
        # 1. Keep only original tweet by exclude retweet
        # 2. Exclude Spam users
        if twt['retweet_from_uid'] is None and twt['uid'] not in spam_users:
            tag_list = []

            # change all tags to lower case
            [tag_list.append(h.lower()) for h in twt['hashtags']]

            # distinct the list to remove duplicate hashtag
            tag_list = list(set(tag_list))

            # Prepare cleaned hashtag
            clean_tweet_hashtag.append(tag_list)

            for tag in tag_list:
                # get hashtag in dict and update count. If not exists just return 0 and plus 1
                hashtag_count[tag] = hashtag_count.get(tag, 0) + 1

# save objects
save_object(hashtag_count, 'genfile_0512-0616//hashtags_count_no_rt_and_spam.pkl')
save_object(clean_tweet_hashtag,'genfile_0512-0616//clean_tweet_hashtag_no_rt_and_spam.pkl')

# # load from processed objects
# hashtag_count = load_object('genfile_0512-0616//hashtags_count_no_rt_and_spam.pkl')
# clean_tweet_hashtag = load_object('genfile_0512-0616//clean_tweet_hashtag_no_rt_and_spam.pkl')

####################################################################################
# Set Threshold of hashtag count and keep only hashtag with count higher than threshold
####################################################################################

### Set Threshold 2 options
# 1. Use mean
min_count_threshold = np.mean(list(hashtag_count.values()))

# # 2. Calculate Threshold from 10% of lowest count of hashtag in the coin list
# coins = ['bitcoin','btc','ethereum','eth','ether','ripple','xrp','bitcoincash','bch','eosio','eos','litecoin','ltc','cardano','ada','stellar','xlm','iota','miota','tron','trx','neo','monero','xmr','dash','nem','xem','tether','usdt','vechain','ven','ethereumclassic','etc','bytecoin','bcn','binancecoin','bnb','qtum','zcash','zec','icx','omisego','lisk','lsk','zilliqa','zil','bitcoingold','btg','aeternity','ae','ontology','ont','verge','xvg','steem']
# coin_hash_count = {}
# for key in coins:
#     coin_hash_count[key] = hashtag_count[key]
# coin_hash_count = sorted(coin_hash_count.items(), key=operator.itemgetter(1), reverse=True)
# coin_hash_count[len(coin_hash_count)-1]
# # set threshold to 10% of the least frequent coin count
# min_count_threshold = coin_hash_count[len(coin_hash_count)-1][1]*0.1

# Remove hashtag below threshold from each tweet
filtered_hashtag_in_twts = []
included_hashtags = list(filter(lambda x: hashtag_count[x] > min_count_threshold, hashtag_count))
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + ' - Removing hashtags below threshold..')
for idx, hset in enumerate(clean_tweet_hashtag):
    # add new list to fix problem that entry of list removed on the way making the loop skipping the next entry
    new_hset = []
    [new_hset.append(h) for h in hset if h in included_hashtags]
    filtered_hashtag_in_twts.append(new_hset)

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + 'Done Cleaning spent: ' + str(datetime.datetime.now() - start))

print("Minimum threshold: " + str(min_count_threshold))
print("Total hashtag: "+ str(len(hashtag_count)))
print("Frequent hashtag: "+ str(len(included_hashtags)))

save_object(included_hashtags,'included_hashtags.pkl')
save_object(filtered_hashtag_in_twts,'filtered_hashtag_in_twts.pkl')

# hashtag_count = load_object('genfile_0512-0616\\hashtags_count_no_rt_and_spam.pkl')
# clean_tweet_hashtag = load_object('genfile_0512-0616\\clean_tweet_hashtag_no_rt_and_spam.pkl')
# included_hashtags = list(filter(lambda x: hashtag_count[x] > 44.3, hashtag_count))

# ## test
# clean_tweet_hashtag = clean_tweet_hashtag[0:2]
# clean_tweet_hashtag = [['bitcoin','btx'],['btc','btx']]
# included_hashtags = ['bitcoin','btc']
# for idx, hset in enumerate(clean_tweet_hashtag):
#     # add new list to fix problem that entry of list removed on the way making the loop skipping the next entry
#     new_hset = []
#     [new_hset.append(h) for h in hset if h in included_hashtags]
#     clean_tweet_hashtag[idx] = new_hset
# clean_tweet_hashtag

#######################################
# 2) Find co-occurrence hashtag. Set main hashtag and process one-by-one
#   Structure: dict{ 'used_tag': dict{ 'co_tag': count } }
#   Ex. dict_used_tag{ 'bitcoin': dict_co_tag{ 'eth': 10, 'btc': 9},
#                    'eth': dict_co_tag{ 'btc': 5, 'ltc': 4} ,... }
#######################################
start = datetime.datetime.now()
print(str(start) + ' - Find cooccur..')

# Prepare list of main hashtag to find its co-occurrence hashtag
# # set main hashtags as coins hashtag
# main_hashtags = [
#       'bitcoin', 'btc'
#     , 'ethereum', 'eth', 'ether'
#     , 'ripple', 'xrp'
#     , 'bitcoincash', 'bch'
#     , 'eosio', 'eos'
#     , 'litecoin', 'ltc'
#     , 'cardano', 'ada'
#     , 'stellar', 'xlm'
#     , 'iota', 'miota'
#     , 'tron', 'trx'
#     , 'neo'
#     , 'monero', 'xmr'
#     , 'dash'
#     , 'nem', 'xem'
#     , 'tether', 'usdt'
#     , 'vechain', 'ven'
#     , 'ethereumclassic', 'etc'
#     , 'bytecoin', 'bcn'
#     , 'binancecoin', 'bnb'
#     , 'qtum'
#     , 'zcash', 'zec'
#     , 'icx'
#     , 'omisego'
#     , 'lisk', 'lsk'
#     , 'zilliqa', 'zil'
#     , 'bitcoingold', 'btg'
#     , 'aeternity', 'ae'
#     , 'ontology', 'ont'
#     , 'verge', 'xvg'
#     , 'steem']
# set main hashtags as hashtag above threshold
main_hashtags = included_hashtags

dict_co_hashtag = {}
processed_tag = []
# count co-occurrence hashtags for each main hashtag one-by-one
for main_tag in main_hashtags:
    start2 = datetime.datetime.now()

    # add processed tag to a list to avoid duplicate pairs
    processed_tag.append(main_tag)
    # iterate set of hashtag of each tweet
    dict_co_tag = {}
    for twt_tags in filtered_hashtag_in_twts:
        # Count co-tag by skipping main hashtag that already processed to avoid duplicate
        # ex. [btc-eth], [eth-btc] we don't need the latter coz its the same
        if main_tag in twt_tags:
            for co_tag in twt_tags:
                if co_tag not in processed_tag:
                    dict_co_tag[co_tag] = dict_co_tag.get(co_tag, 0) + 1

    # add co-occurrence hashtags of this main hashtag to the dict.
    dict_co_hashtag[main_tag] = dict_co_tag.copy()
    print(str(main_tag) + ": " + str(datetime.datetime.now() - start2))
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + 'Done Finding spent: ' + str(datetime.datetime.now() - start))


### 3) Generate co-occurrence hashtag file
start = datetime.datetime.now()
print(str(start) + ' - Save file..')

# prepare node file
with open('genfile_0512-0616//nodes.csv','w',newline='',encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['id','label'])
    # sort asc
    included_hashtags.sort()
    for id, name in enumerate(included_hashtags):
        w.writerow([id, name])

## prepare edge file
with open('genfile_0512-0616//edges_gt_mean.csv','w',newline='',encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['Source','Target','Weight'])
    for main_tag, co_tags in dict_co_hashtag.items():
        src_id = included_hashtags.index(main_tag)
        for tag, cooccur_count in co_tags.items():
            if cooccur_count > 40.3:
                target_id = included_hashtags.index(tag)
                w.writerow([src_id, target_id, cooccur_count])


# ########################################################
# # Analysing stats of hashtag
# ########################################################
# count = list(hashtag_count.values())
# print("Total:%f" % (len(count)))
# print("min:%f" % (np.min(count)))
# print("max:%f" % (np.max(count)))
# print("mean:%f" % (np.mean(count)))
# print("median:%f" % (np.median(count)))
# print("mode:%f" % (stats.mode(count)[0][0]))
# print("std:%f" % (np.std(count)))
#
# log_count = np.log(count)
# print("log min:%f" % (np.min(log_count)))
# print("log max:%f" % (np.max(log_count)))
# print("log mean:%f" % (np.mean(log_count)))
# print("log median:%f" % (np.median(log_count)))
# print("log mode:%f" % (stats.mode(log_count)[0][0]))
# print("log std:%f" % (np.std(log_count)))
# print("log threshold:%f" %(np.log(min_count_threshold)))
# # plot histogram
# hist_info = plt.hist(log_count, bins=50)
# plt.vlines(np.log(min_count_threshold),hist_info[0].min(),hist_info[0].max(),colors='r',label='Threshold')
# # plt.hist(count, bins=50)
# plt.xlabel('Log occurrence)')
# plt.ylabel('Frequency')
# plt.title('Hashtag frequency excluded Spam and Retweet')
##