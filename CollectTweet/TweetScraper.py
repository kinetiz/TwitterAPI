import tweepy
import json
import logging
import datetime

### Setup logging
logging.basicConfig(filename='history.log',level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")


### Class tweepy wrapper
class TweepyWrapper():
    # Variables for authentication
    __CONSUMER_KEY = 'l9BvOKjP2Xj48I5wlc7Uh8sVN'
    __CONSUMER_SECRET = 'HMKOvmuCaReDIzc0GlzfjQGKFrdCJ9jHlRJd8AAp0e7PHfwl6H'
    __ACCESS_TOKEN = '982717247109189632-cdUZCv2mzMCDiPiHkdRDpUQXdRnFIvB'
    __ACCESS_TOKEN_SECRET = 'AaayN6WOC3rPcYIoBg1Cc5uEPeUbcrw2jFHhhZVlHzjGC'

    # Setup authentication objects
    __auth = tweepy.OAuthHandler(__CONSUMER_KEY, __CONSUMER_SECRET)
    __auth.set_access_token(__ACCESS_TOKEN, __ACCESS_TOKEN_SECRET)
    _api = tweepy.API(__auth)
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

class TweetInfo():
    id = 0
    tweet = ""
    tweeterId = 0
    hashtags = []
    created_at = 0
    # location = ""



#######################################################
# Main
#######################################################
# Note
# - if retweeted = true, keep only the original tweet
# - use cursor to manage limit + loop running
# - save to neo4j
# - define more keywords
# - analyse network to refine keywords

twt = TweepyWrapper()

# getTimeline
# tweets = twt.getTweetByUser('kinetizx11')
# for t in tweets:
#     print(str(t.created_at) + " | " + str(t.retweeted) + ": " + t.text)


### search tweets by keywords
keyword = "#bitcoin OR #btc OR #eth OR #ether OR #ethereum until:2018-05-09"
tweets = twt._api.search(keyword, tweet_mode='extended')

### store tweets info
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

with open('data.json', 'w') as fp:
    json.dump(infos, fp, sort_keys=False, indent=4)

# with open('data.json', 'r') as fp:
#     data = json.load(fp)
    # print(str(t.created_at) + " | " + t.author.name +": " + tweet )

# aa = twt._api.user_timeline('kinetizx11', tweet_mode='extended')
# for t in aa:
#     print(str(t.created_at) + " | " + t.author.name + ": " + t.full_text)
#
## check remaining quota
quota = twt._api.rate_limit_status()['resources']
print(quota)

logging.info('test info')