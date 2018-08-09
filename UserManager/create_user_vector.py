from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import copy
import pandas as pd
import json
import os
import logging
import operator
import pickle

# =============== Global Config ====================================================================

logging.basicConfig(filename='create_user_vector.log',level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
# choose module to run
# __name__ = "__main__"
__name__ = "__gencsv__"

# =============== Function ====================================================================
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

class UserNetwork():
    uid = ""
    friends = []
    followers = []

    def __init__(self, uid, friends=[], followers=[]):
        self.uid = uid
        self.friends = friends
        self.followers = followers

def load_object(filename):
    with open(filename, 'rb') as input:
        obj = pickle.load(input)
    return obj

def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def printlog(m):
    print(m)
    logging.info(m)


# =============== Main program ====================================================================
# generate user_objs_score.pkl
if __name__ == "__userobjscorepkl__":

    # =============== Main Config =================
    save_folder = 'user_objs_score//'

    # =============== Coin hashtag config =================
    coin_tag_list = pd.DataFrame.from_csv("C:\\Users\\Auu\\Desktop\\community_compare\\main\\uservector_hashtag_list.csv",header=0,index_col=None)
    dict_cointag_set = dict()

    print(coin_tag_list.shape)
    print(coin_tag_list.columns)
    for coin in coin_tag_list.columns:
        dict_cointag_set[coin] = set(coin_tag_list[coin].dropna())

    # =============== Processing file =================

    file_list = ["user_objs//1_user_objs.pkl",
                 "user_objs//2_user_objs.pkl",
                 "user_objs//3_user_objs.pkl",
                 "user_objs//4_user_objs.pkl",
                 "user_objs//5_user_objs.pkl",
                 "user_objs//6_user_objs.pkl"]

    # Process user_objs file
    for filename in file_list:
        # #* test
        # filename = file_list[0]

        user_objs = load_object(filename)

        for uid, info in user_objs.items():
            # #* test
            # uid = 984047889159737344
            # info = user_objs[uid]

            printlog("Processing user: %d"%uid)

            # prepare user vectors
            interest_scores = dict()

            # get total hashtag to calculate user vector
            total_hashtag_used = sum(info['hashtag_count'].values())

            #**Fix - if total_hashtag == 0 then assign to 0 right away no need to process
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
                        user_coin_tag_count+=info['hashtag_count'][ht]

                    # calculate interest score of this user to this coin: score = num_coin# / num_total#
                    interest_scores[coin_name] = dict()
                    interest_scores[coin_name]['prob'] = user_coin_tag_count/total_hashtag_used
                    interest_scores[coin_name]['count'] = user_coin_tag_count
                    related_tag_count+=user_coin_tag_count

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
        save_filename = save_folder + filename.rsplit("//")[-1].rstrip(".pkl") + "_score.pkl"
        save_object(user_objs, save_filename)
        printlog("Save: %s" % save_filename)
    printlog("Done processing all files..")
    # =============== End main program ====================================================================

# =========== Build user_objs dataframe ====================================================================
if __name__ == "__gencsv__":

    # ================== Config Build user_objs dataframe ==================================
    df_userinfo = pd.DataFrame.from_csv("C:\\Users\\Auu\\Desktop\\user_network\\data\\df_userinfo.csv")
    save_filename = "data//df_user_objs.csv"
    file_list = ["user_objs_score//1_user_objs_score.pkl",
                 "user_objs_score//2_user_objs_score.pkl",
                 "user_objs_score//3_user_objs_score.pkl",
                 "user_objs_score//4_user_objs_score.pkl",
                 "user_objs_score//5_user_objs_score.pkl",
                 "user_objs_score//6_user_objs_score.pkl"]

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
                      # coins_raw_count
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
    for filename in file_list:
        uobjs = load_object(filename)
        for uid, info in uobjs.items():
            uc+=1
            # Assign scores
            for sname, score in info['scores'].items():
                dict_user_objs[sname].append(score['prob'])
                dict_user_objs[sname + '_count'].append(score['count'])

            # Assign user info from collected tweets
            dict_user_objs['uid'].append(uid)
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

    # fix -- uid distort
    # bkp = df_user_objs.copy()
    # bkp_dict_user_objs = dict_user_objs.copy()
    # dict_user_objs = bkp_dict_user_objs.copy()
    # dict_user_objs['uid'][1]
    dict_user_objs['uid'] = ["_"+str(iii) for iii in dict_user_objs['uid']]
    #---end fix--

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
    df_user_objs.to_csv(save_filename, index_label=None)
    print("total users processed: %d"%uc)
# =============== End Build user_objs dataframe ====================================================================

# =============== user_csv with z-score =====================
if __name__ == '__gencsvzscore__':
    df_user_objs = pd.DataFrame.from_csv("data//df_user_objs.csv")
    score_cols = 'bitcoin', 'ethereum', 'ripple', 'bitcoincash', 'eosio', 'litecoin', 'cardano', 'stellar', 'iota', 'tron', 'neo', 'monero', 'dash', 'nem', 'tether', 'vechain', 'ethereumclassic', 'bytecoin', 'binancecoin', 'qtum', 'zcash', 'icx', 'omisego', 'lisk', 'zilliqa', 'bitcoingold', 'aeternity', 'ontology', 'verge', 'steem', '1_crypto_market_news', '2_crypto_buzz_ads', '3_general', '4_bussiness_tech', '5_money_trading', 'others'
    for col in score_cols:
        # reshape to fit scaler
        data = df_user_objs[col].values.reshape(-1,1)
        scaler = StandardScaler()
        scaler.fit(data)
        zscore = scaler.transform(data)
        df_user_objs.loc[:,col] = zscore
        # print(zscore)
        # plt.figure()
        # plt.hist(zscore, bins = 50)
        # plt.title(col)
    df_user_objs.to_csv("data//df_user_objs_zscore.csv")

if __name__ == '__genedge__':
    def generate_edge(thread):
        # setup logfile according to thread
        logger = setup_logger('t%d' % thread, 'edge//%d_generate_edges.log' % (thread))
        logger.info('from thread: %d' % thread)

        def printlog(m):
            print(m)
            logger.info(m)

        strong_usernw = pd.DataFrame.from_csv("data//df_user_objs.csv")
        strong_usernw = strong_usernw.uid.values.tolist()
        print(len(strong_usernw))

        usernw = load_object("C:\\Users\\Auu\\Desktop\\user_network\\data\\top1000_combined_fri-fol_users.pkl")
        df_edge = pd.DataFrame(columns=["source","target"])
        if thread == 1:
            usernw = usernw[0:200]
        elif thread == 2:
            usernw = usernw[200:500]
        elif thread == 3:
            usernw = usernw[500:700]
        elif thread == 4:
            usernw = usernw[700:905]

        total = len(usernw)
        save_every = 10
        procuser = 1
        i = 0

        for baseuser in usernw:
            # base -follow-> u_xx
            src = "_"+str(baseuser.uid)
            for fri in baseuser.friends:
                tar = "_"+str(fri)
                if tar in strong_usernw:
                    df_edge.loc[i] = [src, tar]
                    i += 1
                    # print(i)
            printlog("%d|(%d/%d) Done friends of user: %s"%(thread,procuser,total,baseuser.uid))
            printlog("%d|(%d/%d) Build edges: %s" % (thread,procuser,total,i))

            # u_xx -follow-> base
            tar = "_" + str(baseuser.uid)
            for fol in baseuser.followers:
                src = "_" + str(fol)
                if src in strong_usernw:
                    df_edge.loc[i] = [src, tar]
                    i += 1
                    # print(i)
            printlog("%d|(%d/%d) Done followers of user: %s"%(thread,procuser,total,baseuser.uid))
            printlog("%d|(%d/%d) Build edges: %s" % (thread,procuser,total,i))
            procuser+=1

            # save every 10 users
            if procuser >= save_every:
                df_edge.to_csv("edge//%d//t%d_edge_%d.csv"%(thread,thread,procuser))
                df_edge = pd.DataFrame(columns=["source","target"])
                # 10 more users  then save again then extend and so on..
                save_every+=10

        # save all unsaved edges
        df_edge.to_csv("edge//%d//t%d_edge_%d.csv" % (thread, thread, procuser))

        #** First file
        #df_edge[0:48830].to_csv("edge//edge_1.csv",index=False)


    from multiprocessing.dummy import Pool as ThreadPool
    # make the Pool of workers
    pool = ThreadPool(4)

    # results = pool.starmap(function, zip(list_a, list_b))
    # threads = [1, 2, 3, 4, 5]
    threads = [1,2,3,4]
    pool.map(generate_edge, threads)

    # close the pool and wait for the work to finish
    pool.close()
    pool.join()

if __name__ == 'combine_edge_files':
    # Get json file path
    walk_dir = "edge"
    file_list = []
    for root, subdirs, files in os.walk(walk_dir):
        path, book_name = os.path.split(root)
        all_text = ""
        for filename in files:
            # os.path.join => join str with //
            file_path = os.path.join(root, filename)
            file_list.append(file_path)

    combinded_edge = pd.DataFrame(columns=['source', 'target'])
    for file in file_list:
        edge = pd.DataFrame.from_csv(file)
        print(edge.shape)
        combinded_edge = combinded_edge.append(edge)
    combinded_edge.to_csv('all_edges.csv')

# #
# ii = 0
# file_list = ["user_objs_score//1_user_objs_score.pkl",
#          "user_objs_score//2_user_objs_score.pkl",
#          "user_objs_score//3_user_objs_score.pkl",
#          "user_objs_score//4_user_objs_score.pkl",
#          "user_objs_score//5_user_objs_score.pkl",
#          "user_objs_score//6_user_objs_score.pkl"]
# for filename in file_list:
#     uobjs = load_object(filename)
#     for uid, info in uobjs.items():
#         ii+=1
# print(ii)
