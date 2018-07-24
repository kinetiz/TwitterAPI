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
    followings = []
    followers = []

    def __init__(self, uid, followings=[], followers=[]):
        self.uid = uid
        self.followings = followings
        self.followers = followers


### Class tweepy wrapper
class TweepyWrapper():
    _consumer_key = ""
    _consumer_secret = ""
    _access_token = ""
    _access_token_secret = ""
    _myinfo =""
    _api = ""

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._access_token = access_token
        self._access_token_secret = access_token_secret

        # Setup authentication objects
        __auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        __auth.set_access_token(access_token, access_token_secret)
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
### Setup logging
logging.basicConfig(filename='collectUsers.log',level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

### Select authen account
# Default: app1 -  1: app1, 2: app2, 3: app3
authen = 1

### Setup authentication
if authen == 1:
    ## App1
    __CONSUMER_KEY = 'l9BvOKjP2Xj48I5wlc7Uh8sVN'
    __CONSUMER_SECRET = 'HMKOvmuCaReDIzc0GlzfjQGKFrdCJ9jHlRJd8AAp0e7PHfwl6H'
    __ACCESS_TOKEN = '982717247109189632-cdUZCv2mzMCDiPiHkdRDpUQXdRnFIvB'
    __ACCESS_TOKEN_SECRET = 'AaayN6WOC3rPcYIoBg1Cc5uEPeUbcrw2jFHhhZVlHzjGC'
elif authen == 2:
    ### App2
    __CONSUMER_KEY = 'L7IX0KwYgQUGeC1TqnxULue1v'
    __CONSUMER_SECRET = 'gRiqmdED0KFVjg6v2x9giQmctFLdAiFwEioCECuVCTJafp8byB'
    __ACCESS_TOKEN = '982717247109189632-QRXdgrmZdhIy00do6D5o0wpdUMVKvJU'
    __ACCESS_TOKEN_SECRET = 'szb7jQaVBe8JCf9iM23e3GBd7OgbuLRDxhTM6nU4L3QAp'
elif authen == 3:
    ## App3
    __CONSUMER_KEY = 'w3TysRbh9H6oKp5T8qVNeSEdl'
    __CONSUMER_SECRET = 'LJA4sjmh4mq7OvmfUngVr7OX7rAnxeuUsKPT9rbzD9iU1sWfa3'
    __ACCESS_TOKEN = '982717247109189632-rB4KizgqhsFdMS1V1Tu8qcPdxAe2dDi'
    __ACCESS_TOKEN_SECRET = 'joe3MY7vIjWhDttHMMTJmgchzOLYUNqhjGUuWpAS4d3Ro'
elif authen == 4:
    ### App4
    __CONSUMER_KEY = 'iQtb3NaOC6mMPXDHEuJC3Tk6O'
    __CONSUMER_SECRET = '3AEj5Tz5hivJCufhYeGKifvJOnTwgPjQkdflsPf3MkFi7l86NY'
    __ACCESS_TOKEN = '982717247109189632-Nt2eDyzesz7z5RrFCZ6ThNulxFJcqY4'
    __ACCESS_TOKEN_SECRET = '4hamnnQx4NfH229hIf08StHcxbgEHH6VKvmTiiKXcARAG'
elif authen == 5:
    ## App5
    __CONSUMER_KEY = 'pQuxwVUnj9l533qkYMv2qoBn4'
    __CONSUMER_SECRET = 'P33GAjCp5mLbbJORjvgCpu7C1ILSKdPODJVapxSSjLvyeAOMic'
    __ACCESS_TOKEN = '982717247109189632-A7CoO7YrEpsDcm6jprdf2wmvtCXyxbG'
    __ACCESS_TOKEN_SECRET = 'TI2BpcBogcKjN1AMZWerZUeuhnsVMcAnmcrd5OjdIgVQM'
else: # app1 as default
    ## App1
    __CONSUMER_KEY = 'l9BvOKjP2Xj48I5wlc7Uh8sVN'
    __CONSUMER_SECRET = 'HMKOvmuCaReDIzc0GlzfjQGKFrdCJ9jHlRJd8AAp0e7PHfwl6H'
    __ACCESS_TOKEN = '982717247109189632-cdUZCv2mzMCDiPiHkdRDpUQXdRnFIvB'
    __ACCESS_TOKEN_SECRET = 'AaayN6WOC3rPcYIoBg1Cc5uEPeUbcrw2jFHhhZVlHzjGC'

### intial json file name
filename = 'users.json'

### save every N page
bulkSize = 50

### Define query
coinTags = {}
### 1
coinTags['bitcoin'] = "#bitcoin OR #btc"
####################################################################################################################


##############################################################################################################
# Main
##############################################################################################################
# Initial wrapper
twt = TweepyWrapper(__CONSUMER_KEY,__CONSUMER_SECRET,__ACCESS_TOKEN,__ACCESS_TOKEN_SECRET)

# load list of valid users
df_included_users = pd.DataFrame.from_csv("df_included_users.csv")

# select users on the long tail
topN = 1000
topUsers = df_included_users.loc[0:topN-1]
topUids = list(topUsers.uid.values)

######################################################################################################################
# Estimate request needed for limitation planing
######################################################################################################################

# loop getting users profiles
userProfiles = []
lim_per_req = 100
i = 0
while i < len(topUids):
    collectingUids = topUids[i:i+lim_per_req-1]
    userProfiles += twt._api.lookup_users(collectingUids)
    i += lim_per_req
    print(i)

# check how many requests required to get all users networks
lim_fri_per_req = 5000
user_callneed = {}
for user in userProfiles:
    followers_call = math.ceil(user.followers_count/lim_fri_per_req)
    friends_calls = math.ceil(user.friends_count/lim_fri_per_req)
    user_callneed[user.id] = followers_call
total_call = np.sum(list(user_callneed.values()))
print("Total calls needed: %f"%(total_call))
df_user_callneed = pd.DataFrame(list(user_callneed.items()), columns=['uid','call'])
df_user_callneed = df_user_callneed.sort_values(['call'], ascending=False)
df_user_callneed.head()

# Split data
num_set = 5
chunk_size = math.ceil(total_call/num_set)
user_set = []
uids={}
for idx, row in df_user_callneed.iterrows():
    if np.sum(list(uids.values())) < chunk_size:
        uids[row.uid] = row.call
    else:
        user_set.append(uids)
        uids={}
# update last user list
user_set.append(uids)

save_object(user_set, 'user//user_set.pkl')

# # check user
# twt._api.get_user(24067286).screen_name

######################################################################################################################
# Collect users
######################################################################################################################

user_set = load_object('user//user_set.pkl')
dataset = 0
uid_list = list(user_set[dataset].keys())
userNetworks = []
for uid in uid_list:
    m = "Processing uid: %d"%uid
    print(m); logging.info(m)

    ## Get followers
    page_count = 0
    followeres_list = []
    cur_pages = tweepy.Cursor(twt._api.followers_ids, user_id=uid).pages()
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

    userNetworks.append(UserNetwork(uid, followers=followeres_list))
    save_object(userNetworks)
    msg11 = "%d followers of user: %d have been added..."%(len(followeres_list), uid)
    print(msg11); logging.info(msg11)

    ## Get friends
    page_count = 0
    friends_list = []
    cur_pages = tweepy.Cursor(twt._api.friends_ids, user_id=uid).pages()
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

    userNetworks.append(UserNetwork(uid, friends=friends_list))
    save_object(userNetworks)
    msg11 = "%d friends of user: %d have been added..."%(len(friends_list), uid)
    print(msg11); logging.info(msg11)