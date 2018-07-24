import collections as c
import numpy as np
import math
import pandas as pd
import tweepy
import json
import logging
import datetime
import pickle
import matplotlib.pyplot as plt
import numpy as np
import operator

def load_object(filename):
    with open(filename, 'rb') as input:
        obj = pickle.load(input)
    return obj

def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def unixtime_to_time(unixtime):
    return datetime.datetime.fromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S')

class UserNetwork():
    uid = ""
    friends = []
    followers = []

    def __init__(self, uid, friends=[], followers=[]):
        self.uid = uid
        self.friends = friends
        self.followers = followers


### Class tweepy wrapper
class TweepyWrapper():
    _consumer_key = ""
    _consumer_secret = ""
    _access_token = ""
    _access_token_secret = ""
    _myinfo =""
    _api = ""

    def __init__(self, authen):
        ### Setup authentication
        if authen == 1:
            ## App1
            self._consumer_key = 'l9BvOKjP2Xj48I5wlc7Uh8sVN'
            self._consumer_secret = 'HMKOvmuCaReDIzc0GlzfjQGKFrdCJ9jHlRJd8AAp0e7PHfwl6H'
            self._access_token = '982717247109189632-cdUZCv2mzMCDiPiHkdRDpUQXdRnFIvB'
            self._access_token_secret = 'AaayN6WOC3rPcYIoBg1Cc5uEPeUbcrw2jFHhhZVlHzjGC'
        elif authen == 2:
            ### App2
            self._consumer_key = 'L7IX0KwYgQUGeC1TqnxULue1v'
            self._consumer_secret = 'gRiqmdED0KFVjg6v2x9giQmctFLdAiFwEioCECuVCTJafp8byB'
            self._access_token = '982717247109189632-QRXdgrmZdhIy00do6D5o0wpdUMVKvJU'
            self._access_token_secret = 'szb7jQaVBe8JCf9iM23e3GBd7OgbuLRDxhTM6nU4L3QAp'
        elif authen == 3:
            ## App3
            self._consumer_key = 'w3TysRbh9H6oKp5T8qVNeSEdl'
            self._consumer_secret = 'LJA4sjmh4mq7OvmfUngVr7OX7rAnxeuUsKPT9rbzD9iU1sWfa3'
            self._access_token = '982717247109189632-rB4KizgqhsFdMS1V1Tu8qcPdxAe2dDi'
            self._access_token_secret = 'joe3MY7vIjWhDttHMMTJmgchzOLYUNqhjGUuWpAS4d3Ro'
        elif authen == 4:
            ### App4
            self._consumer_key = 'iQtb3NaOC6mMPXDHEuJC3Tk6O'
            self._consumer_secret = '3AEj5Tz5hivJCufhYeGKifvJOnTwgPjQkdflsPf3MkFi7l86NY'
            self._access_token = '982717247109189632-Nt2eDyzesz7z5RrFCZ6ThNulxFJcqY4'
            self._access_token_secret = '4hamnnQx4NfH229hIf08StHcxbgEHH6VKvmTiiKXcARAG'
        elif authen == 5:
            ## App5
            self._consumer_key = 'pQuxwVUnj9l533qkYMv2qoBn4'
            self._consumer_secret = 'P33GAjCp5mLbbJORjvgCpu7C1ILSKdPODJVapxSSjLvyeAOMic'
            self._access_token = '982717247109189632-A7CoO7YrEpsDcm6jprdf2wmvtCXyxbG'
            self._access_token_secret = 'TI2BpcBogcKjN1AMZWerZUeuhnsVMcAnmcrd5OjdIgVQM'
        else:  # app1 as default
            ## App1
            self._consumer_key = 'l9BvOKjP2Xj48I5wlc7Uh8sVN'
            self._consumer_secret = 'HMKOvmuCaReDIzc0GlzfjQGKFrdCJ9jHlRJd8AAp0e7PHfwl6H'
            self._access_token = '982717247109189632-cdUZCv2mzMCDiPiHkdRDpUQXdRnFIvB'
            self._access_token_secret = 'AaayN6WOC3rPcYIoBg1Cc5uEPeUbcrw2jFHhhZVlHzjGC'

        # Setup authentication objects
        __auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
        __auth.set_access_token(self._access_token, self._access_token_secret)
        self._api = tweepy.API(__auth,
                   # support for multiple authentication handlers
                   # retry 3 times with 5 seconds delay when getting these error codes
                   # For more details see
                   # https://dev.twitter.com/docs/error-codes-responses
                   retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503])
                    , wait_on_rate_limit=True, wait_on_rate_limit_notify=True
                   )
        self._myinfo = self._api.me()

    def sendTweet(self, text):
        # Update status
        self._api.update_status(status=text)

    def getUser(self, name):
        users = self._api.get_user(name)
        return users

    def search(self,keyword):
        tweets = self._api.search(q=keyword, tweet_mode='extended')
        for row in tweets:
            # textoutx.append(row.text)
            print(row.full_text)
        return tweets

    def getRateLimit(self):
        rate = self._api.rate_limit_status()
        print(rate['resources']['search'])

    def getTweetByUser(self,userName):
        tweets = self._api.user_timeline(userName)
        return tweets

    def getRetweetUsers(self,tweetId):
        users = self._api.retweets(tweetId)
        return users
    def getTweetById(self,tweetId):
        return self._api.get_status
    def printQuota(self):
        # Print remaining quota
        quota = twt._api.rate_limit_status('search')['resources']['search']
        callLeft = str(quota['/search/tweets']['remaining'])
        resetTime = datetime.datetime.fromtimestamp(quota['/search/tweets']['reset']).strftime('%Y-%m-%d %H:%M:%S')
        print("Quota (call/resetAt): " + callLeft + "/" + resetTime)

    def printQuotaFriend(self):
        # Print remaining quota
        quota = twt._api.rate_limit_status('followers')['resources']['followers']
        callLeft = str(quota['/followers/ids']['remaining'])
        resetTime = datetime.datetime.fromtimestamp(quota['/followers/ids']['reset']).strftime('%Y-%m-%d %H:%M:%S')
        print("Quota Followers/ids (call/resetAt): " + callLeft + "/" + resetTime)

        quota = twt._api.rate_limit_status('friends')['resources']['friends']
        callLeft = str(quota['/friends/ids']['remaining'])
        resetTime = datetime.datetime.fromtimestamp(quota['/friends/ids']['reset']).strftime('%Y-%m-%d %H:%M:%S')
        print("Quota Friends/ids (call/resetAt): " + callLeft + "/" + resetTime)

    def printQuota(self,name,resource):
        quotas = twt._api.rate_limit_status(name)['resources'][resource]
        for quota in quotas:
            callLeft = str(quota['remaining'])
            resetTime = datetime.datetime.fromtimestamp(quota['reset']).strftime('%Y-%m-%d %H:%M:%S')
            print("Quota (call/resetAt): " + callLeft + "/" + resetTime)

##############################################################
# Configuration
##############################################################
rerun_mode = 0 # run from error? 0:No, 1:Unauthorized, 2:fromCursor
error_uid = 0
# var for recovery from cursor
error_cursor = 0
error_page = 0

folder = "data//"
dataset = 1
mode = "follower" # friend / follower
userNwFilename = folder+"%d_%s_user_network.pkl"%(dataset,mode)
user_set = load_object(folder+'user_set.pkl')

authen_app = 2 # Default: app1 -  app1-5
twt = TweepyWrapper(authen_app) # Initial wrapper

logging.basicConfig(filename='%d_collectUsers.log'%dataset,level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

# ##############################
# col = ['uid', 'screen_name', 'followers_count', 'friends_count']
# df_userinfo = pd.DataFrame(columns=col)
# # test lookup_user
# users = twt._api.lookup_users(screen_names=['thanadonf','kinetiz10'])
# for u in users:
#     df = pd.DataFrame([[u.id, u.screen_name, u.followers_count, u.friends_count]], columns=col)
#     df_userinfo = df_userinfo.append(df,ignore_index=True)


### check number of friends
# - get list of friends and followers
# - check with existing user list ->" how many user we need to collect more?
# - estimate if its possible to collect all users

# file_list = [
#     "data//bkp//0_follower_user_network.pkl",
#     "data//bkp//0_friend_user_network.pkl",
#     "data//bkp//1_follower_user_network.pkl",
#     "data//bkp//1_friend_user_network.pkl",
#     "data//bkp//2_follower_user_network.pkl",
#     "data//bkp//2_friend_user_network.pkl",
#     "data//bkp//3_follower_user_network.pkl",
#     "data//bkp//3_friend_user_network.pkl",
#     "data//bkp//4_follower_user_network.pkl",
#     "data//bkp//4_friend_user_network.pkl",
#     "data//0_follower_user_network.pkl",
#     "data//0_friend_user_network.pkl",
#     "data//1_follower_user_network.pkl",
#     "data//1_friend_user_network.pkl",
#     "data//2_follower_user_network.pkl",
#     "data//2_friend_user_network.pkl",
#     "data//3_follower_user_network.pkl",
#     "data//3_friend_user_network.pkl",
#     ]
# ## combine users in a list
# user_nw = []
# for file in file_list:
#     nw = load_object(file)
#     user_nw+=nw
#
# len(user_nw)
# # save_object(user_nw,folder+"all_users.pkl")
#
#
# ## combine friends and followers to one objects
# combined_users = []
# processed_uidx = []
# for idx, u in enumerate(user_nw):
#     if idx not in processed_uidx:
#         for jdx, u_compare in enumerate(user_nw):
#             if idx != jdx and u.uid == u_compare.uid:
#                 # handle unauthorised users
#                 if u.followers == "Unauthorized": u.followers = []
#                 if u.friends == "Unauthorized": u.friends = []
#                 if u_compare.followers == "Unauthorized": u_compare.followers = []
#                 if u_compare.friends == "Unauthorized": u_compare.friends = []
#
#
#                 # combine to one object, using u as main
#                 u.followers = set(u.followers + u_compare.followers)
#                 u.friends = set(u.friends + u_compare.friends)
#                 combined_users.append(u)
#
#                 # add jdx in already processed user index list
#                 processed_uidx.append(jdx)
#                 break #end loop as there is only 2 users as a pair
#
# len(combined_users)
# save_object(combined_users, folder+"combined_users.pkl")


# # check if users in the list are unique
# uids = [u.uid for u in combined_users]
# len(set(uids))
#
# # check if friends/ followers in the list are not empty
# problem_users = []
# for u in combined_users:
#     if len(u.followers) == 0 or len(u.friends) == 0:
#         problem_users.append(u)
# print(problem_users)

# # find overlapped users in network
# # -> network of User A set(followers+friends) intersect with nw of UserB set(followers+friends)
# combined_users = load_object(folder+ "combined_users.pkl")
# overlap_users = []
# for idx, u in enumerate(combined_users):
#     uset_a = u.followers.union(u.friends)
#
#     next = idx+1
#     for jdx, u_compare in enumerate(combined_users[next:]):
#         uset_b = u_compare.followers.union(u_compare.friends)
#         uset_overlap = uset_a.intersection(uset_b)
#         # print(combined_users[next+jdx] == u_compare)
#
#         # if overlap add to the list and move to
#         if uset_overlap != set():
#             # remove from the set to avoid dup process in next round
#             combined_users[next + jdx].followers = u_compare.followers - uset_overlap
#             combined_users[next + jdx].friends = u_compare.friends - uset_overlap
#
#             overlap_users += list(uset_overlap)
#             print("overlap users added ...")
#
# save_object(overlap_users, folder+"overlap_users.pkl")
overlap_users = load_object(folder+"overlap_users.pkl")
print("unique users num. in network: %d"%len(set(overlap_users)))

## count how many a user links to the based users
# -> 1 means it link to at least 2 users
# -> 2 means linking to 3 users
overlap_counter = c.Counter(overlap_users)
links_to_base = 8
overlap_n_link_user = {k: v for k, v in overlap_counter.items() if v > links_to_base}
print(len(overlap_n_link_user))
save_object(overlap_n_link_user, folder+'overlap_8_link_user.pkl')


###################################################################################################################
# # keep based user for looping
# based_users = []
# for u in user_nw:
#     based_users.append(u.uid)
# based_users = set(based_users)
# len(based_users)
#
# # ## test
# # a=[]
# # l = 0
# # uset = load_object(folder+"old_user_set.pkl")
# # ulist = []
# # for i in range(5):
# #     l += len(uset[i])
# #     ulist+=uset[i].keys()
# # #user already processed
# # ulist
# #
# # #user not yet processed
# # not_proccessed_ulist = []
# # for uid in list(df_user_callneed.uid.values):
# #     if uid not in ulist:
# #         not_proccessed_ulist.append(uid)
# # not_proccessed_ulist
# #
# # len(not_proccessed_ulist)
# # len(ulist)
# #
# # not_proccessed_ulist
#
# ## check how many call needed for the list of users
# df_included_users = pd.DataFrame.from_csv("df_included_users.csv")
# all_ulist = list(df_included_users.uid.values)
# i = 0
# while i < len(all_ulist):
#     ulist = all_ulist[i:i+100]
#     uprof =  twt._api.lookup_users(ulist)
#     df = pd.DataFrame(columns= ['uid', 'call'])
#     callneeded = 0
#     for u in uprof:
#         print("followers:%s | friends:%s"%(u.followers_count,u.friends_count))
#         callneeded += u.followers_count/5000
#         df = df.append(pd.DataFrame([[u.id, callneeded]],columns=['uid','call']))
#     i = i+100
# print('done..')
#
# # Split data
# num_set = 5
# total_call = np.sum(list(df.call.values))
# chunk_size = math.ceil(total_call/num_set)
# user_set = []
# uids={}
# for idx, row in df.iterrows():
#     if np.sum(list(uids.values())) < chunk_size:
#         uids[row.uid] = row.call
#     else:
#         uids[row.uid] = row.call
#         user_set.append(uids)
#         uids={}
# # update last user list
# user_set.append(uids)
# aa = []
# for u in user_set:
#     aa+= u.keys()
# aa
# len(aa)
# user_set[3]
#
# save_object(user_set, folder+'leftover_user_set.pkl')
