import botometer
import logging

# setup logging
logging.basicConfig(filename='spam_detection.log',level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

def setup_botometer():
    # ## App1
    __CONSUMER_KEY = 'l9BvOKjP2Xj48I5wlc7Uh8sVN'
    __CONSUMER_SECRET = 'HMKOvmuCaReDIzc0GlzfjQGKFrdCJ9jHlRJd8AAp0e7PHfwl6H'
    __ACCESS_TOKEN = '982717247109189632-cdUZCv2mzMCDiPiHkdRDpUQXdRnFIvB'
    __ACCESS_TOKEN_SECRET = 'AaayN6WOC3rPcYIoBg1Cc5uEPeUbcrw2jFHhhZVlHzjGC'
    mashape_key = "w53bX6t0Kcmshcdk4EqeAMVor0pDp10Ap6CjsnKtcAyazyqwAm"

    twitter_app_auth = {
        'consumer_key': __CONSUMER_KEY,
        'consumer_secret': __CONSUMER_SECRET,
        'access_token': __ACCESS_TOKEN,
        'access_token_secret': __ACCESS_TOKEN_SECRET,
      }
    bom = botometer.Botometer(wait_on_ratelimit=True,
                              mashape_key=mashape_key,
                              **twitter_app_auth)
    return bom

def is_bot(user):
    # setup bot detector object.
    bom = setup_botometer()

    ##################################
    # check if user is bot?
    # user = '@thanadonf'
    result = bom.check_account(user)
    bot = result['cap']['english'] > 0.5
    u = result['user']['id_str']+':'+result['user']['screen_name']
    print("%s is bot?: %s(%f)"%(u,bot,result['cap']['english']))
    return bot

# from neo4j.v1 import GraphDatabase
# # connect to database
# uri = "bolt://localhost:7687"
# driver = GraphDatabase.driver(uri, auth=("neo4j", "11111"))
#
# ### test code ##################
# coin = 'omisego'
# q_test = """
# MATCH (h1:Hashtag)<-[:has]-(t:Tweet)-[:has]->(h2:Hashtag {tag:'%s'})
# WHERE h1.tag <> '%s'
# AND t.
# RETURN h1.tag AS hashtag, COUNT(*) AS count
# //ORDER BY count DESC
# """%(coin,coin)
#
# with driver.session() as session:
#     tx = session.begin_transaction()
#     ret = tx.run(q_test)
#     tx.commit()
# print('done')
# ret.values()

### count user from json
#Get json file path
import json
import os
import pickle
import operator

def load_object(filename):
    with open(filename, 'rb') as input:
        obj = pickle.load(input)
    return obj

def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

# ##################################################
# # Gen user post from all tweet data
# ##################################################
# walk_dir = "G:\\work\\TwitterAPI\\data\\cleaned_data"
# file_list = []
# for root, subdirs, files in os.walk(walk_dir):
#         path, book_name = os.path.split(root)
#         all_text = ""
#         for filename in files:
#             # os.path.join => join str with //
#             file_path = os.path.join(root, filename)
#             file_list.append(file_path)
#
# # test
# #file_list = ["G:\\work\\TwitterAPI\\data\\test\\test.json"]
# ###
# # count post from each user
# user_postcount = {}
# for filename in file_list:
#     print("Reading: %s.."%(filename))
#     with open(filename) as f:
#         data =json.load(f)
#         for twt in data['tweets']:
#             # Exclude Retweet
#             if twt['retweet_from_uid'] is None:
#                 user_postcount[twt['uid']] = user_postcount.get(twt['uid'], 0) + 1
#
# # sort desc
# logging.info("Sorting user_postcount .."); print("Sorting user_postcount ..")
# user_postcount = sorted(user_postcount.items(), key=operator.itemgetter(1), reverse=True)
#
# #save as obj
# logging.info("Saving as user_postcount_no_retweet.pkl .."); print("Saving as user_postcount_no_retweet.pkl ..")
# save_object(user_postcount, 'user_postcount_no_retweet.pkl')
#
# #save as json
# logging.info("Saving as user_postcount_no_retweet.json .."); print("Saving as user_postcount_no_retweet.json ..")
# with open('user_postcount_no_retweet.json', 'w') as f:
#     json.dump(user_postcount, f)
# logging.info("All jobs done!"); print("All jobs done!")


##################################################
# Gen user post stats and Find spam users
##################################################
# # load object
user_postcount = load_object('user_postcount.pkl')

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

#get list of post count
post_count = [u[1] for u in user_postcount]

# pritn stats
print("Total Users: %d"%(len(post_count)))
print("Min post_count: %.2f"%(np.min(post_count)))
print("Max post_count: %.2f"%(np.max(post_count)))
print("Mean post_count: %.2f"%(np.mean(post_count)))
print("Median post_count: %.2f"%(np.median(post_count)))
print("Sd post_count: %.2f"%(np.std(post_count)))
percent = 25; print("percentile%.2f: %.2f"%(percent,stats.scoreatpercentile(post_count,percent)))
percent = 50; print("percentile%.2f: %.2f"%(percent,stats.scoreatpercentile(post_count,percent)))
percent = 75; print("percentile%.2f: %.2f"%(percent,stats.scoreatpercentile(post_count,percent)))
percent = 99; print("percentile%.2f: %.2f"%(percent,stats.scoreatpercentile(post_count,percent)))
percent = 99.9; print("percentile%.2f: %.2f"%(percent,stats.scoreatpercentile(post_count,percent)))

#log
log_post_count = np.log(post_count)
print("Min log post_count: %.2f"%(np.min(log_post_count)))
print("Max log post_count: %.2f"%(np.max(log_post_count)))
print("Mean log post_count: %.2f"%(np.mean(log_post_count)))
print("Median log post_count: %.2f"%(np.median(log_post_count)))
print("Sd log post_count: %.2f"%(np.std(log_post_count)))
percent = 25; print("percentile%.2f: %.2f"%(percent,stats.scoreatpercentile(log_post_count,percent)))
percent = 50; print("percentile%.2f: %.2f"%(percent,stats.scoreatpercentile(log_post_count,percent)))
percent = 75; print("percentile%.2f: %.2f"%(percent,stats.scoreatpercentile(log_post_count,percent)))
percent = 99; print("percentile%.2f: %.2f"%(percent,stats.scoreatpercentile(log_post_count,percent)))
percent = 99.9; print("percentile%.2f: %.2f"%(percent,stats.scoreatpercentile(log_post_count,percent)))

# filter users under percentile
percentile = stats.scoreatpercentile(post_count,percent)
exclude_users = [tup for tup in user_postcount if tup[1]>percentile]
print("Excluded users:%s"%(len(exclude_users)))
save_object(exclude_users, 'excluded_user.pkl')

# plot histogram of post count
log_post_count = np.log(post_count)
log_percentile = stats.scoreatpercentile(log_post_count,percent)
h = plt.hist(log_post_count,bins = 50)
plt.vlines(log_percentile, 0 ,h[0][0], 'r')
plt.xlabel('Log(Post_Count)')
plt.ylabel('Frequency')
plt.title('Distribution of User Post Count')
#
is_bot(1002826017017192448)