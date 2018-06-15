######
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

#######################################
# 1) Clean and prepare set of hashtags
#######################################
start = datetime.datetime.now()
print(str(start) + ' - Cleaning..')

clean_tweet_hashtag = []
imp_hashtag_list = []
hashtag_count = {}

# # Change hashtag to lowercase before running cypher to increase speed
# for tidx, t in enumerate(data['tweets']):
#     for hidx, h in enumerate(t['hashtags']):
#         data['tweets'][tidx]['hashtags'][hidx] = h.lower()

# Prepare cleaned hashtag
#Get json file path
walk_dir = "G:\\work\\TwitterAPI\\data\\used_data"
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

    for twt in data['tweets']:
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
# save_object(hashtag_count,'hashtags_count.pkl')
# save_object(clean_tweet_hashtag,'clean_tweet_hashtag.pkl')
# get count of each searched hashtags
coins = ['bitcoin','btc','ethereum','eth','ether','ripple','xrp','bitcoincash','bch','eosio','eos','litecoin','ltc','cardano','ada','stellar','xlm','iota','miota','tron','trx','neo','monero','xmr','dash','nem','xem','tether','usdt','vechain','ven','ethereumclassic','etc','bytecoin','bcn','binancecoin','bnb','qtum','zcash','zec','icx','omisego','lisk','lsk','zilliqa','zil','bitcoingold','btg','aeternity','ae','ontology','ont','verge','xvg','steem']
coin_hash_count = {}
for key in coins:
    coin_hash_count[key] = hashtag_count[key]
coin_hash_count = sorted(coin_hash_count.items(), key=operator.itemgetter(1), reverse=True)
coin_hash_count[len(coin_hash_count)-1]
# set threshold to 10% of the least frequent coin count
min_count_threshold = coin_hash_count[len(coin_hash_count)-1][1]*0.1

# ## Analysing stats of hashtag
# hashtag_count = load_object('hashtags_count.pkl')
# clean_tweet_hashtag = load_object('clean_tweet_hashtag.pkl')
# count = list(hashtag_count.values())
# print("Total:%f" % (len(count)))
# print("min:%f" % (np.min(count)))
# print("max:%f" % (np.max(count)))
# print("mean:%f" % (np.mean(count)))
# print("median:%f" % (np.median(count)))
# print("mode:%f" % (stats.mode(count)[0][0]))
# print("std:%f" % (np.std(count)))
#
# # plot histogram
# hist_info = plt.hist(np.log(count), bins=50)
# plt.vlines(np.log(min_count_threshold),hist_info[0].min(),hist_info[0].max(),colors='r',label='Threshold')
# # plt.hist(count, bins=50)
# plt.xlabel('Log occurrence')
# plt.ylabel('Frequency')
# ##

# Prepare important hashtag by filter out rare hashtag (from threshold)
imp_hashtag_list = list(filter(lambda x: hashtag_count[x] > min_count_threshold, hashtag_count))

# Remove hashtag which are not in the important list
for hset in clean_tweet_hashtag:
    [hset.remove(h) for h in hset if h not in imp_hashtag_list]
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + 'Done Cleaning spent: ' + str(datetime.datetime.now() - start))

print("Minimum threshold: " + str(min_count_threshold))
print("Total hashtag: "+ str(len(hashtag_count)))
print("Important hashtag: "+ str(len(imp_hashtag_list)))


#######################################
# 2) Find co-occurrence hashtag. Set main hashtag and process one-by-one
#   Structure: dict{ 'used_tag': dict{ 'co_tag': count } }
#   Ex. dict_used_tag{ 'bitcoin': dict_co_tag{ 'eth': 10, 'btc': 9},
#                    'eth': dict_co_tag{ 'btc': 5, 'ltc': 4} ,... }
#######################################
start = datetime.datetime.now()
print(str(start) + ' - Find cooccur..')

dict_co_hashtag = {}
processed_tag = []
# count co-occurrence hashtags for each used hashtag one-by-one
# imp_hashtag_list = ['bitcoin','omg']
for main_tag in imp_hashtag_list:
    start2 = datetime.datetime.now()
    # add processed tag to a list to avoid duplicate pairs
    processed_tag.append(main_tag)

    # iterate set of hashtag of each tweet
    dict_co_tag = {}
    for twt_tags in clean_tweet_hashtag:
    # a = [ t['hashtags'] for t in data['tweets']]
    # for twt_tags in a:
        # count co-occurrence if tweet contain main tag
        if main_tag in twt_tags:
            # Count co-tag by skipping main hashtag to avoid duplicate
            # ex. [btc-eth], [eth-btc] we don't need the latter coz its the same
            for co_tag in twt_tags:
                if co_tag not in processed_tag:
                    dict_co_tag[co_tag] = dict_co_tag.get(co_tag, 0) + 1

    # add co-occurrence hashtags of this main hashtag to the dict.
    dict_co_hashtag[main_tag] = dict_co_tag
    print(str(main_tag) + ": " + str(datetime.datetime.now() - start2))
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + 'Done Finding spent: ' + str(datetime.datetime.now() - start))


### 3) Generate co-occurrence hashtag file
start = datetime.datetime.now()
print(str(start) + ' - Save file..')

with open('co-hashtag.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["hashtag1", "hashtag2", "count"])
    for main_tag, main_dict in dict_co_hashtag.items():
        for co_tag, co_count in main_dict.items():
            writer.writerow([main_tag, co_tag, co_count])
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + 'Done Save file spent: ' + str(datetime.datetime.now() - start))
