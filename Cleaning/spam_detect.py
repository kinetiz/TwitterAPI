import botometer
import logging
import pandas as pd
# setup logging
logging.basicConfig(filename='spam_detection.log',level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

def setup_botometer():
    ## App1
    __CONSUMER_KEY = 'l9BvOKjP2Xj48I5wlc7Uh8sVN'
    __CONSUMER_SECRET = 'HMKOvmuCaReDIzc0GlzfjQGKFrdCJ9jHlRJd8AAp0e7PHfwl6H'
    __ACCESS_TOKEN = '982717247109189632-cdUZCv2mzMCDiPiHkdRDpUQXdRnFIvB'
    __ACCESS_TOKEN_SECRET = 'AaayN6WOC3rPcYIoBg1Cc5uEPeUbcrw2jFHhhZVlHzjGC'
    mashape_key = "w53bX6t0Kcmshcdk4EqeAMVor0pDp10Ap6CjsnKtcAyazyqwAm"

    # ### App2
    # __CONSUMER_KEY = 'L7IX0KwYgQUGeC1TqnxULue1v'
    # __CONSUMER_SECRET = 'gRiqmdED0KFVjg6v2x9giQmctFLdAiFwEioCECuVCTJafp8byB'
    # __ACCESS_TOKEN = '982717247109189632-QRXdgrmZdhIy00do6D5o0wpdUMVKvJU'
    # __ACCESS_TOKEN_SECRET = 'szb7jQaVBe8JCf9iM23e3GBd7OgbuLRDxhTM6nU4L3QAp'
    # mashape_key = "U9FdFWj9X4msh7uuWlVccyFcTai5p1EIqV2jsnXUiPRb0Z04yT"

    # ## App3
    # __CONSUMER_KEY = 'w3TysRbh9H6oKp5T8qVNeSEdl'
    # __CONSUMER_SECRET = 'LJA4sjmh4mq7OvmfUngVr7OX7rAnxeuUsKPT9rbzD9iU1sWfa3'
    # __ACCESS_TOKEN = '982717247109189632-rB4KizgqhsFdMS1V1Tu8qcPdxAe2dDi'
    # __ACCESS_TOKEN_SECRET = 'joe3MY7vIjWhDttHMMTJmgchzOLYUNqhjGUuWpAS4d3Ro'
    # mashape_key = "cUoaAQSE5xmshWYV9xPOqphXPQvSp1j9WcPjsn0CMPY2c7Aopg"
    ####

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
    return result

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

# # ##################################################
# # # Gen user post from all tweet data
# # ##################################################
# # walk_dir = "G:\\work\\TwitterAPI\\data\\cleaned_data"
# # file_list = []
# # for root, subdirs, files in os.walk(walk_dir):
# #         path, book_name = os.path.split(root)
# #         all_text = ""
# #         for filename in files:
# #             # os.path.join => join str with //
# #             file_path = os.path.join(root, filename)
# #             file_list.append(file_path)
# #
# # # test
# # #file_list = ["G:\\work\\TwitterAPI\\data\\test\\test.json"]
# # ###
# # # count post from each user
# # user_postcount = {}
# # for filename in file_list:
# #     print("Reading: %s.."%(filename))
# #     with open(filename) as f:
# #         data =json.load(f)
# #         for twt in data['tweets']:
# #             # Exclude Retweet
# #             if twt['retweet_from_uid'] is None:
# #                 user_postcount[twt['uid']] = user_postcount.get(twt['uid'], 0) + 1
# #
# # # sort desc
# # logging.info("Sorting user_postcount .."); print("Sorting user_postcount ..")
# # user_postcount = sorted(user_postcount.items(), key=operator.itemgetter(1), reverse=True)
# #
# # #save as obj
# # logging.info("Saving as user_postcount_no_retweet.pkl .."); print("Saving as user_postcount_no_retweet.pkl ..")
# # save_object(user_postcount, 'user_postcount_no_retweet.pkl')
# #
# # #save as json
# # logging.info("Saving as user_postcount_no_retweet.json .."); print("Saving as user_postcount_no_retweet.json ..")
# # with open('user_postcount_no_retweet.json', 'w') as f:
# #     json.dump(user_postcount, f)
# # logging.info("All jobs done!"); print("All jobs done!")
#
#
# ##################################################
# # Gen user post stats and Find spam users
# ##################################################
# # # load object
user_postcount = load_object('user_postcount_no_retweet.pkl')
#
# import matplotlib.pyplot as plt
# import numpy as np
# from scipy import stats
#
# #get list of post count
# post_count = [u[1] for u in user_postcount]
#
# # pritn stats
# print("Total Users: %d"%(len(post_count)))
# print("Min post_count: %.2f"%(np.min(post_count)))
# print("Max post_count: %.2f"%(np.max(post_count)))
# print("Mean post_count: %.2f"%(np.mean(post_count)))
# print("Median post_count: %.2f"%(np.median(post_count)))
# print("Sd post_count: %.2f"%(np.std(post_count)))
# percent = 25; print("percentile%.2f: %.2f"%(percent,stats.scoreatpercentile(post_count,percent)))
# percent = 50; print("percentile%.2f: %.2f"%(percent,stats.scoreatpercentile(post_count,percent)))
# percent = 75; print("percentile%.2f: %.2f"%(percent,stats.scoreatpercentile(post_count,percent)))
# percent = 99; print("percentile%.2f: %.2f"%(percent,stats.scoreatpercentile(post_count,percent)))
# percent = 99.9; print("percentile%.2f: %.2f"%(percent,stats.scoreatpercentile(post_count,percent)))
#
# # #log
# # log_post_count = np.log(post_count)
# # print("Min log post_count: %.2f"%(np.min(log_post_count)))
# # print("Max log post_count: %.2f"%(np.max(log_post_count)))
# # print("Mean log post_count: %.2f"%(np.mean(log_post_count)))
# # print("Median log post_count: %.2f"%(np.median(log_post_count)))
# # print("Sd log post_count: %.2f"%(np.std(log_post_count)))
# # percent = 25; print("percentile%.2f: %.2f"%(percent,stats.scoreatpercentile(log_post_count,percent)))
# # percent = 50; print("percentile%.2f: %.2f"%(percent,stats.scoreatpercentile(log_post_count,percent)))
# # percent = 75; print("percentile%.2f: %.2f"%(percent,stats.scoreatpercentile(log_post_count,percent)))
# # percent = 99; print("percentile%.2f: %.2f"%(percent,stats.scoreatpercentile(log_post_count,percent)))
# # percent = 99.9; print("percentile%.2f: %.2f"%(percent,stats.scoreatpercentile(log_post_count,percent)))
# #
# # # filter users under percentile
# # percentile = stats.scoreatpercentile(post_count,percent)
# # exclude_users = [tup for tup in user_postcount if tup[1]>percentile]
# # print("Excluded users:%s"%(len(exclude_users)))
# # # save_object(exclude_users, 'excluded_user.pkl')
#
# # # plot histogram of post count
# # log_post_count = np.log(post_count)
# # log_percentile = stats.scoreatpercentile(log_post_count,percent)
#
# # # log log scale
# # fig = plt.figure(); ax = fig.add_subplot(1, 1, 1)
# # h = ax.hist(post_count,bins=np.logspace(np.log10(0.1),np.log10(5), 10), log = True,cumulative=False)
# # ax.set_xscale('log')
#
# # log y scale
# fig = plt.figure(); ax = fig.add_subplot(1, 1, 1)
# h = ax.hist(post_count,bins=100, log = True,cumulative=False)
#
# plt.vlines(log_percentile, 0 ,h[0][0], 'r')
# plt.xlabel('No. of Tweet from each User)')
# plt.ylabel('Log Frequency')
# plt.title('Distribution of User tweets')
# #
# is_bot(962428211249471498)
#
# ######################################################3
# # Gen users to check bot
# ######################################################3
# ## prepare set of users to check bot (post > 15 tweets)
# check_users = [tup[0] for tup in user_postcount if tup[1]>15]
# print("check_users users:%s"%(len(check_users)))
# import math
# chunk_size = math.ceil(len(check_users)/3)
# spam_check_set1 = check_users[0:chunk_size]
# spam_check_set2 = check_users[chunk_size:chunk_size*2]
# spam_check_set3 = check_users[chunk_size*2:len(check_users)]
# save_object(spam_check_set1,'spam_check_set1.pkl')
# save_object(spam_check_set2,'spam_check_set2.pkl')
# save_object(spam_check_set3,'spam_check_set3.pkl')
#
# ## get result from botometer
# bot_results = {}
# error_user = {}
# for idx, u in enumerate(spam_check_set1):
#     print(idx)
#     try:
#         result = is_bot(u)
#         id = result['user']['id_str']
#         bot_results[id] = result
#     except Exception as e:
#         logging.info("Error user: %s | %s " % (u, str(e)))
#         error_user[u] = str(e)
#
# save_object(bot_results, 'bot_results_set1.pkl')
# save_object(error_user, 'error_user_set1.pkl')
#
# # # sort desc
# # sorted_bot_results = sorted(bot_results.items(), key=operator.itemgetter(1), reverse=True)

# compare relationship of bot vs no. of tweets posted
import pandas as pd

# combine the results into one object
bot_results_set1 = load_object('bot_results_set1.pkl')
bot_results_set2 = load_object('bot_results_set2.pkl')
bot_results_set3 = load_object('bot_results_set3.pkl')

bot_results = {}
bot_results.update(bot_results_set1)
bot_results.update(bot_results_set2)
bot_results.update(bot_results_set3)


df = pd.DataFrame(columns=['bot_cap','bot_score','bot_cat_content'
        ,'bot_cat_friend','bot_cat_network','bot_cat_sentiment'
        ,'bot_cat_temporal','bot_cat_user'])

for idx, user_twt in enumerate(user_postcount):
    # avoid error by processing only the uid existing in the results dict
    if str(user_twt[0]) in bot_results:
        bot_cap = bot_results[str(user_twt[0])]['cap']['english']
        bot_score = bot_results[str(user_twt[0])]['scores']['english']
        bot_cat_content = bot_results[str(user_twt[0])]['categories']['content']
        bot_cat_friend = bot_results[str(user_twt[0])]['categories']['friend']
        bot_cat_network = bot_results[str(user_twt[0])]['categories']['network']
        bot_cat_sentiment = bot_results[str(user_twt[0])]['categories']['sentiment']
        bot_cat_temporal = bot_results[str(user_twt[0])]['categories']['temporal']
        bot_cat_user = bot_results[str(user_twt[0])]['categories']['user']
        screen_name = bot_results[str(user_twt[0])]['user']['screen_name']
        df = df.append({'uid':user_twt[0],'screen_name':screen_name, 'twt': user_twt[1],
                    'bot_cap': bot_cap, 'bot_score': bot_score,
                    'bot_cat_content': bot_cat_content, 'bot_cat_friend': bot_cat_friend,
                    'bot_cat_network': bot_cat_network, 'bot_cat_sentiment': bot_cat_sentiment,
                    'bot_cat_temporal': bot_cat_temporal, 'bot_cat_user': bot_cat_user
                   }, ignore_index=True)
        print('%d: %s has been processed..'%(idx,screen_name))

# # df.sort_values(by="twt")
# save_object(df,'df_bot_results.pkl')

df = load_object('df_bot_results.pkl')

### select bot
bot_user = df[df.bot_score > 0.5][['uid', 'screen_name','bot_score']]
bot_user.head
save_object(bot_user, 'bot-from-bot_score.pkl')

#### no. of bot in total
# def count_bot(bot_prob_list):
#     bot_total = 0
#     for bot in bot_prob_list:
#         if bot > 0.5:
#             bot_total+=1
#     return bot_total
# # plot graph comparing no. of tweets vs bot prob.
# bot_measures = ['bot_cap',
#                 'bot_score',
#                 'bot_cat_content',
#                 'bot_cat_network',
#                 'bot_cat_temporal',
#                 'bot_cat_friend',
#                 'bot_cat_sentiment',
#                 'bot_cat_user'
#                 ]
# # for measure in bot_measures:
# df1 = df[['twt','bot_score']]
# label = []
# for row in df1.values:
# ## scale 100
#     if 0 <= row[0] < 100:
#         label.append(1)
#     if 100 <= row[0] < 200:
#         label.append(2)
#     if 200 <= row[0] < 300:
#         label.append(3)
#     if 300 <= row[0] < 400:
#         label.append(4)
#     if 400 <= row[0] < 500:
#         label.append(5)
#     if 500 <= row[0] < 600:
#         label.append(6)
#     if 600 <= row[0] < 700:
#         label.append(7)
#     if 700 <= row[0] < 800:
#         label.append(8)
#     if 800 <= row[0] < 900:
#         label.append(9)
#     if 900 <= row[0] < 1000:
#         label.append(10)
#     if 1000 <= row[0]:
#         label.append(11)
#     # ## scale 2^X *100
#     # if 0 <= row[0] < 200:
#     #     label.append('a)0-200')
#     # if 200 <= row[0] < 400:
#     #     label.append('b)200-400')
#     # if 400 <= row[0] < 800:
#     #     label.append('c)400-800')
#     # if 800 <= row[0] < 1600:
#     #     label.append('d)800-1600')
#     # if 1600 <= row[0] < 3200:
#     #     label.append('e)1600-3200')
#     # if 3200 <= row[0] < 6400:
#     #     label.append('f)3200-6400')
#     # if 6400 <= row[0]:
#     #     label.append('g)6400+')
#
# df1['label'] = label
# df1[df1.label == 'a)0-200'].count()[0]
# df1[df1.label == 'b)200-400'].count()[0]
# df1[df1.label == 'c)400-800'].count()[0]
# df1[df1.label == 'd)800-1600'].count()[0]
# df1[df1.label == 'e)1600-3200'].count()[0]
# df1[df1.label == 'f)3200-6400'].count()[0]
# df1[df1.label == 'g)6400+'].count()[0]
#
# ## Box plot
# df1.boxplot(column='bot_score', by='label')

# ## Scatter plot
# measure = 'bot_score'
# y = df[measure]
# x = df['twt']
#
# fig = plt.figure(); ax = fig.add_subplot(1, 1, 1)
#
# ax.scatter(x,y,marker='.',c=y)
# fig.show(ax)
# ax.set_xscale('log')
# ax.set_xlabel('No. of tweets posted')
# ax.set_ylabel('Bot probability')
# ax.set_title('No. of tweets vs Bot probability(%s)'%(measure))
# # print total bots identified
# print("%s = Bot/AllUsers : %d/%d"%(measure, count_bot(y),len(y)))
