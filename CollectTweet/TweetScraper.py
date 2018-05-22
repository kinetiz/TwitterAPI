import tweepy
import json
import logging
import datetime
##############################################################
# Configuration
##############################################################
### Setup logging
logging.basicConfig(filename='history.log',level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

### Collecting date range
collectingDataSince = "2018-05-12"
collectingDataUntil = "2018-05-16"

### intial json file name
filename = 'top1_'+collectingDataSince+'_to_'+collectingDataUntil+'.json'

### save every N page
bulkSize = 50

### Define query
coinTags = {}
### 1 ###
coinTags['bitcoin'] = "#bitcoin OR #btc"

### 2-10 ###
# coinTags['ethereum'] = "#ethereum OR #eth OR #ether"
# coinTags['ripple'] = "#ripple OR #xrp"
# coinTags['bitcoincash'] = "#bitcoincash OR #bch"
# coinTags['eosio'] = "#eosio OR #eos"

# ## 11-30 ###
# coinTags['litecoin'] = "#litecoin OR #ltc"
# coinTags['cardano'] = "#cardano OR #ada"
# coinTags['stellar'] = "#stellar OR #xlm"
# coinTags['iota'] = "#iota OR #miota"
# coinTags['tron'] = "#tron OR #trx"
# coinTags['neo'] = "#neo"
# coinTags['monero'] = "#monero OR #xmr"
# coinTags['dash'] = "#dash"
# coinTags['nem'] = "#nem OR #xem"
# coinTags['tether'] = "#tether OR #usdt"
# coinTags['vechain'] = "#vechain OR #ven"
# coinTags['ethereum_classic'] = "#ethereumclassic OR #etc"
# coinTags['bytecoin'] = "#bytecoin OR #bcn"
# coinTags['binance_coin'] = "#binancecoin OR #bnb"
# coinTags['qtum'] = "#qtum"
# coinTags['zcash'] = "#zcash OR #zec"
# coinTags['icon'] = "#icx"
# coinTags['omisego'] = "#omisego"
# coinTags['lisk'] = "#lisk OR #lsk"
# coinTags['zilliqa'] = "#zilliqa OR #zil"
# coinTags['bitcoingold'] = "#bitcoingold OR #btg"
# coinTags['aeternity'] = "#aeternity OR #ae"
# coinTags['ontology'] = "#ontology OR #ont"
# coinTags['verge'] = "#verge OR #xvg"
# coinTags['steem'] = "#steem"

### Build query
query = ""
for i, c in enumerate(coinTags.values()):
    if i < len(coinTags)-1:
        query += c + " OR "
    else:
        query += c
query+=" since:"+collectingDataSince+" until:"+collectingDataUntil
print(len(query))
#########################################################################33


### Class tweepy wrapper
class TweepyWrapper():
    # Variables for authentication
    ## App1
    __CONSUMER_KEY = 'l9BvOKjP2Xj48I5wlc7Uh8sVN'
    __CONSUMER_SECRET = 'HMKOvmuCaReDIzc0GlzfjQGKFrdCJ9jHlRJd8AAp0e7PHfwl6H'
    __ACCESS_TOKEN = '982717247109189632-cdUZCv2mzMCDiPiHkdRDpUQXdRnFIvB'
    __ACCESS_TOKEN_SECRET = 'AaayN6WOC3rPcYIoBg1Cc5uEPeUbcrw2jFHhhZVlHzjGC'

    # ## App2
    # __CONSUMER_KEY = 'L7IX0KwYgQUGeC1TqnxULue1v'
    # __CONSUMER_SECRET = 'gRiqmdED0KFVjg6v2x9giQmctFLdAiFwEioCECuVCTJafp8byB'
    # __ACCESS_TOKEN = '982717247109189632-QRXdgrmZdhIy00do6D5o0wpdUMVKvJU'
    # __ACCESS_TOKEN_SECRET = 'szb7jQaVBe8JCf9iM23e3GBd7OgbuLRDxhTM6nU4L3QAp'

    # ## App3
    # __CONSUMER_KEY = 'w3TysRbh9H6oKp5T8qVNeSEdl'
    # __CONSUMER_SECRET = 'LJA4sjmh4mq7OvmfUngVr7OX7rAnxeuUsKPT9rbzD9iU1sWfa3'
    # __ACCESS_TOKEN = '982717247109189632-rB4KizgqhsFdMS1V1Tu8qcPdxAe2dDi'
    # __ACCESS_TOKEN_SECRET = 'joe3MY7vIjWhDttHMMTJmgchzOLYUNqhjGUuWpAS4d3Ro'

    # Setup authentication objects
    __auth = tweepy.OAuthHandler(__CONSUMER_KEY, __CONSUMER_SECRET)
    __auth.set_access_token(__ACCESS_TOKEN, __ACCESS_TOKEN_SECRET)
    _api = tweepy.API(__auth,
               # support for multiple authentication handlers
               # retry 3 times with 5 seconds delay when getting these error codes
               # For more details see
               # https://dev.twitter.com/docs/error-codes-responses
               retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503])
                , wait_on_rate_limit=True, wait_on_rate_limit_notify=True
               )
    _myinfo = _api.me()

    def sendTweet(self, text):
        # Update status
        self._api.update_status(status=text)

    def getUser(self, name):
        users = self._api.get_user("Blockchain")
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

#######################################################
# Main
#######################################################
# Note
# - if retweeted = true, keep only the original tweet
# - use cursor to manage limit + loop running
# - save to neo4j
# - define more keywords
# - analyse network to refine keywords

# Initial wrapper
twt = TweepyWrapper()
# ### Stored fields ##################################################################
# aa = twt.search("thanadonf")
# t = aa[0]
# ## tweet
# created_at = t.created_at
# tid = t.id
# tweet = t.full_text
# tweet_from_country = t.place.country if t.place is not None else None
#
# ## user /
# t.user.id
# t.user.screen_name
# t.user.followers_count
# t.user.friends_count
#
# ## build/update node + edge
#
# mentioned_uids = [i['id'] for i in t.entities['user_mentions']]
#
# hashtags = [i['text'] for i in t.entities['hashtags']]
#
# links = [i['url'] for i in t.entities['urls']]
#
# reply_to_tid = t.in_reply_to_status_id
# reply_to_uid = t.in_reply_to_user_id
#
# retweet_from_tid = t.retweeted_status.id #check none
# retweet_from_uid = t.retweeted_status.user.id #check none
#
# #<class 'list'>: [{'url': 'https://t.co/1V9RlGWRfE', 'expanded_url': 'http://www.google.com', 'display_url': 'google.com', 'indices': [46, 69]}, {'url': 'https://t.co/PKRIQSuGxd', 'expanded_url': 'http://www.sanook.com', 'display_url': 'sanook.com', 'indices': [70, 93]}]
# ##################################################################
###############################
# Loading tweets
###############################
# Initial json file as list
jsonFormat = {'tweets':[]}
with open(filename, 'w') as fp:
    json.dump(jsonFormat, fp, sort_keys=False, indent=4)

# Function for updating file
def updateJson(fname, infos):
    # load previous tweets
    with open(fname) as f:
        data = json.load(f)
    #getList of tweet from dict{tweets:[{info1},{info2},..]
    twList = data['tweets']
    # concate new tweets
    twList += infos
    data['tweets'] = twList
    # overwrite new tweets
    with open(fname, 'w') as f:
        json.dump(data, f, sort_keys=False, indent=4)

# Start loading with cursor
page_count = 0
infos = []
for tweets in tweepy.Cursor(twt._api.search, q=query, tweet_mode='extended', count=100).pages():
    page_count += 1
    print("processing page: " + str(page_count) + " with " + str(len(tweets)) + " tweets...")
    print("Sample: " + str(tweets[0].created_at))

    # build tweet info
    for t in tweets:
        info = {}
        # if tweet is not original, text will be truncated to 144 length.
        # Need to retrieve text and hashtags from original tweet.
        if 'retweeted_status' in t._json:
            tsource = t.retweeted_status
            info['hashtags'] = [i['text'] for i in tsource.entities['hashtags']]
            info['tweet'] = tsource.full_text
        else: #if its original, retrieve normally
            info['hashtags'] = [i['text'] for i in t.entities['hashtags']]
            info['tweet'] = t.full_text
        #tweet
        info['tid'] = t.id
        info['created_at'] = str(t.created_at)
        info['country'] = t.place.country if t.place is not None else None
        info['link_count'] = len(t.entities['urls'])
        #user
        info['uid'] = t.user.id
        info['screen_name'] = t.user.screen_name
        info['followers_count'] = t.user.followers_count
        info['friends_count'] = t.user.friends_count

        #relationship
        info['mentioned_uids'] = [i['id'] for i in t.entities['user_mentions']]
        info['reply_to_tid'] = t.in_reply_to_status_id
        info['reply_to_uid'] = t.in_reply_to_user_id
        info['retweet_from_tid'] = info['retweet_from_uid'] = None
        if 'retweeted_status' in t._json:
            info['retweet_from_tid'] = t.retweeted_status.id
            info['retweet_from_uid'] = t.retweeted_status.user.id

        infos.append(info)

    # Bulk write data every n pages
    if (page_count%bulkSize == 0):
        updateJson(filename, infos)
        updatedTweetCount = len(infos)
        logging.info("Save page/updated_twt: " + str(page_count) + "/" + str(updatedTweetCount))
        infos = []

    # Print remaining quota
    twt.printQuota()
# update again to save last bulk
updateJson(filename, infos)
logging.info("Save page/updated_twt: " + str(page_count) + "/" + str(updatedTweetCount))

print('Last bulk updated.. Done..')


# getTimeline
# tweets = twt.getTweetByUser('kinetizx11')
# for t in tweets:
#     print(str(t.created_at) + " | " + str(t.retweeted) + ": " + t.text)

# # load previous tweets
# with open("test2018-05-11.json") as f:
#     data = json.load(f)
#
# print(len(data))
