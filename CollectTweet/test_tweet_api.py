import tweepy
import json
import logging
import datetime

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

##############################################################
# Configuration
##############################################################
### Setup logging
logging.basicConfig(filename='history.log',level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

### Setup authentication
# ## App1
__CONSUMER_KEY = 'l9BvOKjP2Xj48I5wlc7Uh8sVN'
__CONSUMER_SECRET = 'HMKOvmuCaReDIzc0GlzfjQGKFrdCJ9jHlRJd8AAp0e7PHfwl6H'
__ACCESS_TOKEN = '982717247109189632-cdUZCv2mzMCDiPiHkdRDpUQXdRnFIvB'
__ACCESS_TOKEN_SECRET = 'AaayN6WOC3rPcYIoBg1Cc5uEPeUbcrw2jFHhhZVlHzjGC'

# ### App2
# __CONSUMER_KEY = 'L7IX0KwYgQUGeC1TqnxULue1v'
# __CONSUMER_SECRET = 'gRiqmdED0KFVjg6v2x9giQmctFLdAiFwEioCECuVCTJafp8byB'
# __ACCESS_TOKEN = '982717247109189632-QRXdgrmZdhIy00do6D5o0wpdUMVKvJU'
# __ACCESS_TOKEN_SECRET = 'szb7jQaVBe8JCf9iM23e3GBd7OgbuLRDxhTM6nU4L3QAp'

# ## App3
# __CONSUMER_KEY = 'w3TysRbh9H6oKp5T8qVNeSEdl'
# __CONSUMER_SECRET = 'LJA4sjmh4mq7OvmfUngVr7OX7rAnxeuUsKPT9rbzD9iU1sWfa3'
# __ACCESS_TOKEN = '982717247109189632-rB4KizgqhsFdMS1V1Tu8qcPdxAe2dDi'
# __ACCESS_TOKEN_SECRET = 'joe3MY7vIjWhDttHMMTJmgchzOLYUNqhjGUuWpAS4d3Ro'
####

### Collecting date range
collectingDataSince = "2018-06-12"
collectingDataUntil = "2018-06-16"

### intial json file name
filename = 'top2-5_'+collectingDataSince+'_to_'+collectingDataUntil+'.json'

### save every N page
bulkSize = 50

### Define query
coinTags = {}
### 1
# coinTags['bitcoin'] = "#bitcoin OR #btc"

# 2-5 ###
coinTags['ethereum'] = "#ethereum OR #eth OR #ether"
coinTags['ripple'] = "#ripple OR #xrp"
coinTags['bitcoincash'] = "#bitcoincash OR #bch"
coinTags['eosio'] = "#eosio OR #eos"

# ## 6-30 ###
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
#########################################################################


#######################################################
# Main
#######################################################
# Note
# - save to neo4j
# - analyse network to refine keywords

# Initial wrapper
twt = TweepyWrapper(__CONSUMER_KEY,__CONSUMER_SECRET,__ACCESS_TOKEN,__ACCESS_TOKEN_SECRET)
tweets = twt.getTweetByUser('kinetiz10')