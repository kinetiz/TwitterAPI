from datetime import datetime
import numpy as np
import math
import pandas as pd
import tweepy
import json
import logging
import pickle
import matplotlib.pyplot as plt
import numpy as np
import operator
ee=0
# auth = tweepy.OAuthHandler('l9BvOKjP2Xj48I5wlc7Uh8sVN', 'HMKOvmuCaReDIzc0GlzfjQGKFrdCJ9jHlRJd8AAp0e7PHfwl6H'); auth.secure = True; auth.get_authorization_url()
#
#

global_pin = 'app'
# global_pin = '5257527'

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

    def __init__(self, authen=1, pin='app'):
        ### Setup authentication
        if authen == 1:
            ## App1
            self._consumer_key = 'zir1nLr04snX8BHPfMERQfCx3'
            self._consumer_secret = 'jWLq4JQvhzACSwMbce3nlXc36AjmTuM2t57nsIkzhfmI7ypdjc'
            self._access_token = '982717247109189632-4BIILPdon3xG9l2OfdLEEC1ZUzfiurI'
            self._access_token_secret = '5tfTBeRxyJ8RuDynOCBTE1eKiE7HCDTeVn0stUUAfEVmP'
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

        # App authen - Setup authentication objects
        __auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
        __auth.set_access_token(self._access_token, self._access_token_secret)

        # User authen
        if pin != 'app':
            # authUrl = __auth.get_authorization_url()
            tokens = __auth.get_access_token(verifier=pin)
            __auth.set_access_token(tokens[0], tokens[1])

        self._api = tweepy.API(__auth,
                   # support for multiple authentication handlers
                   # retry 3 times with 5 seconds delay when getting these error codes
                   # For more details see
                   # https://dev.twitter.com/docs/error-codes-responses
                   retry_count=3, retry_delay=5, retry_errors=set([404, 500, 503])
                    , wait_on_rate_limit=True, wait_on_rate_limit_notify=True
                   )
        self._myinfo = self._api.me()

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

def isTooActive(active_hour_list, notLongerThanHr=20):
    # unique and sort
    active_hour_list = sorted(list(set(active_hour_list)))

    count = 1 # [1-24]
    max_count = 0
    for idx, hr in enumerate(active_hour_list):
        if idx < len(active_hour_list)-1: # prevent index out of range
            if active_hour_list[idx+1] - active_hour_list[idx] == 1: #if next hr continue, +1
                count +=1
            else:
                count = 1 #reset

            if count > max_count: max_count = count

    print('activehours:%d'%max_count)
    if max_count > notLongerThanHr:
        return True
    else:
        return False

def isTooOften(active_dates, tweet_count, limitPerDay=80):
    # how many day?
    num_day = len(np.unique(active_dates))

    # avg tweets per day
    twt_per_day = tweet_count / num_day
    print('twtperday:%s'%twt_per_day)
    if twt_per_day > limitPerDay:
        return True
    else:
        return False
##############################################################
# Configuration
##############################################################

authen_app = 1 # Default: app1 -  app1-5
twt = TweepyWrapper(authen_app, pin=global_pin) # Initial wrapper

logging.basicConfig(filename='GetUserTimeline.log',level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

def printlog(m):
    print(m); logging.info(m)

### error config: pick value from error #########
dict_set = 1
bot_list = []  #load_object("usertimeline//auu_bot_list.pkl")
dict_usertwt = dict() #load_object("usertimeline//dict_usertwt%d.pkl"%dict_set)
ulist = load_object('usertimeline//overlap_8_link_user_set1.pkl')
# from_uid = 948317654150012929 #change it
# ulist = ulist[ulist.index(from_uid):]

########################################################################################################################
# Get user Timeline
########################################################################################################################
# # split data to 5 sets
# ulist = list(load_object('usertimeline//overlap_8_link_user.pkl').keys())
# size = 13304
# set1,set2,set3,set4,set5 = ulist[0:size], ulist[size:size*2], ulist[size*2:size*3], ulist[size*3:size*4], ulist[size*4:size*5]
# save_object(set1, 'usertimeline//overlap_8_link_user_set1.pkl')
# save_object(set2, 'usertimeline//overlap_8_link_user_set2.pkl')
# save_object(set3, 'usertimeline//overlap_8_link_user_set3.pkl')
# save_object(set4, 'usertimeline//overlap_8_link_user_set4.pkl')
# save_object(set5, 'usertimeline//overlap_8_link_user_set5.pkl')


# #test
# a = twt._api.user_timeline(screen_name='kinetiz10', count=200)
# new_tweets = twt._api.user_timeline(screen_name='kinetiz10', count=200, tweet_mode="extended")
# t = new_tweets[2]

count = 200
date_format = '%a %b %d %H:%M:%S %z %Y'
for uid in ulist:
    m = "Collecting twt of uid: %d .."%uid; print(m); logging.info(m)

    is_bot = False
    all_tweets = []
    retweet_count = 0
    cur_pages = tweepy.Cursor(twt._api.user_timeline, user_id=uid, count=count, tweet_mode="extended").pages()

    try:
        for tweets in cur_pages:
            ######################################################
            # Bot is..
            # 1. continuously active > 20 hours a day
            # 2. more than 80 post a day
            ######################################################

            active_hours = []
            active_days =[]
            count_original_twt = 0 #num. tweet excluded RT

            for t in tweets:
                # count active time to check bot
                active_hours.append(datetime.strptime(t._json['created_at'], date_format).hour)
                active_days.append(datetime.strptime(t._json['created_at'], date_format).date())

                # collect tweet info
                twt_info = dict()
                twt_info['id'] = t.id
                twt_info['created_at'] = t.created_at
                twt_info['lang'] = t.lang
                twt_info['retweet_count'] = t.retweet_count

                if 'retweeted_status' in t._json:
                    twt_info['entities'] = t.retweeted_status.entities
                    twt_info['full_text'] = t.retweeted_status.full_text
                    twt_info['retweet_from_tid'] = t.retweeted_status.id  # exist only retweet status
                    twt_info['retweet_from_uid'] = t.retweeted_status.user.id  # exist only retweet status
                else: # original as retweet field not exist
                    twt_info['entities'] = t.entities
                    twt_info['full_text'] = t.full_text
                    retweet_count += t.retweet_count #count how many time this users'post was retweeted
                    count_original_twt += 1 #count number of original tweets for bot checking

                # exist only replied status
                if t.in_reply_to_status_id is not None:
                    twt_info['reply_tid'] = t.in_reply_to_status_id
                    twt_info['reply_uid'] = t.in_reply_to_user_id

                # collect tweet
                all_tweets.append(twt_info)

            ### Checking bot
            # Is it too active?
            if isTooActive(active_hours, notLongerThanHr=20):
                is_bot = True
                printlog('uid: %d Too active!'%uid)
                break

            # Is it too often?
            if isTooOften(active_days, tweet_count= count_original_twt, limitPerDay=80):
                is_bot = True
                printlog('uid: %d Tweet too often!'%uid)
                break

            # log for recovery
            printlog("Collected tid: %d"%tweets[-1].id)
            printlog('Cursor maxid: %d' % (cur_pages.max_id))

        # if not bot, add user with tweets to the dict
        if not is_bot:
            dict_usertwt[uid] = {'tweets': all_tweets, 'retweet_count': retweet_count}
            printlog("Added uid: %d with RT: %d | Twt: %d" %(uid, retweet_count,len(all_tweets)))
        else:
            bot_list.append(uid)
            printlog("uid: %d is Bot" % uid)

    except Exception as e:
        ee=e
        if e.response.reason == 'Authorization Required':
            printlog("uid: %s is Not authorized." % uid)
        else:
            raise

    # save objs
    #every N users save dict as file set then clear mem
    if len(dict_usertwt) < 500:
        save_object(dict_usertwt, "usertimeline//dict_usertwt%d.pkl" % dict_set)
    else:
        save_object(dict_usertwt, "usertimeline//dict_usertwt%d.pkl" % dict_set)
        dict_usertwt=dict()
        dict_set += 1

    save_object(bot_list, "usertimeline//auu_bot_list.pkl")
    printlog("save objs..")

printlog("Done collect user timeline..")
