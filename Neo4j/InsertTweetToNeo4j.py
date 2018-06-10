import json
from py2neo import Graph, authenticate
import os
import logging
import datetime

### Setup logging
# logging.basicConfig(filename='insert_history.log',level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

# Connect to neo4j
authenticate("localhost:7474", "neo4j", "11111")
graph = Graph()

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
file_list = [ "G:\\work\\TwitterAPI\\data\\used_data\\top2-5\\top2-5_2018-05-12_to_2018-05-16.json"
            , "G:\\work\\TwitterAPI\\data\\used_data\\top2-5\\top2-5_2018-05-16.json"
            , "G:\\work\\TwitterAPI\\data\\used_data\\top1\\top1_2018-05-14.json"
            , "G:\\work\\TwitterAPI\\data\\used_data\\top1\\top1_2018-05-15.json"
            , "G:\\work\\TwitterAPI\\data\\used_data\\top1\\top1_2018-05-16.json"
            , "G:\\work\\TwitterAPI\\data\\used_data\\top2-5\\top2-5_2018-05-17_to_2018-05-21.json"
            , "G:\\work\\TwitterAPI\\data\\used_data\\top2-5\\top2-5_2018-05-21_to_2018-05-24.json"
             ]
data = []
# Loop insert data to Neo4j from each json file
for file_name in file_list:
    print('Loading: ' + file_name + '..')
    with open(file_name) as f:
        data = json.load(f)

    # Initial networks with Nodes and some relationship
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

    print('Inserting: ' + file_name + '..')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    graph.run(q, json=data).dump()

    print('Done inserting: ' + file_name + '..')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    # logging.info("Done Insert: " + file_name)

    # Add Hash-to-Hash relationship
    # ...

    # Add User-to-User Reply and Retweet & Update Tweet.Retweet_count and Reply_count
    # ...

    # """WITH {json} AS document
    #         UNWIND document.tweets AS tweets
    #         UNWIND tweets.hashtags AS hashtag
    #         //Tweet
    #         MERGE (t:Tweet {id: tweets.tid})
    #             ON CREATE SET
    #                 t.id = tweets.tid,
    #                 t.text = tweets.tweet,
    #                 t.created_at = tweets.created_at,
    #                 t.country = tweets.country,
    #                 t.link_count = tweets.link_count
    #         //Users
    #         MERGE (u:User {id: tweets.uid})
    #             ON CREATE SET
    #                 u.id = tweets.uid,
    #                 u.screen_name = tweets.screen_name,
    #                 u.follower_count = tweets.friends_count,
    #                 u.following_count = tweets.followers_count
    #         //Hashtag
    #         MERGE (h:Hashtag {tag: toLower(hashtag)})
    #             ON CREATE SET
    #                 h.tag = toLower(hashtag)
    #
    #         //Tweet->Hashtag
    #         MERGE (t)-[:has]->(h)
    #
    #         //User->Tweet
    #         MERGE (u)-[:post]->(t)
    #
    #         RETURN count(t)
    #         """