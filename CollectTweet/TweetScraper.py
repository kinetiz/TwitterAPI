import tweepy
import json
import logging
import datetime
##############################################################
# Configuration
##############################################################
### Setup logging
logging.basicConfig(filename='historyV1.log',level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
logging.info("Save page: " + str(1))

### intial json file name
filename = 'top1_10_2018_05_16_to_18coins.json'

### Define query
coinTags = {}
### 1-10 ###
coinTags['bitcoin'] = "#bitcoin OR #btc"
coinTags['ethereum'] = "#ethereum OR #eth OR #ether"
coinTags['ripple'] = "#ripple OR #xrp"
coinTags['bitcoincash'] = "#bitcoincash OR #bch"
coinTags['eosio'] = "#eosio OR #eos"
coinTags['litecoin'] = "#litecoin OR #ltc"
coinTags['cardano'] = "#cardano OR #ada"
coinTags['stellar'] = "#stellar OR #xlm"
coinTags['iota'] = "#iota OR #miota"
coinTags['tron'] = "#tron OR #trx"

# ## 11-20 ###
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

### 21-30 ###
# coinTags['zcash'] = "#zcash OR #zec"
# coinTags['icon'] = "#icx"
# coinTags['omisego'] = "#omisego"
# coinTags['lisk'] = "#lisk OR #lsk"
# coinTags['zilliqa'] = "#zilliqa OR #zil"
# coinTags['bitcoingold'] = "#btg"
# coinTags['aeternity'] = "#aeternity OR #ae"
# coinTags['ontology'] = "#ontology OR #ont"
# coinTags['verge'] = "#verge OR #xvg"
# coinTags['steem'] = "#steem"

query = ""
for i, c in enumerate(coinTags.values()):
    if i < len(coinTags)-1:
        query += c + " OR "
    else:
        query += c
query+=" since:2018-05-16 until:2018-05-18"
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
        tweets = self._api.search(q=keyword)
        for row in tweets:
            # textoutx.append(row.text)
            print(row.text)
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
        print("Quota (call/time): " + callLeft + "/" + resetTime)

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

###############################
# Loading tweets
###############################
# Initial json file as list
with open(filename, 'w') as fp:
    json.dump([], fp, sort_keys=False, indent=4)

# Start loading with cursor
page_count = 0
for tweets in tweepy.Cursor(twt._api.search, q=query, tweet_mode='extended', count=100).pages():
    page_count += 1
    print("processing page: " + str(page_count) + " with " + str(len(tweets)) + " tweets...")
    print("Sample: " + str(tweets[0].created_at))
    # build tweet info
    infos = []
    for t in tweets:
        if 'retweeted_status' in t._json:
            t = t.retweeted_status
        hashtags = []
        for h in t.entities['hashtags']:
            hashtags.append(h['text'])
        info = {}
        info['id'] = t.id
        info['tweet'] = t.full_text
        info['user_id'] = t.author.id
        info['created_at'] = str(t.created_at)
        info['hashtags'] = hashtags
        infos.append(info)

    # Bulk write data every 50 pages
    if (page_count%50 == 0):
        # load previous tweets
        with open(filename) as f:
            data = json.load(f)
        # append with new tweets
        data += infos
        # overwrite new tweets
        with open(filename, 'w') as f:
            json.dump(data, f, sort_keys=False, indent=4)

        logging.info("Save page: " + str(page_count))

    # Print remaining quota
    twt.printQuota()

print('Done..')


# getTimeline
# tweets = twt.getTweetByUser('kinetizx11')
# for t in tweets:
#     print(str(t.created_at) + " | " + str(t.retweeted) + ": " + t.text)


