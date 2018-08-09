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

authen_app = 3 # Default: app1 -  app1-5
twt = TweepyWrapper(authen_app, pin=global_pin) # Initial wrapper

logging.basicConfig(filename='fix_missing_users.log',level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

def printlog(m):
    print(m); logging.info(m)

### error config: pick value from error #########
dict_set = 1
bot_list = []  #load_object("usertimeline//auu_bot_list.pkl")
dict_usertwt = dict() #load_object("usertimeline//dict_usertwt%d.pkl"%dict_set)
base_user_no_info = pd.DataFrame.from_csv("data//base_user_no_info.csv")

########################################################################################################################
# Get user Timeline
########################################################################################################################
if __name__ == "__main__":
    # ulist = base_user_no_info.uid.values.tolist()
    # unauthorised_users = []
    # count = 200
    # date_format = '%a %b %d %H:%M:%S %z %Y'
    # for uid in ulist:
    #     m = "Collecting twt of uid: %d .."%uid; print(m); logging.info(m)
    #
    #     is_bot = False
    #     all_tweets = []
    #     retweet_count = 0
    #     cur_pages = tweepy.Cursor(twt._api.user_timeline, user_id=uid, count=count, tweet_mode="extended").pages()
    #
    #     try:
    #         for tweets in cur_pages:
    #             ######################################################
    #             # Bot is..
    #             # 1. continuously active > 20 hours a day
    #             # 2. more than 80 post a day
    #             ######################################################
    #
    #             active_hours = []
    #             active_days =[]
    #             count_original_twt = 0 #num. tweet excluded RT
    #
    #             for t in tweets:
    #                 # # count active time to check bot
    #                 # active_hours.append(datetime.strptime(t._json['created_at'], date_format).hour)
    #                 # active_days.append(datetime.strptime(t._json['created_at'], date_format).date())
    #
    #                 # collect tweet info
    #                 twt_info = dict()
    #                 twt_info['id'] = t.id
    #                 twt_info['created_at'] = t.created_at
    #                 twt_info['lang'] = t.lang
    #                 twt_info['retweet_count'] = t.retweet_count
    #
    #                 if 'retweeted_status' in t._json:
    #                     twt_info['entities'] = t.retweeted_status.entities
    #                     twt_info['full_text'] = t.retweeted_status.full_text
    #                     twt_info['retweet_from_tid'] = t.retweeted_status.id  # exist only retweet status
    #                     twt_info['retweet_from_uid'] = t.retweeted_status.user.id  # exist only retweet status
    #                 else: # original as retweet field not exist
    #                     twt_info['entities'] = t.entities
    #                     twt_info['full_text'] = t.full_text
    #                     retweet_count += t.retweet_count #count how many time this users'post was retweeted
    #                     count_original_twt += 1 #count number of original tweets for bot checking
    #
    #                 # exist only replied status
    #                 if t.in_reply_to_status_id is not None:
    #                     twt_info['reply_tid'] = t.in_reply_to_status_id
    #                     twt_info['reply_uid'] = t.in_reply_to_user_id
    #
    #                 # collect tweet
    #                 all_tweets.append(twt_info)
    #
    #             # ### Checking bot
    #             # # Is it too active?
    #             # if isTooActive(active_hours, notLongerThanHr=20):
    #             #     is_bot = True
    #             #     printlog('uid: %d Too active!'%uid)
    #             #     break
    #             #
    #             # # Is it too often?
    #             # if isTooOften(active_days, tweet_count= count_original_twt, limitPerDay=80):
    #             #     is_bot = True
    #             #     printlog('uid: %d Tweet too often!'%uid)
    #             #     break
    #
    #             # log for recovery
    #             printlog("Collected tid: %d"%tweets[-1].id)
    #             printlog('Cursor maxid: %d' % (cur_pages.max_id))
    #
    #         # if not bot, add user with tweets to the dict
    #         if not is_bot:
    #             dict_usertwt[uid] = {'tweets': all_tweets, 'retweet_count': retweet_count}
    #             printlog("Added uid: %d with RT: %d | Twt: %d" %(uid, retweet_count,len(all_tweets)))
    #         else:
    #             bot_list.append(uid)
    #             printlog("uid: %d is Bot" % uid)
    #
    #     except Exception as e:
    #         ee=e
    #         if e.response.reason == 'Authorization Required':
    #             unauthorised_users.append(uid)
    #             printlog("uid: %s is Not authorized." % uid)
    #         else:
    #             raise
    #     #
    #     # # save objs
    #     # #every N users save dict as file set then clear mem
    #     # if len(dict_usertwt) < 500:
    #     #     save_object(dict_usertwt, "usertimeline//dict_usertwt%d.pkl" % dict_set)
    #     # else:
    #     #     save_object(dict_usertwt, "usertimeline//dict_usertwt%d.pkl" % dict_set)
    #     #     dict_usertwt=dict()
    #     #     dict_set += 1
    # save_object(dict_usertwt, "data//based_users_no_info_twt.pkl" )
    # # save_object(bot_list, "usertimeline//auu_bot_list.pkl")
    # printlog("save objs..")
    # #
    # # printlog("Done collect user timeline..")
    # pd.DataFrame({"uid":unauthorised_users}).to_csv("data//unauthorised_baseuser.csv")

    # # process each user
    # dict_usertwt = load_object("data//based_users_no_info_twt.pkl")
    # user_objs=dict()
    # for uid, twt_infos in dict_usertwt.items():
    #     printlog("Processing user: %d" % uid)
    #
    #     # var to keep hashtag count
    #     hashtag_count_dict = dict()
    #
    #     # read tweet from each user
    #     for tweet in twt_infos['tweets']:
    #         entities = tweet['entities']
    #         # distinct hashtag
    #         hashtag_in_tweet = set([tag['text'].lower() for tag in entities['hashtags']])
    #
    #         # count tag from all tweets of this user
    #         for tag in hashtag_in_tweet:
    #             hashtag_count_dict[tag] = hashtag_count_dict.get(tag, 0)+1
    #
    #     # assign user_objs
    #     user_objs[uid] = {'retweet_count': twt_infos['retweet_count'],
    #                       'hashtag_count': hashtag_count_dict,
    #                       'tweet_count': len(twt_infos['tweets'])}
    #
    #     printlog("Assigned user: %d" % uid)
    #
    # save_object(user_objs, "data//base_user_objs.pkl")

    ## #*test
    ##new_user_objs = dict()
    ## user_objs = load_object("data//base_user_objs.pkl")
    ## for uid, info in user_objs.items():
    ##     # transform tag to lower case and combine the count if duplicate
    ##     user_tag = dict()
    ##     for t, count in info['hashtag_count'].items():
    ##         lower_tag = t.lower()
    ##         user_tag[lower_tag] = user_tag.get(lower_tag, 0) + count
    ##
    ##     user_objs[uid]['hashtag_count'] = user_tag
    ## save_object(user_objs,"data//base_user_objs.pkl")

    # ==== build score

    # =============== Coin hashtag config =================
    coin_tag_list = pd.DataFrame.from_csv("C:\\Users\\Auu\\Desktop\\community_compare\\main\\uservector_hashtag_list.csv", header=0, index_col=None)
    dict_cointag_set = dict()

    print(coin_tag_list.shape)
    print(coin_tag_list.columns)
    for coin in coin_tag_list.columns:
        dict_cointag_set[coin] = set(coin_tag_list[coin].dropna())

    user_objs = load_object("data//base_user_objs.pkl")

    for uid, info in user_objs.items():
        # #* test
        # uid = 984047889159737344
        # info = user_objs[uid]

        printlog("Processing user: %d" % uid)

        # prepare user vectors
        interest_scores = dict()

        # get total hashtag to calculate user vector
        total_hashtag_used = sum(info['hashtag_count'].values())

        # **Fix - if total_hashtag == 0 then assign to 0 right away no need to process
        if total_hashtag_used > 0:
            # calculate user vector
            user_hashtag_set = set(info['hashtag_count'].keys())
            related_tag_count = 0
            for coin_name, coin_tag_set in dict_cointag_set.items():
                # find overlap coin hashtag in user's
                overlap_hashtag = user_hashtag_set.intersection(coin_tag_set)

                # count coin hashtag (from overlap)
                user_coin_tag_count = 0
                for ht in overlap_hashtag:
                    user_coin_tag_count += info['hashtag_count'][ht]

                # calculate interest score of this user to this coin: score = num_coin# / num_total#
                interest_scores[coin_name] = dict()
                interest_scores[coin_name]['prob'] = user_coin_tag_count / total_hashtag_used
                interest_scores[coin_name]['count'] = user_coin_tag_count
                related_tag_count += user_coin_tag_count

            # calculate score for other topics
            other_tag_count = total_hashtag_used - related_tag_count
            interest_scores['others'] = dict()
            interest_scores['others']['prob'] = other_tag_count / total_hashtag_used
            interest_scores['others']['count'] = other_tag_count
        else:
            # assign all to zero
            for coin_name, coin_tag_set in dict_cointag_set.items():
                interest_scores[coin_name] = dict()
                interest_scores[coin_name]['prob'] = 0
                interest_scores[coin_name]['count'] = 0

            # calculate score for other topics
            other_tag_count = 0
            interest_scores['others'] = dict()
            interest_scores['others']['prob'] = 0
            interest_scores['others']['count'] = 0

        # add score to user_objs
        user_objs[uid]['total_hashtag'] = total_hashtag_used
        user_objs[uid]['scores'] = interest_scores
        printlog("Done calculation user: %d" % uid)
    # save updated user_objs
    save_filename = "base_user_objs_score.pkl"
    save_object(user_objs, save_filename)
    printlog("Save: %s" % save_filename)

    #auu ==== user csv

    # ================== Config Build user_objs dataframe ==================================
    df_userinfo = pd.DataFrame.from_csv("C:\\Users\\Auu\\Desktop\\user_network\\data\\df_userinfo.csv")

    # define csv layout
    dict_user_objs = {'uid':[], 'screen_name':[], 'rt_count':[], 'lifetime_twt_count':[]
                    , 'friends_count':[], 'followers_count':[],'twt_count':[], 'hashtag_count':[],
                      # coin   _prob
                    'bitcoin': [],'ethereum': [],'ripple': [],'bitcoincash': [],
                    'eosio': [],'litecoin': [],'cardano': [],'stellar': [],'iota': [],
                    'tron': [],'neo': [],'monero': [],'dash': [],'nem': [],'tether': [],
                    'vechain': [],'ethereumclassic': [], 'bytecoin': [], 'binancecoin': [],
                      'qtum': [], 'zcash': [], 'icx': [], 'omisego': [], 'lisk': [], 'zilliqa': [],
                      'bitcoingold': [], 'aeternity': [], 'ontology': [], 'verge': [], 'steem': [],
                      '1_crypto_market_news': [], '2_crypto_buzz_ads': [], '3_general': [],
                      '4_bussiness_tech': [], '5_money_trading': [], 'others': [],
                      # coins_count_count
                      'bitcoin_count': [], 'ethereum_count': [], 'ripple_count': [], 'bitcoincash_count': [],
                      'eosio_count': [], 'litecoin_count': [], 'cardano_count': [], 'stellar_count': [],
                      'iota_count': [], 'tron_count': [], 'neo_count': [], 'monero_count': [], 'dash_count': [],
                      'nem_count': [], 'tether_count': [], 'vechain_count': [], 'ethereumclassic_count': [],
                      'bytecoin_count': [], 'binancecoin_count': [], 'qtum_count': [], 'zcash_count': [],
                      'icx_count': [], 'omisego_count': [],'lisk_count': [],'zilliqa_count': [],
                    'bitcoingold_count': [],'aeternity_count': [],'ontology_count': [],'verge_count': [],
                    'steem_count': [],'1_crypto_market_news_count': [],'2_crypto_buzz_ads_count': [],
                    '3_general_count': [],'4_bussiness_tech_count': [],'5_money_trading_count': [], 'others_count': []
                      }

    # process users from each file
    uc = 0
    uobjs = load_object("base_user_objs_score.pkl")
    for uid, info in uobjs.items():
        uc+=1
        # Assign scores
        for sname, score in info['scores'].items():
            dict_user_objs[sname].append(score['prob'])
            dict_user_objs[sname + '_count'].append(score['count'])

        # Assign user info from collected tweets
        dict_user_objs['uid'].append(str(uid))
        dict_user_objs['rt_count'].append(info['retweet_count'])
        dict_user_objs['twt_count'].append(info['tweet_count'])
        dict_user_objs['hashtag_count'].append(info['total_hashtag'])

        # Assign user info from user_info api - look up from df_userinfo.csv file
        userinfo = df_userinfo[df_userinfo['uid']==uid]
        if userinfo.shape[0] == 0:
            dict_user_objs['screen_name'].append(None)
            dict_user_objs['friends_count'].append(None)
            dict_user_objs['followers_count'].append(None)
            dict_user_objs['lifetime_twt_count'].append(None)
        else:
            dict_user_objs['screen_name'].append(userinfo.screen_name.values[0])
            dict_user_objs['friends_count'].append(userinfo.friends_count.values[0])
            dict_user_objs['followers_count'].append(userinfo.followers_count.values[0])
            dict_user_objs['lifetime_twt_count'].append(userinfo.statuses_count.values[0])

    # create dataframe from dict
    df_user_objs = pd.DataFrame(data=dict_user_objs)
    df_user_objs = df_user_objs[[   'uid', 'screen_name', 'rt_count', 'lifetime_twt_count', 'friends_count', 'followers_count','twt_count', 'hashtag_count',
                                    # coin   _prob
                                    'bitcoin','bitcoin_count',
                                    'ethereum','ethereum_count',
                                    'ripple','ripple_count',
                                    'bitcoincash','bitcoincash_count',
                                    'eosio','eosio_count',
                                    'litecoin','litecoin_count',
                                    'cardano','cardano_count',
                                    'stellar','stellar_count',
                                    'iota','iota_count',
                                    'tron','tron_count',
                                    'neo','neo_count',
                                    'monero','monero_count',
                                    'dash','dash_count',
                                    'nem','nem_count',
                                    'tether','tether_count',
                                    'vechain','vechain_count',
                                    'ethereumclassic','ethereumclassic_count',
                                    'bytecoin','bytecoin_count',
                                    'binancecoin','binancecoin_count',
                                    'qtum','qtum_count',
                                    'zcash','zcash_count',
                                    'icx','icx_count',
                                    'omisego','omisego_count',
                                    'lisk','lisk_count',
                                    'zilliqa','zilliqa_count',
                                    'bitcoingold','bitcoingold_count',
                                    'aeternity','aeternity_count',
                                    'ontology','ontology_count',
                                    'verge','verge_count',
                                    'steem','steem_count',
                                    '1_crypto_market_news','1_crypto_market_news_count',
                                    '2_crypto_buzz_ads','2_crypto_buzz_ads_count',
                                    '3_general','3_general_count',
                                    '4_bussiness_tech','4_bussiness_tech_count',
                                    '5_money_trading','5_money_trading_count',
                                    'others','others_count']]

    df_user_objs.to_csv("base_user_objs_score.csv", index_label=None)
    print("total users processed: %d"%uc)

    #*-- fix uid type exp
    save_object(df_user_objs,"base_user_objs_score.pkl")

if __name__ == "__getuserinfo__":
    user_no_info = [   7.68675E+17,
                            1385680262,
                            2410501247,
                            4037304203,
                            380984069,
                            429231819,
                            2190102376,
                            446012196,
                            2472671829,
                            718979694,
                            581270284,
                        ]
    # combine missing userinfo and the missing based_user
    # ulist = user_no_info
    # df_user_objs = pd.DataFrame.from_csv("base_user_objs_score.csv")
    df_user_objs = load_object("base_user_objs_score.pkl")
    # base_user_objs_missing = df_user_objs[df_user_objs.screen_name.isnull()]
    # ulist = base_user_objs_missing.uid.values.tolist()
    #
    # # might dup, so distinct it
    # ulist = set(ulist)
    #
    # missing_user_info = []
    # error_uids = []
    # totalloop = len(ulist)
    # print("total loop: %d"%totalloop)
    # for idx, uid in enumerate(ulist):
    #     print("progress: %d/%d" % (idx,totalloop))
    #     try:
    #         missing_user_info.append(twt._api.get_user(uid))
    #         printlog("Collected uid: %d"%uid)
    #     except:
    #         error_uids.append(uid)
    #         printlog("Added error uid: %d"%uid)
    #
    # print("valid users: %d" % len(missing_user_info))
    # print("error users: %d" % len(error_uids))
    #
    # dfu = {'uid':[], 'screen_name':[], 'lifetime_twt_count':[], 'friends_count':[], 'followers_count':[]}
    # for u in missing_user_info:
    #     dfu['uid'].append(u.id)
    #     dfu['screen_name'].append(u.screen_name)
    #     dfu['lifetime_twt_count'].append(u.statuses_count)
    #     dfu['friends_count'].append(u.friends_count)
    #     dfu['followers_count'].append(u.followers_count)
    # pd.DataFrame(dfu).to_csv('base_missing_user_info.csv')
    #
    # for uu in missing_user_info:
    #     # match_row = df_user_objs.loc[df_user_objs.uid == uu.id]
    #     idx = df_user_objs.loc[df_user_objs.uid == uu.id].index.values[0]
    #     df_user_objs.at[idx, 'screen_name'] = uu.screen_name
    #     df_user_objs.at[idx, 'lifetime_twt_count'] = uu.statuses_count
    #     df_user_objs.at[idx, 'friends_count'] = uu.friends_count
    #     df_user_objs.at[idx, 'followers_count'] = uu.followers_count
    #
    # df_user_objs.to_csv("new_info_missing_user.csv")
    # ##

    # *** Fill missing user info from the saved file
    dfu = pd.DataFrame.from_csv('base_missing_user_info.csv')
    for uu in dfu.iterrows():
        uu = uu[1]
        # match_row = df_user_objs.loc[df_user_objs.uid == uu.id]
        # idx = df_user_objs.loc[df_user_objs.uid == uu.uid].index.values[0]
        idx = df_user_objs.loc[df_user_objs.uid == str(uu.uid)].index.values[0]
        df_user_objs.at[idx, 'screen_name'] = uu.screen_name
        df_user_objs.at[idx, 'lifetime_twt_count'] = uu.lifetime_twt_count
        df_user_objs.at[idx, 'friends_count'] = uu.friends_count
        df_user_objs.at[idx, 'followers_count'] = uu.followers_count
    # make it string coz when write to csv number will be distorted from the auto exponent transformation
    df_user_objs.uid = ["_"+ii for ii in list(df_user_objs.uid)]
    df_user_objs.to_csv("complete_missing_user_objs.csv")

# # missing info users - keep it! please!
# uulist = [768674896729608192
# ,1385680262
# ,2410501247
# ,4037304203
# ,380984069
# ,429231819
# ,2190102376
# ,446012196
# ,2472671829
# ,718979694
# ,581270284
# ]
# aaaa = twt._api.lookup_users(uulist)
# for a in aaaa:
#     print("%s, %s, %s, %s, %s"%(a.id,a.screen_name,a.statuses_count,a.friends_count,a.followers_count))
#

