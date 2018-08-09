from datetime import datetime
import numpy as np
import math
import pandas as pd
import tweepy
import json
import pickle
import numpy as np

ee=0

import logging
def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""

    formatter = logging.Formatter('%(asctime)s.%(msecs)03d : %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

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

    # print('activehours:%d'%max_count)
    if max_count > notLongerThanHr:
        return True
    else:
        return False

def isTooOften(active_dates, tweet_count, limitPerDay=80):
    # how many day?
    num_day = len(np.unique(active_dates))

    # avg tweets per day
    twt_per_day = tweet_count / num_day
    # print('twtperday:%s'%twt_per_day)
    if twt_per_day > limitPerDay:
        return True
    else:
        return False

thread=5
# def get_user_timeline(thread):
##############################################################
# Configuration
##############################################################

authen_app = thread # Default: app1 -  app1-5
twt = TweepyWrapper(authen_app) # Initial wrapper

# setup logfile according to thread
logger = setup_logger('t%d'%thread, 'thread_usertimeline//%d//%d_GetUserTimeline.log'%(thread,thread))
logger.info('from thread: %d'%thread)

def printlog(m):
    print(m)
    logger.info(m)

### error config: pick value from error #########

bot_list = load_object("thread_usertimeline//%d//%d_auu_bot_list.pkl"%(thread,thread))
dict_usertwt = dict() #load_object("usertimeline//dict_usertwt%d.pkl"%dict_set)
ulist = load_object('thread_usertimeline//overlap_8_link_user_set%d.pkl'%thread)

# if thread == 1:
#     from_uid = 940513566645293056  # change it
#     dict_set = 6
# elif thread == 2:
#     from_uid = 890941197451235329  # change it
#     dict_set = 14
# if thread == 3:
#     from_uid = 1129184342  # change it
#     dict_set = 52
if thread == 4:
    from_uid = 25624275  # change it
    dict_set = 40
elif thread == 5:
    from_uid = 704317326146084864  # change it
    dict_set = 43

ulist = ulist[ulist.index(from_uid)+1:]
###############################################################################################################

save_chunk = 50
count_user = 0
file_size = 200  # users per file
checkbot_limit = 2  # only first N time
date_format = '%a %b %d %H:%M:%S %z %Y'
for uid in ulist:
    printlog("T:%d|Collecting twt of uid: %d .." % (thread,uid))

    is_bot = False
    all_tweets = []
    retweet_count = 0
    checkbot_count = 0

    cur_pages = tweepy.Cursor(twt._api.user_timeline, user_id=uid, count=200, tweet_mode="extended").pages()
    try:
        for tweets in cur_pages:
            active_hours = []
            active_days = []
            count_original_twt = 0  # num. tweet excluded RT

            for t in tweets:
                ### Checking bot (only first round)
                if checkbot_count < checkbot_limit:
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
                    # twt_info['full_text'] = t.retweeted_status.full_text
                    twt_info['retweet_from_tid'] = t.retweeted_status.id  # exist only retweet status
                    twt_info['retweet_from_uid'] = t.retweeted_status.user.id  # exist only retweet status
                else:  # original as retweet field not exist
                    twt_info['entities'] = t.entities
                    # twt_info['full_text'] = t.full_text
                    retweet_count += t.retweet_count  # count how many time this users'post was retweeted
                    count_original_twt += 1  # count number of original tweets for bot checking

                # exist only replied status
                if t.in_reply_to_status_id is not None:
                    twt_info['reply_tid'] = t.in_reply_to_status_id
                    twt_info['reply_uid'] = t.in_reply_to_user_id

                # collect tweet
                all_tweets.append(twt_info)

            ### Checking bot (only first 2 round)
            if checkbot_count < checkbot_limit:
                ######################################################
                # Bot is..
                # 1. continuously active > 20 hours a day
                # 2. more than 80 post a day
                ######################################################
                # Is it too active?
                if isTooActive(active_hours, notLongerThanHr=20):
                    is_bot = True
                    printlog('uid: %d Too active!' % uid)
                    break

                # Is it too often?
                if isTooOften(active_days, tweet_count=count_original_twt, limitPerDay=80):
                    is_bot = True
                    printlog('uid: %d Tweet too often!' % uid)
                    break

                checkbot_count += 1  # count if checked

            ## log for recovery
            # printlog("Collected tid: %d"%tweets[-1].id)
            # printlog('Cursor maxid: %d' % (cur_pages.max_id))

        # if not bot, add user with tweets to the dict
        if not is_bot:
            dict_usertwt[uid] = {'tweets': all_tweets, 'retweet_count': retweet_count}
            count_user += 1
            print("T:%d|Ucount: %d" % (thread, count_user))
            # printlog("Added uid: %d with RT: %d | Twt: %d" %(uid, retweet_count,len(all_tweets)))
        else:
            bot_list.append(uid)
            printlog("uid: %d is Bot" % uid)

    except Exception as e:
        ee = e
        if e.response.reason == 'Authorization Required':
            printlog("uid: %s is Not authorized." % uid)
        else:
            raise

    # save objs
    if count_user % save_chunk == 0 and count_user != 0:
        save_object(dict_usertwt, "thread_usertimeline//%d//%d_dict_usertwt%d.pkl" % (thread, thread, dict_set))
        save_object(bot_list, "thread_usertimeline//%d//%d_auu_bot_list.pkl" % (thread, thread))
        printlog("save objs set%d|count user:%d|uid:%d" % (dict_set, count_user, uid))

        # every N users, clear mem and move to new file
        if count_user >= file_size:
            count_user = 0  # reset count user
            dict_usertwt = dict()  # rest - new dict
            dict_set += 1

# save when all users processed
save_object(dict_usertwt, "thread_usertimeline//%d//%d_dict_usertwt%d.pkl" % (thread, thread, dict_set))
save_object(bot_list, "thread_usertimeline//%d//%d_auu_bot_list.pkl" % (thread, thread))
printlog("save objs set%d|count user:%d|uid:%d" % (dict_set, count_user, uid))
printlog("Done collect user timeline thread: %d.." % thread)

#
# from multiprocessing.dummy import Pool as ThreadPool
#
# # make the Pool of workers
# pool = ThreadPool(1)
#
# # results = pool.starmap(function, zip(list_a, list_b))
# # threads = [1, 2, 3, 4, 5]
# threads = [5]
# pool.map(get_user_timeline, threads)
#
# # close the pool and wait for the work to finish
# pool.close()
# pool.join()












# ########################################################################
# # adhoc 22/07/2018: remove tweets fields from dict_user_twt object as its too big
# ########################################################################
# t=4
# ulist = load_object('usertimeline//overlap_8_link_user_set%d.pkl'%t)
# # ulist.index(920861740862021632)
# # len(ulist)
# # ulist = ulist[ulist.index(920861740862021632):]
# i=0
# withTwt = load_object('thread_usertimeline//bkp//%d_dict_usertwt1.pkl'%t)
# for uid, info in withTwt.items():
#     for item in info['tweets']:
#         del item['full_text']
#     i+=1
#     print(i)
#
# save_object(withTwt,'thread_usertimeline//reduce//%d_dict_usertwt1.pkl'%t)

# #check if users already collected
# t=5
# withTwt = load_object('thread_usertimeline//%d//%d_dict_usertwt2.pkl'%(t,t))
# 2416374152 in withTwt

# # check howm many bot detected
# bb = load_object("G:\\work\\TwitterAPI\\CollectUser\\thread_usertimeline\\5\\5_auu_bot_list.pkl")
# len(bb)
len(bot_list)