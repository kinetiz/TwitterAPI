import json
from py2neo import Graph, authenticate
from neo4j.v1 import GraphDatabase
import os
import logging
import datetime
import math

### Setup logging
logging.basicConfig(filename='insert_history.log',level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
#
# # Connect to neo4j
# authenticate("localhost:7474", "neo4j", "11111")
# graph = Graph()


# Connect to database
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "11111"))

### test code ##################
q_test = """Return apoc.date.format(timestamp()+(1000*60*60*1)) as now"""
with driver.session() as session:
    tx = session.begin_transaction()
    ret = tx.run(q_test).single().value()
    tx.commit()
    print(ret)
#################################


##Get json file path
# walk_dir = "G:\\work\\TwitterAPI\\data\\used_data\\top1"
# file_list = []
# for root, subdirs, files in os.walk(walk_dir):
#         path, book_name = os.path.split(root)
#         all_text = ""
#         for filename in files:
#             # os.path.join => join str with //
#             file_path = os.path.join(root, filename)
#             file_list.append(file_path)

file_list = [
                "G:\\work\\TwitterAPI\\data\\cleaned_data\\top2-5\\top2-5_2018-06-12_to_2018-06-16.json",
                "G:\\work\\TwitterAPI\\data\\cleaned_data\\top6-30\\top6-30_2018-06-14_to_2018-06-16.json",
                "G:\\work\\TwitterAPI\\data\\cleaned_data\\top1\\top1_2018-06-13_to_2018-06-16.json",
             ]

chunkSize = 10000

data = []
# Loop insert data to Neo4j from each json file
for file_name in file_list:
    print('Loading: ' + file_name + '..')
    with open(file_name) as f:
        data = json.load(f)

    # Change hashtag to lowercase before running cypher to increase speed
    for tidx, t in enumerate(data['tweets']):
        for hidx, h in enumerate(t['hashtags']):
            data['tweets'][tidx]['hashtags'][hidx] = h.lower()

    chunkNum = math.ceil(len(data['tweets'])/chunkSize)

    for i in range(0,chunkNum):
        start = (i*chunkSize)
        chunk = {'tweets': data['tweets'][start:start+chunkSize]}

        ## Prepare query
        # Insert Tweet
        q_insert_tweet = """WITH {json} AS document
                        UNWIND document.tweets AS tweets
                        MERGE (t:Tweet {id: tweets.tid})
                            ON CREATE SET
                                t.id = tweets.tid,
                                t.text = tweets.tweet,
                                t.created_at = tweets.created_at,
                                t.country = tweets.country,
                                t.link_count = tweets.link_count,
                                t.last_update = apoc.date.format(timestamp()+(1000*60*60*1))
                        RETURN count(t)
                        """
        #  user
        q_insert_user = """WITH {json} AS document
                        UNWIND document.tweets AS tweets
                        MERGE (u:User {id: tweets.uid})
                            ON CREATE SET
                                u.id = tweets.uid,
                                u.screen_name = tweets.screen_name,
                                u.follower_count = tweets.friends_count,
                                u.following_count = tweets.followers_count,
                                u.last_update = apoc.date.format(timestamp()+(1000*60*60*1))

                        RETURN count(u)
                        """
        #  hashtag
        q_insert_hashtag = """WITH {json} AS document
                                UNWIND document.tweets AS tweets
                                UNWIND tweets.hashtags AS hashtag
                                //Hashtag
                                MERGE (h:Hashtag {tag: hashtag})
                                    ON CREATE SET
                                        h.tag = hashtag,
                                        h.last_update = apoc.date.format(timestamp()+(1000*60*60*1))
                                RETURN count(h)
                                """
        #  link
        q_insert_link = """WITH {json} AS document
                                UNWIND document.tweets AS tweets
                                UNWIND tweets.hashtags AS hashtag
                                MATCH   (t:Tweet{id: tweets.tid}),
                                        (u:User{id: tweets.uid}),
                                        (h:Hashtag{tag: hashtag})
                                //Tweet->Hashtag
                                MERGE (t)-[rh:has]->(h)
                                //User->Tweet
                                MERGE (u)-[rp:post]->(t)
                                RETURN count(rh)+count(rp)
                                """

        ### Execute queries
        with driver.session() as session:
            ### Insert Tweets
            logging.info('Start inserting Tweets Chunk: ' + str(i) + ' | ' + file_name + '..')
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + " - Chunk: " + str(i) + ' - inserting Tweets: ' + file_name + '..')
            tx = session.begin_transaction()
            ret = tx.run(q_insert_tweet, json=chunk).single().value()
            tx.commit()
            print(str(ret) + " nodes inserted")
            logging.info(str(ret) + " nodes inserted")

            # Insert Users
            logging.info('Start inserting Users Chunk: ' + str(i) + ' | ' + file_name + '..')
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + " - Chunk: " + str(i) + ' - inserting Users: ' + file_name + '..')
            tx = session.begin_transaction()
            ret = tx.run(q_insert_user, json=chunk).single().value()
            tx.commit()
            print(str(ret) + " nodes inserted")
            logging.info(str(ret) + " nodes inserted")

            # Insert Hashtag
            logging.info('Start inserting Hashtag Chunk: ' + str(i) + ' | ' + file_name + '..')
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + " - Chunk: " + str(i) + ' - inserting Hashtag: ' + file_name + '..')
            tx = session.begin_transaction()
            ret = tx.run(q_insert_hashtag, json=chunk).single().value()
            tx.commit()
            print(str(ret) + " nodes inserted")
            logging.info(str(ret) + " nodes inserted")

            # Insert Links
            logging.info('Start inserting link Chunk: ' + str(i) + ' | ' + file_name + '..')
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + " - Chunk: " + str(i) + ' - inserting links: ' + file_name + '..')
            tx = session.begin_transaction()
            ret = tx.run(q_insert_link, json=chunk).single().value()
            tx.commit()
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + " - Done Chunk: " + str(i) + " | " + str(ret) + " links inserted")
            logging.info("Done Chunk: " + str(i) + " | " + str(ret) + " links inserted")

        # Add Hash-to-Hash relationship

        ## add hash-hash
        # print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + ' - inserting hash-hash: ' + file_name + '..')
        # logging.info("Chunk"+str(i)+ ": " + 'Start inserting hash-hash: ' + file_name + '..')
        # with driver.session() as session:
        #     # Open transaction
        #     tx = session.begin_transaction()
        #     for t in chunk['tweets']:
        #         hashtag = t['hashtags']
        #         hashLen = len(hashtag)
        #         # Loop matching hashtag but not include previous eg. 3 tags -> (1,2),(1,3),(2,3) -> not include 2,1 /2,2 / 3,2
        #         for i in range(0, hashLen - 1):
        #             for j in range(i + 1, hashLen):
        #                 q = """ MATCH (h1:Hashtag{tag: $tag1}),
        #                               (h2:Hashtag{tag: $tag2})
        #                         MERGE (h1)-[r:together]-(h2)
        #                         ON CREATE SET r.count = 1
        #                         ON MATCH SET r.count = coalesce(r.count,0) + 1
        #                         RETURN count(r)"""
        #                 ret = tx.run(q, tag1=hashtag[i], tag2=hashtag[j]).single().value()
        #     tx.commit()
        # print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        # print("Chunk"+str(i)+ ": " + str(ret) + " Hash-hash links added..")
        # logging.info("Chunk"+str(i)+ ": " + str(ret) + " Hash-hash links added..")

        # Add User-to-User Reply and Retweet & Update Tweet.Retweet_count and Reply_count
        # ...
