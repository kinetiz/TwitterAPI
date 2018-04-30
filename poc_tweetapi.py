import tweepy
import json

# Variables for authentication
consumer_key = 'l9BvOKjP2Xj48I5wlc7Uh8sVN'
consumer_secret = 'HMKOvmuCaReDIzc0GlzfjQGKFrdCJ9jHlRJd8AAp0e7PHfwl6H'
access_token = '982717247109189632-cdUZCv2mzMCDiPiHkdRDpUQXdRnFIvB'
access_token_secret = 'AaayN6WOC3rPcYIoBg1Cc5uEPeUbcrw2jFHhhZVlHzjGC'

# Setup authentication objects
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Update status
#tweet = 'Hello, world!'
#api.update_status(status=tweet)
#myinfo = api.me()
#api.get_user("Blockchain")

#for tweet in tweepy.Cursor(api.search, q='#python', rpp=100).items(MAX_TWEETS):
#    # Do something
#    pass


    
result = api.search(q='thanadonf')
print(len(result)) 
textout=[]
for row in result:
    textout.append(row.text) 
    print(row.text)
rate = api.rate_limit_status()
print(rate['resources']['search'])

#--
resultx = api.search(q='#btc or #eth')
print(len(resultx))
rate = api.rate_limit_status()

textoutx=[]
for row in resultx:
    textoutx.append(row.text) 
    print(row.text)

result_user=api.user_timeline("kinetizx11")

#get retweet
aa = api.retweets(result[8].id)

987490376977088512 <-source
987833474076807169 <-retweeted
987494932926562305 <-retweeted by kinetiz10
987833474076807169 <-retweeted by kinetiz11