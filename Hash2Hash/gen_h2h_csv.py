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


# data = {
#     "tweets": [
#         {
#             "hashtags": [
#                 "bitcoin",
#                 "ethereum"
#             ],
#             "tid": 1
#         },
#         {
#             "hashtags": [
#                 "bitcoin",
#                 "ethereum",
#                 "omg"
#             ],
#             "tid": 2
#         },
#         {
#             "hashtags": [
#                 "bitcoin",
#                 "ethereum",
#                 "omg",
#                 "ltc"
#             ],
#             "tid": 3
#         }
#     ]
# }
#
# #######################################
# ### Config
# #######################################
# min_count_threshold = 0 # will be set below
# # spam_users = list(dict(load_object('excluded_user.pkl')).keys())
# spam_users = load_object('bot-from-bot_score.pkl')
# spam_users = list(spam_users.uid.values)
#
# start = datetime.datetime.now()
# print(str(start) + ' - Cleaning..')
# #######################################
# # 1) Clean and prepare 2 objects
# #   - hashtag_count = dict of each hashtag in cleaned tweet with its count
# #   - clean_tweet_hashtag = list of hashtag contained in each cleaned tweets
# #######################################
# clean_tweet_hashtag = []
# main_hashtags = []
# hashtag_count = {}
#
# # Prepare cleaned hashtag
# #Get json file path
# walk_dir = "G:\\work\\TwitterAPI\\data\\cleaned_data"
# file_list = []
# for root, subdirs, files in os.walk(walk_dir):
#     path, book_name = os.path.split(root)
#     all_text = ""
#     for filename in files:
#         # os.path.join => join str with //
#         file_path = os.path.join(root, filename)
#         file_list.append(file_path)
#
#
# for file_name in file_list:
#     print('Loading: ' + file_name + '..')
#     with open(file_name) as f:
#         data = json.load(f)
#
#     # Prepare 2 obj (cleaned hashtag in tweet and count of hashtag)
#     for twt in data['tweets']:
#         # 1. Keep only original tweet by exclude retweet
#         # 2. Exclude Spam users
#         if twt['retweet_from_uid'] is None and twt['uid'] not in spam_users:
#             tag_list = []
#
#             # change all tags to lower case
#             [tag_list.append(h.lower()) for h in twt['hashtags']]
#
#             # distinct the list to remove duplicate hashtag
#             tag_list = list(set(tag_list))
#
#             # Prepare cleaned hashtag
#             clean_tweet_hashtag.append(tag_list)
#
#             for tag in tag_list:
#                 # get hashtag in dict and update count. If not exists just return 0 and plus 1
#                 hashtag_count[tag] = hashtag_count.get(tag, 0) + 1
#
# # save objects
# save_object(hashtag_count, 'hashtags_count_no_rt_and_bot_score.pkl')
# save_object(clean_tweet_hashtag,'clean_tweet_hashtag_no_rt_and_bot_score.pkl')

# # load from processed objects
hashtag_count = load_object('hashtags_count_no_rt_and_bot_score.pkl')
clean_tweet_hashtag = load_object('clean_tweet_hashtag_no_rt_and_bot_score.pkl')

####################################################################################
# Set Threshold of hashtag count and keep only hashtag with count higher than threshold
####################################################################################

### Set Threshold 2 options
# 1. Use mean
# min_count_threshold = np.mean(list(hashtag_count.values()))
mean_threshold = np.mean(list(hashtag_count.values()))
upper_threshold = np.mean(list(hashtag_count.values()))*2
lower_threshold = np.mean(list(hashtag_count.values()))/2
min_count_threshold = lower_threshold

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
# filtered_hashtag_in_twts = []
# included_hashtags = list(filter(lambda x: hashtag_count[x] > min_count_threshold, hashtag_count))
# print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + ' - Removing hashtags below threshold..')
# for idx, hset in enumerate(clean_tweet_hashtag):
#     # add new list to fix problem that entry of list removed on the way making the loop skipping the next entry
#     new_hset = []
#     [new_hset.append(h) for h in hset if h in included_hashtags]
#     filtered_hashtag_in_twts.append(new_hset)
#
# # print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + 'Done Cleaning spent: ' + str(datetime.datetime.now() - start))
#
# print("Minimum threshold: " + str(min_count_threshold))
# print("Total hashtag: "+ str(len(hashtag_count)))
# print("Frequent hashtag: "+ str(len(included_hashtags)))
#
# save_object(included_hashtags,'above-lower-mean_hashtags_botscore.pkl')
# save_object(filtered_hashtag_in_twts,'above-lower-mean_filtered_hashtag_in_twts_botscore.pkl')
#
# ######## gen 3 sets of node and edges file for gephi
# file_set = ['lower-mean','mean', 'upper-mean']
# file_set_thr = {'lower-mean':lower_threshold,'mean':mean_threshold, 'upper-mean':upper_threshold}
# for set_name in file_set:
#     included_hashtags = load_object('above-%s_hashtags_botscore.pkl'%(set_name))
#     filtered_hashtag_in_twts = load_object('above-%s_filtered_hashtag_in_twts_botscore.pkl'%(set_name))
#
#     # hashtag_count = load_object('genfile_0512-0616\\hashtags_count_no_rt_and_spam.pkl')
#     # included_hashtags = list(filter(lambda x: hashtag_count[x] > 44.3, hashtag_count))
#
#     # ## test
#     # clean_tweet_hashtag = clean_tweet_hashtag[0:2]
#     # clean_tweet_hashtag = [['bitcoin','btx'],['btc','btx']]
#     # included_hashtags = ['bitcoin','btc']
#     # for idx, hset in enumerate(clean_tweet_hashtag):
#     #     # add new list to fix problem that entry of list removed on the way making the loop skipping the next entry
#     #     new_hset = []
#     #     [new_hset.append(h) for h in hset if h in included_hashtags]
#     #     clean_tweet_hashtag[idx] = new_hset
#     # clean_tweet_hashtag
#
#     #######################################
#     # 2) Find co-occurrence hashtag. Set main hashtag and process one-by-one
#     #   Structure: dict{ 'used_tag': dict{ 'co_tag': count } }
#     #   Ex. dict_used_tag{ 'bitcoin': dict_co_tag{ 'eth': 10, 'btc': 9},
#     #                    'eth': dict_co_tag{ 'btc': 5, 'ltc': 4} ,... }
#     #######################################
#     start = datetime.datetime.now()
#     print(str(start) + ' - Find cooccur..')
#
#     # Prepare list of main hashtag to find its co-occurrence hashtag
#     # # set main hashtags as coins hashtag
#     # main_hashtags = [
#     #       'bitcoin', 'btc'
#     #     , 'ethereum', 'eth', 'ether'
#     #     , 'ripple', 'xrp'
#     #     , 'bitcoincash', 'bch'
#     #     , 'eosio', 'eos'
#     #     , 'litecoin', 'ltc'
#     #     , 'cardano', 'ada'
#     #     , 'stellar', 'xlm'
#     #     , 'iota', 'miota'
#     #     , 'tron', 'trx'
#     #     , 'neo'
#     #     , 'monero', 'xmr'
#     #     , 'dash'
#     #     , 'nem', 'xem'
#     #     , 'tether', 'usdt'
#     #     , 'vechain', 'ven'
#     #     , 'ethereumclassic', 'etc'
#     #     , 'bytecoin', 'bcn'
#     #     , 'binancecoin', 'bnb'
#     #     , 'qtum'
#     #     , 'zcash', 'zec'
#     #     , 'icx'
#     #     , 'omisego'
#     #     , 'lisk', 'lsk'
#     #     , 'zilliqa', 'zil'
#     #     , 'bitcoingold', 'btg'
#     #     , 'aeternity', 'ae'
#     #     , 'ontology', 'ont'
#     #     , 'verge', 'xvg'
#     #     , 'steem']
#     # set main hashtags as hashtag above threshold
#     main_hashtags = included_hashtags
#
#     dict_co_hashtag = {}
#     processed_tag = []
#     # count co-occurrence hashtags for each main hashtag one-by-one
#     for main_tag in main_hashtags:
#         start2 = datetime.datetime.now()
#
#         # add processed tag to a list to avoid duplicate pairs
#         processed_tag.append(main_tag)
#         # iterate set of hashtag of each tweet
#         dict_co_tag = {}
#         for twt_tags in filtered_hashtag_in_twts:
#             # Count co-tag by skipping main hashtag that already processed to avoid duplicate
#             # ex. [btc-eth], [eth-btc] we don't need the latter coz its the same
#             if main_tag in twt_tags:
#                 for co_tag in twt_tags:
#                     if co_tag not in processed_tag:
#                         dict_co_tag[co_tag] = dict_co_tag.get(co_tag, 0) + 1
#
#         # add co-occurrence hashtags of this main hashtag to the dict.
#         dict_co_hashtag[main_tag] = dict_co_tag.copy()
#         print(str(main_tag) + ": " + str(datetime.datetime.now() - start2))
#     print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + 'Done Finding spent: ' + str(datetime.datetime.now() - start))
#
#
#     ### 3) Generate co-occurrence hashtag file
#     start = datetime.datetime.now()
#     print(str(start) + ' - Save file..')
#
#     # prepare node file
#     with open('nodes_%s.csv'%(set_name),'w',newline='',encoding='utf-8') as f:
#         w = csv.writer(f)
#         w.writerow(['id','label'])
#         # sort asc
#         included_hashtags.sort()
#         for id, name in enumerate(included_hashtags):
#             w.writerow([id, name])
#
#     ## prepare edge file
#     with open('edges_%s.csv'%(set_name),'w',newline='',encoding='utf-8') as f:
#         w = csv.writer(f)
#         w.writerow(['Source','Target','Weight'])
#         for main_tag, co_tags in dict_co_hashtag.items():
#             src_id = included_hashtags.index(main_tag)
#             for tag, cooccur_count in co_tags.items():
#                 if cooccur_count > file_set_thr[set_name]:
#                     target_id = included_hashtags.index(tag)
#                     w.writerow([src_id, target_id, cooccur_count])


########################################################
# Analysing stats of hashtag
########################################################
# Prepare data
hashtag_above_lower_mean = load_object('above-lower-mean_hashtags_botscore.pkl')
print(len(hashtag_above_lower_mean))
hashtag_above_mean = load_object('above-mean_hashtags_botscore.pkl')
print(len(hashtag_above_mean))
hashtag_above_upper_mean = load_object('above-upper-mean_hashtags_botscore.pkl')
print(len(hashtag_above_upper_mean))

hashtag_count = load_object('hashtags_count_no_rt_and_bot_score.pkl')
mean_threshold = np.mean(list(hashtag_count.values()))
upper_threshold = np.mean(list(hashtag_count.values()))*2
lower_threshold = np.mean(list(hashtag_count.values()))/2
##

sorted_count = sorted(hashtag_count.items(), key=operator.itemgetter(1), reverse=True)
count = list(hashtag_count.values())
print("Total:%f" % (len(count)))
print("Lower_Mean_Threshold:%f" % (lower_threshold))
print("Mean_Threshold:%f" % (mean_threshold))
print("Upper_Mean_Threshold:%f" % (upper_threshold))
print("min:%f" % (np.min(count)))
print("max:%f" % (np.max(count)))
print("mean:%f" % (np.mean(count)))
print("median:%f" % (np.median(count)))
print("mode:%f" % (stats.mode(count)[0][0]))
print("std:%f" % (np.std(count)))

## PDF
plt.figure()
plt.subplot(211)
hist, bins, _ = plt.hist(count, bins=100, log=True, cumulative=False, density=False, color='orange')
plt.vlines(lower_threshold, 0, hist.max(), colors='r',linestyles=':', label='Mean/2')
plt.hold(); plt.vlines(mean_threshold, 0, hist.max(), colors='g',linestyles=':', label='Mean')
plt.hold(); plt.vlines(upper_threshold, 0, hist.max(), colors='b',linestyles=':', label='Mean*2')
# plt.hist(count, bins=50)
# plt.xlabel('Frequency of Hashtag used')
# plt.ylabel('Frequency')
plt.legend(loc='best')
plt.show()
plt.title('PDF of Hashtag frequency excluding Bot and Retweet')
plt.ylabel('Hashtag count in each bin')

##Log-log
logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
plt.subplot(212)
hist, bins, _ = plt.hist(count, log=True, bins=logbins, cumulative=False, density=False,color='orange')
plt.vlines(lower_threshold, 0, hist.max(), colors='r',linestyles=':', label='Mean/2')
plt.hold(); plt.vlines(mean_threshold, 0, hist.max(), colors='g',linestyles=':', label='Mean')
plt.hold(); plt.vlines(upper_threshold, 0, hist.max(), colors='b',linestyles=':', label='Mean*2')
plt.legend(loc='best'); plt.show()
plt.xscale('log')
plt.ylabel('Hashtag count in each bin')
plt.xlabel('Frequency of Hashtag used')

## CDF
plt.figure()
plt.subplot(211)
hist, bins, _ = plt.hist(count, bins=100, log=True, cumulative=True, density=True,color='orange')
plt.vlines(lower_threshold, 0, hist.max(), colors='r',linestyles=':', label='Mean/2')
plt.hold(); plt.vlines(mean_threshold, 0, hist.max(), colors='g',linestyles=':', label='Mean')
plt.hold(); plt.vlines(upper_threshold, 0, hist.max(), colors='b',linestyles=':', label='Mean*2')
# plt.hist(count, bins=50)
# plt.xlabel('Frequency of Hashtag used')
# plt.ylabel('Frequency')
plt.legend(loc='best')
plt.show()
plt.title('CDF of Hashtag frequency excluding Bot and Retweet')
plt.ylabel('Density')
## Log-log
logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
plt.subplot(212)
hist, bins, _ = plt.hist(count, log=True, bins=logbins, cumulative=True, density=True,color='orange')
plt.vlines(lower_threshold, 0, hist.max(), colors='r',linestyles=':', label='Mean/2')
plt.hold(); plt.vlines(mean_threshold, 0, hist.max(), colors='g',linestyles=':', label='Mean')
plt.hold(); plt.vlines(upper_threshold, 0, hist.max(), colors='b',linestyles=':', label='Mean*2')
plt.legend(loc='best'); plt.show()
plt.xscale('log')
plt.ylabel('Density')
plt.xlabel('Frequency of Hashtag used')
# plt.ylabel('Frequency')
# plt.title('Log-log CDF of Hashtag frequency excluded Bot and Retweet')
