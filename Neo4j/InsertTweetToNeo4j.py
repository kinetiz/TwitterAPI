import json
from py2neo import Graph, authenticate

# Connect to neo4j
authenticate("localhost:7474", "neo4j", "11111")
graph = Graph()
## data
data = {"tweets": [
    {
        "hashtags": [
            "bitcoin",
            "ethereum",
            "ico",
            "binance",
            "xoxo"
        ],
        "tweet": "Big shoutout to @devnullius , Bitto's number one source for Crypto gossips! :)\nJust kidding about gossips of course - Devvie is a true crypto expert, make sure to follow them!\n\n#bitcoin #ethereum #ico #binance #xoxo https://t.co/yRCaIm7LP1",
        "tid": 995453567296159744,
        "created_at": "2018-05-12 23:59:59",
        "country": None,
        "link_count": 0,
        "uid": 975044115317403649,
        "screen_name": "mu_hoc",
        "followers_count": 12,
        "friends_count": 103,
        "mentioned_uids": [
            940886642197274625,
            41140413
        ],
        "reply_to_tid": None,
        "reply_to_uid": None,
        "retweet_from_tid": 995353213896417281,
        "retweet_from_uid": 940886642197274625
    },
    {
        "hashtags": [
            "HappyWeekend",
            "crypto",
            "Telegram",
            "LetsMakeItReal",
            "Cryptocurrency",
            "Blockchain",
            "ToTheMOON",
            "Bitcoin"
        ],
        "tweet": "#HappyWeekend to all the #crypto community ",
        "tid": 995453565689790466,
        "created_at": "2018-05-12 23:59:59",
        "country": None,
        "link_count": 0,
        "uid": 3255922813,
        "screen_name": "emtseth",
        "followers_count": 2515,
        "friends_count": 1546,
        "mentioned_uids": [
            954521193205436417
        ],
        "reply_to_tid": None,
        "reply_to_uid": None,
        "retweet_from_tid": 995327759110037505,
        "retweet_from_uid": 954521193205436417
    }
]
}

with open("G:/work/TwitterAPI/data/top1/test.json") as f:
    data = json.load(f)

q_build_initial_graph = """WITH {json} AS document
    UNWIND document.tweets AS tweets
    UNWIND tweets.hashtags AS hashtag
    //Tweet
    MERGE (t:Tweet {id: tweets.tid})
        ON CREATE SET 
            t.id = tweets.tid,
            t.text = tweets.tweet,    
            t.created_at = tweets.created_at,
            t.country = tweets.country,
            t.link_count = tweets.link_count
    //Users
    MERGE (u:User {id: tweets.uid})
        ON CREATE SET 
            u.id = tweets.uid,
            u.screen_name = tweets.screen_name,
            u.follower_count = tweets.friends_count,
            u.following_count = tweets.followers_count  
    //Hashtag
    MERGE (h:Hashtag {tag: toLower(hashtag)})
        ON CREATE SET 
            h.tag = toLower(hashtag)      

    //Tweet->Hashtag
    MERGE (t)-[:has]->(h)

    //User->Tweet
    MERGE (u)-[:post]->(t)

    RETURN count(t)
    """
q = q_build_initial_graph
graph.run(q, json=data).dump()
