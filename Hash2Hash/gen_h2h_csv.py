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
logging.basicConfig(filename='gen-cohashtag.log',level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

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
folder = "rework_addmorebot_2018-07-13\\"
min_count_threshold = 0 # will be set below
# spam_users = list(dict(load_object('excluded_user.pkl')).keys())
# spam_users = load_object('20180513-0626//bot-from-bot_score.pkl')
excluded_users = load_object(folder+'bot-from-bot_score-and-manual-check.pkl')
excluded_users = list(excluded_users.uid.values)

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

# prepare var
total_tweets = 0
non_eng_users = []
for file_name in file_list:
    print('Loading: ' + file_name + '..')
    with open(file_name) as f:
        data = json.load(f)

    # count tweets
    total_tweets+=len(data['tweets'])

    # prepare new data without RT and Bot
    new_data = {'tweets': []}

    # Prepare 2 obj (cleaned hashtag in tweet and count of hashtag)
    for twt in data['tweets']:
        # 1. Exclude retweet
        # 2. Exclude Spam users
        if twt['retweet_from_uid'] is None and twt['uid'] not in excluded_users:
            tag_list = []

            # change all tags to lower case
            [tag_list.append(h.lower()) for h in twt['hashtags']]

            # distinct the list to remove duplicate hashtag
            tag_list = set(tag_list)

            # check if tweet contain non-eng, add this user to excluded list and skip to next tweet
            skip = False
            for t in tag_list:
                if not isEnglish(t):
                    excluded_users.append(twt['uid'])
                    non_eng_users.append(twt['uid'])
                    skip = True
                    break
            if skip: continue

            # Prepare cleaned hashtag
            clean_tweet_hashtag.append(list(tag_list))

            # Count hashtag
            for tag in tag_list:
                # get hashtag in dict and update count. If not exists just return 0 and plus 1
                hashtag_count[tag] = hashtag_count.get(tag, 0) + 1

            # add to new data that has.. no RT, no Bot and only English
            new_data['tweets'].append(twt)

    #save as json
    newfilename = file_name.rstrip('.json') + "_filtered.json"
    with open(newfilename, 'w') as f:
        json.dump(new_data, f)
    print("New file written: %s"%newfilename)

# save objects
save_object(hashtag_count, folder+'hashtags_count.pkl')
save_object(clean_tweet_hashtag, folder+'clean_tweet_hashtag.pkl')
save_object(non_eng_users, folder+'non_eng_users.pkl')
save_object(excluded_users, folder+'excluded_users.pkl')
save_object(total_tweets, folder+'totaltweet.pkl')
logging.info("Total Tweet: %s"%str(total_tweets))

#test
hashtag_count = load_object(folder+'hashtags_count.pkl')
save_object(clean_tweet_hashtag, folder+'clean_tweet_hashtag.pkl')
save_object(non_eng_users, folder+'non_eng_users.pkl')
save_object(excluded_users, folder+'excluded_users.pkl')
total_tweets = load_object(folder+'totaltweet.pkl')


non_eng_users = load_object(folder+'non_eng_users.pkl')
# ############ test - combine hashtag
# clean_later = load_object('later_clean_tweet_hashtag_no_rt_and_bot_score.pkl')
# hashtag_later = load_object('later_hashtags_count_no_rt_and_bot_score.pkl')
# clean_s1 = load_object('s1_clean_tweet_hashtag_no_rt_and_bot_score.pkl')
# hashtag_s1 = load_object('s1_hashtags_count_no_rt_and_bot_score.pkl')
# hashtag_old = load_object('20180512-0617\\hashtags_count_no_rt_and_bot_score.pkl')
# clean_old= load_object('20180512-0617\\clean_tweet_hashtag_no_rt_and_bot_score.pkl')
#
# # combine hashtag
# for tag, count in hashtag_later.items():
#     print(tag)
#     print(count)
#     # get hashtag in dict and update count. If not exists just return 0 and plus 1
#     hashtag_s1[tag] = hashtag_s1.get(tag, 0) + count
#
# for tag, count in hashtag_s1.items():
#     # get hashtag in dict and update count. If not exists just return 0 and plus 1
#     hashtag_old[tag] = hashtag_old.get(tag, 0) + count
#
# save_object(hashtag_old, '20180513-0626\\hashtags_count_no_rt_and_bot_score.pkl')
#
# # combine clean hashtag
# clean_tweet_hashtag = clean_old + clean_s1 + clean_later
#
# save_object(clean_tweet_hashtag,'20180513-0626\\clean_tweet_hashtag_no_rt_and_bot_score.pkl')
# ##################################
#

####################################################################################
# Set Threshold of hashtag count and keep only hashtag with count higher than threshold
####################################################################################

# # # # load from processed objects
# hashtag_count = load_object(folder+'hashtag_count.pkl')
# clean_tweet_hashtag = load_object(folder+'clean_tweet_hashtag.pkl')

# ## remove non-eng
# df_tag = pd.DataFrame.from_dict(hashtag_count,orient='index')
# noneng_list=[]
# for index, row in df_tag.iterrows():
#     # list row that is non-eng
#     if not isEnglish(index):
#         noneng_list.append(index)
#
# # drop non-eng row
# df_eng = df_tag.drop(noneng_list)
# hashtag_count = pd.DataFrame.to_dict(df_eng)[0]
# save_object(hashtag_count_eng,'hashtag_count_eng.pkl')

### Set Threshold
# top 4000 (3710) by threshold = 52.3
mean_threshold = np.mean(list(hashtag_count.values()))#62.3
# # top1000 hashtags left (1000) -> thr = 292
upper_threshold = 292# np.mean(list(hashtag_count_eng.values()))*3#172.4
# # top10000 hashtags left (10203)
lower_threshold = 13# np.mean(list(hashtag_count_eng.values()))/3#19.2

min_count_threshold = lower_threshold

# included_hashtags = list(filter(lambda x: hashtag_count_eng[x] > min_count_threshold, hashtag_count_eng))
included_hashtags={}

for tag, count in hashtag_count.items():
    if count > min_count_threshold:
        included_hashtags[tag] = count
len(included_hashtags)
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + ' - Removing hashtags below threshold..')
save_object(included_hashtags,folder+'%s_included_hashtags.pkl'%min_count_threshold)

fileset = [str(mean_threshold), str(upper_threshold), str(lower_threshold)]
# fileset = ['top1000','top4000', 'top10000']
for file in fileset:
    clean_tweet_hashtag = load_object(folder+'clean_tweet_hashtag.pkl')
    included_hashtags = load_object(folder+'%s_included_hashtags.pkl'%file)
    included_hashtag_keywords = list(included_hashtags.keys())
    for tag_set in clean_tweet_hashtag:
        # add new list to fix problem that entry of list removed on the way making the loop skipping the next entry
        for tag in list(tag_set):
            if tag not in included_hashtag_keywords:
                #print(tag + ' is removed')
                tag_set.remove(tag)
    filtered_hashtag_in_twts = clean_tweet_hashtag
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + 'Done Cleaning')

    # print("Minimum threshold: " + str(min_count_threshold))
    # print("Total hashtag: "+ str(len(hashtag_count_eng)))
    # print("Frequent hashtag: "+ str(len(included_hashtags)))


    save_object(filtered_hashtag_in_twts, folder+'%s_filtered_hashtag_in_twts.pkl'%file)
    # save_object(included_hashtags,'upper_mean_hashtags.pkl')
    # save_object(filtered_hashtag_in_twts,'upper_mean_filtered_hashtag_in_twts.pkl')
    # save_object(included_hashtags,'lower_mean_hashtags.pkl')
    # save_object(filtered_hashtag_in_twts,'lower_mean_filtered_hashtag_in_twts.pkl')

############################################################################################
# gen 3 sets of node and edges file for gephi
############################################################################################
# fileset = ['top1000', 'top4000', 'top10000']
# file_set = ['mean']
for set_name in fileset:
    included_hashtags = load_object(folder+'%s_included_hashtags.pkl'%(set_name))
    filtered_hashtag_in_twts = load_object(folder+'%s_filtered_hashtag_in_twts.pkl'%(set_name))

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
    logging.info('Start finding Co-occurring hashtag..')

    # # Prepare list of main hashtag to find its co-occurrence hashtag
    # set main hashtags as hashtag above threshold
    main_hashtags = included_hashtags

    dict_co_hashtag = {}
    processed_tag = []
    # count co-occurrence hashtags for each main hashtag one-by-one
    for main_tag in list(main_hashtags.keys()):
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

    save_object(dict_co_hashtag, folder+'%s_dict_co_hashtag.pkl'%set_name)
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + 'Done Finding spent: ' + str(datetime.datetime.now() - start))
    logging.info('Done finding Co-occurring hashtag')

# fileset = ['top1000','top4000', 'top10000']
for set_name in fileset:
    ############################################################################################
    # Build probability matrix of hashtag - to normalise co-occurrence network
    ############################################################################################
    # set_name = 'mean'
    # included_hashtags = load_object('20180513-0626\\%s_included_hashtags.pkl'% set_name)
    included_hashtags = load_object(folder+'%s_included_hashtags.pkl' % set_name)
    dict_co_hashtag = load_object(folder+"%s_dict_co_hashtag.pkl" % set_name)
    # d = {'a': [], 'b': [], 'p(a)': [], 'p(b)': [], 'p(a)p(b)': [], 'p(a,b)': [], 'p(a,b)-p(a)p(b)': []}
    d = {'a': [], 'b': [], 'p(a)': [], 'p(b)': [], 'p(a)p(b)': [], 'p(a,b)': []}
    df_cotag = pd.DataFrame(data=d)
    total_tag = np.sum(list(included_hashtags.values()))

    for a, b_list in dict_co_hashtag.items():
        # prepare list to assign data
        a_list, prob_a_list, prob_b_list, prob_a_prob_b_list, prob_ab_list, norm_weight_list = [], [], [], [], [], []

        prob_a = included_hashtags[a] / total_tag
        for b, count in b_list.items():
            prob_b = included_hashtags[b] / total_tag
            prob_a_prob_b = prob_a * prob_b
            prob_ab = count / total_tag
            a_list.append(a)
            prob_a_list.append(prob_a)
            prob_b_list.append(prob_b)
            prob_a_prob_b_list.append(prob_a_prob_b)
            prob_ab_list.append(prob_ab)
            # # normalise weight by p(a,b) - p(a)p(b) means minus by prob that happen by chance
            # norm_weight_list.append(prob_ab - prob_a_prob_b)
        df = pd.DataFrame(
            {'a': a_list, 'b': list(b_list), 'p(a)': prob_a_list, 'p(b)': prob_b_list,
             'p(a)p(b)': prob_a_prob_b_list, 'p(a,b)': prob_ab_list})

        # concat to the main df
        df_cotag = pd.concat([df_cotag, df])

    # Keep only P(a,b) > P(a)P(b). Thus, not co-occur by chance
    df_normalised_cotag = df_cotag.loc[df_cotag['p(a,b)'] > df_cotag['p(a)p(b)']]
    df_exclued_cotag = df_cotag.loc[df_cotag['p(a,b)'] <= df_cotag['p(a)p(b)']]

    # Calculate weight from: weight = P(a,b) - P(a)P(b) / sd(P(a)P(b))
    weight = (df_normalised_cotag['p(a,b)']-df_normalised_cotag['p(a)p(b)'])/np.std(df_normalised_cotag['p(a)p(b)'])
    df_normalised_cotag['weight'] = weight

    # Save file
    df_cotag.to_csv(folder+'%s_full_cotag.csv' % set_name, encoding='utf-8', index=False)
    df_normalised_cotag.to_csv(folder+'%s_normalised_cotag.csv' % set_name, encoding='utf-8', index=False)
    df_exclued_cotag.to_csv(folder+'%s_excluded_cotag.csv' % set_name, encoding='utf-8', index=False)

    # write file for Gephi
    # df_gephi = df_normalised_cotag[['a', 'b', 'p(a,b)-p(a)p(b)']]
    df_gephi = df_normalised_cotag[['a', 'b', 'weight']]
    df_gephi.columns = ['source', 'target', 'weight']
    scaler = MinMaxScaler(feature_range=(1, 10))
    scaler.fit(df_gephi[['weight']])
    df_gephi.loc[:, 'weight'] = scaler.transform(df_gephi[['weight']])
    df_gephi.to_csv(folder+'s10gephi_%s_normalised_cotag.csv' % set_name, encoding='utf-8', index=False)

    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + 'Done ' + set_name)
logging.info('Done create hashtag probability matrix')

## test
filename = 'top10000'
df_test = pd.read_csv('rework_addmorebot_2018-07-13\\52.35532252754701_dict_co_hashtag.pkl' , encoding='utf-8')
df_test.shape
sd = np.std(df_test['p(a)p(b)'])
df_test_norm = df_test.loc[df_test['p(a,b)'] > df_test['p(a)p(b)']]
df_test_norm['weight'] = (df_test_norm['p(a,b)']-df_test_norm['p(a)p(b)']) / sd
df_test_gephi = df_test_norm[['a', 'b', 'weight']]
df_test_gephi.columns = ['source', 'target', 'weight']
scaler = MinMaxScaler(feature_range=(1, 10))
scaler.fit(df_test_gephi[['weight']])
df_test_gephi.loc[:, 'weight'] = scaler.transform(df_test_gephi[['weight']])
df_test_gephi.to_csv('eng\\s10_gephi_%s_normalised_cotag.csv' % filename, encoding='utf-8', index=False)
df_test_gephi.shape
##

    # # dict_co_hashtag = load_object('20180512-0617\\%s_dict_co_hashtag.pkl'%set_name)
    # ### 3) Generate co-occurrence hashtag file
    # start = datetime.datetime.now()
    # print(str(start) + ' - Save file..')
    #
    # logging.info('Generating Node.csv ..')
    # # prepare node file
    # with open('20180513-0626\\nodes_%s.csv'%(set_name),'w',newline='',encoding='utf-8') as f:
    #     w = csv.writer(f)
    #     w.writerow(['id','label'])
    #     # sort asc
    #     included_hashtags.sort()
    #     for id, name in enumerate(included_hashtags):
    #         w.writerow([id, name])
    #
    # logging.info('Generating Edge.csv ..')
    # ## prepare edge file
    # with open('20180513-0626\\edges_all_%s.csv'%(set_name),'w',newline='',encoding='utf-8') as f:
    #     w = csv.writer(f)
    #     w.writerow(['Source','Target','Weight'])
    #     for main_tag, co_tags in dict_co_hashtag.items():
    #         src_id = included_hashtags.index(main_tag)
    #         for tag, cooccur_count in co_tags.items():
    #                 target_id = included_hashtags.index(tag)
    #                 w.writerow([src_id, target_id, cooccur_count])
    #
    # logging.info('Complete generating node and edge..')



############################################################################################
# # Analysing stats of hashtag
############################################################################################
# # Prepare data
# hashtag_above_lower_mean = load_object('above-lower-mean_hashtags_botscore.pkl')
# print(len(hashtag_above_lower_mean))
# hashtag_above_mean = load_object('above-mean_hashtags_botscore.pkl')
# print(len(hashtag_above_mean))
# hashtag_above_upper_mean = load_object('above-upper-mean_hashtags_botscore.pkl')
# print(len(hashtag_above_upper_mean))
#
# hashtag_count_eng = load_object('hashtags_count_no_rt_and_bot_score.pkl')
# mean_threshold = np.mean(list(hashtag_count_eng.values()))
# upper_threshold = np.mean(list(hashtag_count_eng.values()))*2
# lower_threshold = np.mean(list(hashtag_count_eng.values()))/2
# ##
#
# sorted_count = sorted(hashtag_count_eng.items(), key=operator.itemgetter(1), reverse=True)
# count = list(hashtag_count_eng.values())
# print("Total:%f" % (len(count)))
# print("Lower_Mean_Threshold:%f" % (lower_threshold))
# print("Mean_Threshold:%f" % (mean_threshold))
# print("Upper_Mean_Threshold:%f" % (upper_threshold))
# print("min:%f" % (np.min(count)))
# print("max:%f" % (np.max(count)))
# print("mean:%f" % (np.mean(count)))
# print("median:%f" % (np.median(count)))
# print("mode:%f" % (stats.mode(count)[0][0]))
# print("std:%f" % (np.std(count)))
#
# ## PDF
# plt.figure()
# plt.subplot(211)
# hist, bins, _ = plt.hist(count, bins=100, log=True, cumulative=False, density=False, color='orange')
# plt.vlines(lower_threshold, 0, hist.max(), colors='r',linestyles=':', label='Mean/2')
# plt.hold(); plt.vlines(mean_threshold, 0, hist.max(), colors='g',linestyles=':', label='Mean')
# plt.hold(); plt.vlines(upper_threshold, 0, hist.max(), colors='b',linestyles=':', label='Mean*2')
# # plt.hist(count, bins=50)
# # plt.xlabel('Frequency of Hashtag used')
# # plt.ylabel('Frequency')
# plt.legend(loc='best')
# plt.show()
# plt.title('PDF of Hashtag frequency excluding Bot and Retweet')
# plt.ylabel('Hashtag count in each bin')
#
# ##Log-log
# logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
# plt.subplot(212)
# hist, bins, _ = plt.hist(count, log=True, bins=logbins, cumulative=False, density=False,color='orange')
# plt.vlines(lower_threshold, 0, hist.max(), colors='r',linestyles=':', label='Mean/2')
# plt.hold(); plt.vlines(mean_threshold, 0, hist.max(), colors='g',linestyles=':', label='Mean')
# plt.hold(); plt.vlines(upper_threshold, 0, hist.max(), colors='b',linestyles=':', label='Mean*2')
# plt.legend(loc='best'); plt.show()
# plt.xscale('log')
# plt.ylabel('Hashtag count in each bin')
# plt.xlabel('Frequency of Hashtag used')
#
# ## CDF
# plt.figure()
# plt.subplot(211)
# hist, bins, _ = plt.hist(count, bins=100, log=True, cumulative=True, density=True,color='orange')
# plt.vlines(lower_threshold, 0, hist.max(), colors='r',linestyles=':', label='Mean/2')
# plt.hold(); plt.vlines(mean_threshold, 0, hist.max(), colors='g',linestyles=':', label='Mean')
# plt.hold(); plt.vlines(upper_threshold, 0, hist.max(), colors='b',linestyles=':', label='Mean*2')
# # plt.hist(count, bins=50)
# # plt.xlabel('Frequency of Hashtag used')
# # plt.ylabel('Frequency')
# plt.legend(loc='best')
# plt.show()
# plt.title('CDF of Hashtag frequency excluding Bot and Retweet')
# plt.ylabel('Density')
# ## Log-log
# logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
# plt.subplot(212)
# hist, bins, _ = plt.hist(count, log=True, bins=logbins, cumulative=True, density=True,color='orange')
# plt.vlines(lower_threshold, 0, hist.max(), colors='r',linestyles=':', label='Mean/2')
# plt.hold(); plt.vlines(mean_threshold, 0, hist.max(), colors='g',linestyles=':', label='Mean')
# plt.hold(); plt.vlines(upper_threshold, 0, hist.max(), colors='b',linestyles=':', label='Mean*2')
# plt.legend(loc='best'); plt.show()
# plt.xscale('log')
# plt.ylabel('Density')
# plt.xlabel('Frequency of Hashtag used')
# # plt.ylabel('Frequency')
# # plt.title('Log-log CDF of Hashtag frequency excluded Bot and Retweet')




# ############################################################################################
# # Analyse co-occurrence hashtag
# ############################################################################################
# dict_co_hashtag = load_object('20180512-0617\\%s_dict_co_hashtag.pkl' % "mean")
# count = []
# for m in dict_co_hashtag.values():
#     for w in m.values():
#         count.append(w)
# len(count)
# med_threshold = np.median(count)
# mean_threshold = np.mean(count)
# ## PDF
# plt.figure()
# plt.subplot(211)
# hist, bins, _ = plt.hist(count, bins=100, log=True, cumulative=False, density=False, color='orange')
# plt.vlines(med_threshold, 0, hist.max(), colors='r',linestyles=':', label='Median')
# plt.hold(); plt.vlines(mean_threshold, 0, hist.max(), colors='g',linestyles=':', label='Mean')
# # plt.hold(); plt.vlines(upper_threshold, 0, hist.max(), colors='b',linestyles=':', label='Mean*2')
# plt.legend(loc='best')
# plt.show()
# plt.title('PDF of Co-occurrence Hashtag')
# plt.ylabel('Frequency of Co-occurrence Hashtag')
#
# ##Log-log
# logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
# plt.subplot(212)
# hist, bins, _ = plt.hist(count, log=True, bins=logbins, cumulative=False, density=False,color='orange')
# plt.vlines(med_threshold, 0, hist.max(), colors='r',linestyles=':', label='Median')
# plt.hold(); plt.vlines(mean_threshold, 0, hist.max(), colors='g',linestyles=':', label='Mean')
# plt.legend(loc='best'); plt.show()
# plt.xscale('log')
# plt.xlabel('Co-occurrence Hashtag')
#
# ## CDF
# plt.figure()
# # plt.subplot(211)
# # hist, bins, _ = plt.hist(count, bins=100, log=True, cumulative=True, density=True,color='orange')
# # plt.vlines(med_threshold, 0, hist.max(), colors='r',linestyles=':', label='Median')
# # plt.hold(); plt.vlines(mean_threshold, 0, hist.max(), colors='g',linestyles=':', label='Mean')
# # # plt.hold(); plt.vlines(upper_threshold, 0, hist.max(), colors='b',linestyles=':', label='Mean*2')
# #
#
# # plt.ylabel('Density')
# ## Log-log
# logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
# plt.subplot(111)
# hist, bins, _ = plt.hist(count, log=True, bins=logbins, cumulative=True, density=True,color='orange')
# plt.vlines(med_threshold, 0, hist.max(), colors='r',linestyles=':', label='Median')
# plt.hold(); plt.vlines(mean_threshold, 0, hist.max(), colors='g',linestyles=':', label='Mean')
# plt.legend(loc='best'); plt.show()
# plt.xscale('log')
# plt.ylabel('Density')
# plt.xlabel('Co-occurrence Hashtag')
# plt.legend(loc='best')
# plt.show()
# plt.title('CDF of Co-occurrence Hashtag excluding Bot and Retweet')
# # plt.ylabel('Frequency')
# # plt.title('Log-log CDF of Hashtag frequency excluded Bot and Retweet')
#
# ##
