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
rerun_mode = 2 # run from error? 0:No, 1:Unauthorized, 2:fromCursor
error_uid = 3367334171
# var for recovery from cursor
error_cursor = 1568733199122954827
error_page = 62
error_page -= 1

folder = "data//"
dataset = 0
mode = "follower" # friend / follower
userNwFilename = folder+"%d_%s_user_network.pkl"%(dataset,mode)
user_set = load_object(folder+'user_set.pkl')

authen_app = 1 # Default: app1 -  app1-5
twt = TweepyWrapper(authen_app) # Initial wrapper

logging.basicConfig(filename='%d_collectUsers.log'%dataset,level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

##############################################################################################################
# Main
##############################################################################################################

# # load list of valid users
# df_included_users = pd.DataFrame.from_csv("df_included_users.csv")

# ######################################################################################################################
# # Estimate request needed for limitation planing
# ######################################################################################################################
# # select users on the long tail
# topN = 1000
# topUsers = df_included_users.loc[0:topN-1]
# topUids = list(topUsers.uid.values)
# # loop getting users profiles
# userProfiles = []
# lim_per_req = 100
# i = 0
# while i < len(topUids):
#     collectingUids = topUids[i:i+lim_per_req-1]
#     userProfiles += twt._api.lookup_users(collectingUids)
#     i += lim_per_req
#     print(i)
#
# # check how many requests required to get all users networks
# lim_fri_per_req = 5000
# user_callneed = {}
# for user in userProfiles:
#     followers_call = math.ceil(user.followers_count/lim_fri_per_req)
#     friends_calls = math.ceil(user.friends_count/lim_fri_per_req)
#     user_callneed[user.id] = followers_call
# total_call = np.sum(list(user_callneed.values()))
# print("Total calls needed: %f"%(total_call))
# df_user_callneed = pd.DataFrame(list(user_callneed.items()), columns=['uid','call'])
# df_user_callneed = df_user_callneed.sort_values(['call'], ascending=False)
# df_user_callneed.head()
#
# # Split data
# num_set = 5
# chunk_size = math.ceil(total_call/num_set)
# user_set = []
# uids={}
# for idx, row in df_user_callneed.iterrows():
#     if np.sum(list(uids.values())) < chunk_size:
#         uids[row.uid] = row.call
#     else:
#         user_set.append(uids)
#         uids={}
# # update last user list
# user_set.append(uids)
#
# save_object(user_set, folder+'user_set.pkl')
#
# # # check user
# # twt._api.get_user(24067286).screen_name

######################################################################################################################
# Collect users
######################################################################################################################
### Config ##############################

##########################################

uid_list = list(user_set[dataset].keys())
processing_uids = uid_list
userNetworks = []

#** rerun mode
if rerun_mode != 0:
    # start user network from last error
    userNetworks = load_object(userNwFilename)
    # process from last error user onward
    processing_uids = uid_list[uid_list.index(error_uid):]

# index [n:] for rework on last index that got error
for uid in processing_uids:
    m = "Processing uid: %d"%uid
    print(m); logging.info(m)

    if mode == "follower":
        ## Get followers
        page_count = 0

        # ** support run from last error cursor
        if rerun_mode == 2:
            page_count = error_page
            followeres_list = load_object(folder + "followeres_list.pkl")
            cur_pages = tweepy.Cursor(twt._api.followers_ids, user_id=uid, cursor=error_cursor).pages()
        else:
            followeres_list = []
            cur_pages = tweepy.Cursor(twt._api.followers_ids, user_id=uid).pages()
        #

        try:
            for followers in cur_pages:
                page_count += 1
                # add to list
                followeres_list+=followers

                # if error, next run use cur_pages.next_cursor of the last round: cursor = cur_pages.next_cursor
                msg1 = 'Prev/Next: %s/%s' %(cur_pages.prev_cursor, cur_pages.next_cursor)
                msg2 = "last updated follower: " + str(followers[-1])
                msg3 = "processing page: " + str(page_count) + " with " + str(len(followers)) + " followers..."
                print(msg1); logging.info(msg1)
                print(msg2); logging.info(msg2)
                print(msg3); logging.info(msg3)
                twt.printQuotaFriend()

                # ** save followers list for error recovery
                save_object(followeres_list, folder+"followeres_list.pkl")
                # skip Not authorized error
        except Exception as e:
            if e.reason == 'Not authorized.':
                m = "uid: %s is Not authorized." % uid
                followeres_list = "Unauthorized"
                print(m);
                logging.info(m)
            else:
                raise

        #** set flag back to normal run
        rerun_mode = 0

        userNetworks.append(UserNetwork(uid, followers=followeres_list))
        save_object(userNetworks, userNwFilename)
        msg11 = "%d followers of user: %d have been added..."%(len(followeres_list), uid)
        print(msg11); logging.info(msg11)

    elif mode == "friend":
        ## Get friends
        page_count = 0

        # ** support run from last error
        if rerun_mode == 2:
            page_count = error_page
            friends_list = load_object(folder + "friends_list.pkl")
            cur_pages = tweepy.Cursor(twt._api.friends_ids, user_id=uid, cursor=1568733199122954827).pages()
        else:
            friends_list = []
            cur_pages = tweepy.Cursor(twt._api.friends_ids, user_id=uid).pages()
        #

        try:
            for friends in cur_pages:
                page_count += 1
                # add to list
                friends_list += friends

                # if error, next run use cur_pages.next_cursor of the last round: cursor = cur_pages.next_cursor
                msg1 = 'Prev/Next: %s/%s' % (cur_pages.prev_cursor, cur_pages.next_cursor)
                msg2 = "last updated friend: " + str(friends[-1])
                msg3 = "processing page: " + str(page_count) + " with " + str(len(friends)) + " friends..."
                print(msg1);
                logging.info(msg1)
                print(msg2);
                logging.info(msg2)
                print(msg3);
                logging.info(msg3)
                twt.printQuotaFriend()

                # ** save followers list for error recovery
                save_object(friends_list, folder+"friends_list.pkl")
        # skip Not authorized error
        except Exception as e:
            if e.reason == 'Not authorized.':
                m = "uid: %s is Not authorized." % uid
                friends_list = "Unauthorized"
                print(m);
                logging.info(m)
            else:
                raise

        #** set flag back to normal run
        rerun_mode = 0

        userNetworks.append(UserNetwork(uid, friends=friends_list))
        # ** Save
        save_object(userNetworks, userNwFilename)

        msg11 = "%d friends of user: %d have been added..."%(len(friends_list), uid)
        print(msg11); logging.info(msg11)

# userNetworks = load_object('4_user_network.pkl')