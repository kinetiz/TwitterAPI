
from itertools import repeat
import sys
import time
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

    def __init__(self, authen):
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
        elif authen == 6:
            ## App5
            self._consumer_key = 'HEno0nyL1TOYBaclXGkjsC1Ex'
            self._consumer_secret = 'iDVdnCH2vbEanTBbr6f9dWpNQ4lwsstBobRGzw6dvAoRUb2QeL'
            self._access_token = '982717247109189632-FDKLiX19tQMrnfY9S55f5puRTWv6C9J'
            self._access_token_secret = 'fdekClsfrvrnGUMUDO8CUUzgI4tDJDyZrPERmL3iHKJX9'
        elif authen == 7:
            ## App5
            self._consumer_key = 'vTK9HgQP7cVS4GoQ0HXDVTXqd'
            self._consumer_secret = 'Umoiq7MpNuABLCp7ae4MgZ8Ci3D0kVTRS0rNYLCANnFCzugpWV'
            self._access_token = '982717247109189632-yJUhNGzMQcZ7yZbOmfWMMALiiIhRQ0h'
            self._access_token_secret = 'EdCoE9oJI1TCHNXujBT6bcUeoTXY4wxFstgW2dx0ksz15'
        elif authen == 8:
            ## App5
            self._consumer_key = 'M6Lzjh94BRBgBLUBdK25dcf3S'
            self._consumer_secret = 'qppEr9SvJgQKPf2wxU0VDxt5fa0o5mV19iBg5jOOBP7zPNYWxA'
            self._access_token = '982717247109189632-AWCE4UdvXMXfLxEqQDbiYstD1lM3qtL'
            self._access_token_secret = 'dDz8VQnBOjBQ4MpmIMlOr7eN6QP8yhw5AdBCNjcIvfYpB'
        # elif authen == 9:
        #     ## App5
        #     self._consumer_key = 'HEno0nyL1TOYBaclXGkjsC1Ex'
        #     self._consumer_secret = 'iDVdnCH2vbEanTBbr6f9dWpNQ4lwsstBobRGzw6dvAoRUb2QeL'
        #     self._access_token = '982717247109189632-FDKLiX19tQMrnfY9S55f5puRTWv6C9J'
        #     self._access_token_secret = 'fdekClsfrvrnGUMUDO8CUUzgI4tDJDyZrPERmL3iHKJX9'
        # elif authen == 10:
        #     ## App5
        #     self._consumer_key = 'HEno0nyL1TOYBaclXGkjsC1Ex'
        #     self._consumer_secret = 'iDVdnCH2vbEanTBbr6f9dWpNQ4lwsstBobRGzw6dvAoRUb2QeL'
        #     self._access_token = '982717247109189632-FDKLiX19tQMrnfY9S55f5puRTWv6C9J'
        #     self._access_token_secret = 'fdekClsfrvrnGUMUDO8CUUzgI4tDJDyZrPERmL3iHKJX9'
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
        quota = self._api.rate_limit_status('search')['resources']['search']
        callLeft = str(quota['/search/tweets']['remaining'])
        resetTime = datetime.datetime.fromtimestamp(quota['/search/tweets']['reset']).strftime('%Y-%m-%d %H:%M:%S')
        print("Quota (call/resetAt): " + callLeft + "/" + resetTime)

    def printQuotaFriend(self):
        # Print remaining quota
        quota = self._api.rate_limit_status('followers')['resources']['followers']
        callLeft = str(quota['/followers/ids']['remaining'])
        resetTime = datetime.datetime.fromtimestamp(quota['/followers/ids']['reset']).strftime('%Y-%m-%d %H:%M:%S')
        print("Quota Followers/ids (call/resetAt): " + callLeft + "/" + resetTime)

        quota = self._api.rate_limit_status('friends')['resources']['friends']
        callLeft = str(quota['/friends/ids']['remaining'])
        resetTime = datetime.datetime.fromtimestamp(quota['/friends/ids']['reset']).strftime('%Y-%m-%d %H:%M:%S')
        print("Quota Friends/ids (call/resetAt): " + callLeft + "/" + resetTime)

    def printQuota(self,name,resource):
        quotas = self._api.rate_limit_status(name)['resources'][resource]
        for quota in quotas:
            callLeft = str(quota['remaining'])
            resetTime = datetime.datetime.fromtimestamp(quota['reset']).strftime('%Y-%m-%d %H:%M:%S')
            print("Quota (call/resetAt): " + callLeft + "/" + resetTime)


def collect_users(thread, mode, rerun_mode = 0, error_uid = 0, error_cursor = 0, error_page = 0):
    ##############################################################
    # Configuration
    ##############################################################

    # rerun_mode = 0 # run from error? 0:No, 1:Unauthorized, 2:fromCursor
    # error_uid = 25965585
    # # var for recovery from cursor
    # error_cursor = 1553447401708251160
    # error_page = 40
    # error_page -= 1
    all_collecting_uid = load_object('data//all_collecting_uid.pkl')
    filtereduid_and_baseuser_set = set(load_object('data//filtereduid_and_baseuser.pkl'))

    ## prepare user files
    # all_collecting_uid = pd.DataFrame.from_csv('data//filtered_uid.csv', index_col=None)
    # all_collecting_uid = all_collecting_uid.uid.values.tolist()
    # base_users = load_object('data//base_users.pkl')
    # wanted_uid_set = set(all_collecting_uid+base_users)
    # collecting = set(all_collecting_uid)-set(base_users)
    # save_object(collecting, 'all_collecting_uid.pkl')
    # len(collecting )
    # save_object(list(wanted_uid_set), 'filtereduid_and_baseuser.pkl')
    # ii = ['_'+str(i) for i in wanted_uid_set]
    # pd.DataFrame({'uid':ii}).to_csv('filtereduid_and_baseuser.csv',index=False)
    if mode == "friend": wait = 140
    else: wait = 0

    if thread == 1:
        authen_app = 1  # change it
        dataset = 1
        uid_list = all_collecting_uid[6500:6700]
        time.sleep(wait)
    elif thread == 2:
        authen_app = 2  # change it
        dataset = 2
        uid_list = all_collecting_uid[6700:6900]
        time.sleep(20+wait)
    elif thread == 3:
        authen_app = 3  # change it
        dataset = 3
        uid_list = all_collecting_uid[6900:7100]
        time.sleep(40+wait)
    elif thread == 4:
        authen_app = 4  # change it
        dataset = 4
        uid_list = all_collecting_uid[7100:7300]
        time.sleep(60+wait)
    elif thread == 5:
        authen_app = 5  # change it
        dataset = 5
        uid_list = all_collecting_uid[7300:7500]
        time.sleep(80+wait)
    elif thread == 6:
        authen_app = 6  # change it
        dataset = 6
        uid_list = all_collecting_uid[7500:7700]
        time.sleep(100+wait)
    elif thread == 7:
        authen_app = 7  # change it
        dataset = 7
        uid_list = all_collecting_uid[7700:7900]
        time.sleep(120+wait)
    elif thread == 8:
        authen_app = 8  # change it
        dataset = 8
        uid_list = all_collecting_uid[7900:]
        time.sleep(140+wait)

    print('thread:%s|mode:%s|rerunmode:%s|erroruid:%s'%(thread,mode,rerun_mode,error_uid))
    folder = "thread_collect_user//%d//"%(thread)
    # mode = "follower" # friend / follower
    userNwFilename = folder + "%d_%s_user_network.pkl" % (dataset, mode)
    red_userNwFilename = folder + "%d_%s_red_user_network.pkl" % (dataset, mode)
    # user_set = load_object(folder + 'user_set.pkl')

    processing_uids = uid_list
    userNetworks = []
    red_userNetworks = []
    unauthorised_users = []
    notfound_users = []

    twt = TweepyWrapper(authen_app) # Initial wrapper
    # logging.basicConfig(filename='%d_collectUsers.log'%dataset,level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")


    # setup logfile according to thread
    logger = setup_logger('t%d'%thread, 'thread_collect_user//%d//%d_%s_collect_user.log'%(thread,thread,mode))
    logger.info('from thread: %d'%thread)

    def printlog(m, t=thread):
        print( '%s_%s'%(t,m))
        logger.info('%s_%s'%(t,m))

    ##############################################################################################################
    # Main
    ##############################################################################################################

    # # # load list of valid users
    # df_included_users = pd.DataFrame.from_csv(folder+"df_included_users.csv")

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
    #     collectingUids = topUids[i:i+lim_per_req]
    #     userProfiles += twt._api.lookup_users(collectingUids)
    #     i += lim_per_req
    #     print("%d : %d"%(len(collectingUids),len(userProfiles)))
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
    #         uids[row.uid] = row.call
    #         user_set.append(uids)
    #         uids={}
    # # update last user list
    # user_set.append(uids)
    #
    # save_object(user_set, folder+'user_set.pkl')
    #
    # # # check user
    # # twt._api.get_user(24067286).screen_name

    #** rerun mode
    if rerun_mode != 0:
        # start user network from last error
        userNetworks = load_object(userNwFilename)
        # process from last error user onward
        processing_uids = uid_list[uid_list.index(error_uid):]

    # index [n:] for rework on last index that got error
    for uid in processing_uids:
        printlog("Processing uid: %d"%uid)

        authorised_error = False

        if mode == "follower":
            ## Get followers
            page_count = 0

            # ** support run from last error cursor
            if rerun_mode == 2:
                page_count = error_page
                followeres_list = load_object(folder + "followeres_list.pkl")
                red_followeres_set = load_object(folder + "red_followeres_set.pkl")
                cur_pages = tweepy.Cursor(twt._api.followers_ids, user_id=uid, cursor=error_cursor).pages()
            else:
                followeres_list = []
                red_followeres_set = set()
                cur_pages = tweepy.Cursor(twt._api.followers_ids, user_id=uid).pages()
            #

            try:
                for followers in cur_pages:
                    page_count += 1
                    # add to list
                    followeres_list+=followers
                    red_followeres_set = red_followeres_set.union(filtereduid_and_baseuser_set.intersection(set(followers)))
                    # if error, next run use cur_pages.next_cursor of the last round: cursor = cur_pages.next_cursor
                    msg1 = 'Prev/Next: %s/%s' %(cur_pages.prev_cursor, cur_pages.next_cursor)
                    msg2 = "last updated follower: " + str(followers[-1])
                    msg3 = "processing page: " + str(page_count) + " with " + str(len(followers)) + " followers..."
                    printlog(msg1)
                    printlog(msg2)
                    printlog(msg3)
                    twt.printQuotaFriend()

                    # ** save followers list for error recovery
                    save_object(followeres_list, folder+"followeres_list.pkl")
                    save_object(red_followeres_set, folder+"red_followeres_set.pkl")
                    # skip Not authorized error
            except Exception as e:
                if e.reason == 'Not authorized.':
                    m = "uid: %s is Not authorized." % uid
                    followeres_list = "Unauthorized"
                    printlog(m)
                    authorised_error = True
                    unauthorised_users.append(uid)

                elif e.reason == "[{'code': 34, 'message': 'Sorry, that page does not exist.'}]":
                    printlog('uid:%s is not found' % uid)
                    notfound_users.append(uid)
                else:
                    raise

            #** set flag back to normal run
            rerun_mode = 0

            if not authorised_error:
                userNetworks.append(UserNetwork(uid, followers=followeres_list))
                save_object(userNetworks, userNwFilename)

                red_userNetworks.append(UserNetwork(uid, followers=list(red_followeres_set)))
                save_object(red_userNetworks, red_userNwFilename)
                msg11 = "%d followers of user: %d have been added..."%(len(followeres_list), uid)
                printlog(msg11)
            save_object(unauthorised_users, folder + "%s_unauthorised_users.pkl"%(mode))
            save_object(notfound_users, folder + "%s_notfound_users.pkl"%(mode))


        elif mode == "friend":
            ## Get friends
            page_count = 0

            # ** support run from last error
            if rerun_mode == 2:
                page_count = error_page
                friends_list = load_object(folder + "friends_list.pkl")
                red_friends_set = load_object(folder + "red_friends_set.pkl")
                cur_pages = tweepy.Cursor(twt._api.friends_ids, user_id=uid, cursor=1568733199122954827).pages()
            else:
                friends_list = []
                red_friends_set = set()
                cur_pages = tweepy.Cursor(twt._api.friends_ids, user_id=uid).pages()
            #

            try:
                for friends in cur_pages:
                    page_count += 1
                    # add to list
                    friends_list += friends
                    red_friends_set = red_friends_set.union(filtereduid_and_baseuser_set.intersection(set(friends)))
                    # if error, next run use cur_pages.next_cursor of the last round: cursor = cur_pages.next_cursor
                    msg1 = 'Prev/Next: %s/%s' % (cur_pages.prev_cursor, cur_pages.next_cursor)
                    msg2 = "last updated friend: " + str(friends[-1])
                    msg3 = "processing page: " + str(page_count) + " with " + str(len(friends)) + " friends..."
                    printlog(msg1)
                    printlog(msg2)
                    printlog(msg3)
                    twt.printQuotaFriend()

                    # ** save followers list for error recovery
                    save_object(friends_list, folder+"friends_list.pkl")
                    save_object(red_friends_set, folder + "red_friends_set.pkl")
            # skip Not authorized error
            except Exception as e:
                if e.reason == 'Not authorized.':
                    m = "uid: %s is Not authorized." % uid
                    friends_list = "Unauthorized"
                    printlog(m)
                    authorised_error = True
                    unauthorised_users.append(uid)
                elif e.reason == "[{'code': 34, 'message': 'Sorry, that page does not exist.'}]":
                    printlog('uid:%s is not found' % uid)
                    notfound_users.append(uid)
                else:
                    printlog(e)
                    raise

            #** set flag back to normal run
            rerun_mode = 0

            if not authorised_error:
                userNetworks.append(UserNetwork(uid, friends=friends_list))
                save_object(userNetworks, userNwFilename)

                red_userNetworks.append(UserNetwork(uid, friends=list(red_friends_set)))
                save_object(red_userNetworks, red_userNwFilename)

                msg11 = "%d friends of user: %d have been added..."%(len(friends_list), uid)
                printlog(msg11)
            save_object(unauthorised_users, folder+"%s_unauthorised_users.pkl"%(mode))
            save_object(notfound_users, folder+"%s_notfound_users.pkl"%(mode))
    printlog("all done..")
    # userNetworks = load_object('4_user_network.pkl')

    # ## test
    # a=[]
    # l = 0
    # uset = load_object(folder+"old_user_set.pkl")
    # ulist = []
    # for i in range(5):
    #     l += len(uset[i])
    #     ulist+=uset[i].keys()
    # #user already processed
    # ulist
    #
    # #user not yet processed
    # not_proccessed_ulist = []
    # for uid in list(df_user_callneed.uid.values):
    #     if uid not in ulist:
    #         not_proccessed_ulist.append(uid)
    # not_proccessed_ulist
    #
    # len(not_proccessed_ulist)
    # len(ulist)
    #
    # not_proccessed_ulist
    #
    # uprof =  twt._api.lookup_users(not_proccessed_ulist)
    # df = pd.DataFrame(columns= ['uid', 'call'])
    # callneeded = 0
    # for u in uprof:
    #     print("followers:%s | friends:%s"%(u.followers_count,u.friends_count))
    #     callneeded += u.followers_count/5000
    #     df = df.append(pd.DataFrame([[u.id, callneeded]],columns=['uid','call']))
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

    # a = twt._api.friends_ids(900521261842825216)
    # len(a)


if __name__ == "__main__":

    from multiprocessing.dummy import Pool as ThreadPool


    # make the Pool of workers
    pool = ThreadPool(8)

    # results = pool.starmap(function, zip(list_a, list_b))
    threads = [1, 2, 3, 4, 5,6,7,8]
    # modes = [ "follower", "follower", "follower", "follower", "follower"]
    modes = sys.argv[1]
    rerunmodes = [0,0,0,0,0,0,0,0]
    # if modes == 'follower':
    #     erroruids = [730662056,2799211554,977278817889812480,230144987,989544343626244097,0,0,0]
    # elif modes == 'friend':
    #     erroruids = [730662056,4746613774,874142510267936768,820374121116827649,977842653353140224,0,0,0]
    print(modes)

    # pool.map(collect_users, threads)
    pool.starmap(collect_users, zip(threads, repeat(modes)))

    # close the pool and wait for the work to finish
    pool.close()
    pool.join()


# # test error
# ee=''
# try:
#     twt = TweepyWrapper(authen=6)
#     aa = twt._api.friends_ids(949488868277084160)
# except Exception as e:
#     ee = e
#     if e.reason == 'Not authorized.':
#         m = "uid: %s is Not authorized." % 956478302058958848
#         print(m)
#     elif e.reason == "[{'code': 34, 'message': 'Sorry, that page does not exist.'}]":
#         print('uid:%s is not found'%956478302058958848)
#     # if ee.reason[0]
#     else:
#         print(e)
#         raise
#
# #*test
# all_collecting_uid.index(929987954436657152)
# len(all_collecting_uid)
# filtereduid_and_baseuser_set = set(load_object('data//filtereduid_and_baseuser.pkl'))
#
# red_1 =load_object('thread_collect_user/1/follower_unauthorised_users.pkl')
# red_1
# len(filtereduid_and_baseuser_set.intersection(set(red_1[0].followers))) == len(set(red_1[0].followers))