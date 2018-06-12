import pickle
def load_object(filename):
    with open(filename, 'rb') as input:
        obj = pickle.load(input)
    return obj

def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

obj = load_object('twt_top6-30_2-5.pkl')
top6_30 = obj[0]
top2_5 = obj[1]
top1 = load_object('twt_top6-30_2-5.pkl')[0]

len(top6_30)
len(top2_5)
len(top1)

import operator
import csv
import sys

# coins = {
#         "bitcoin": ["bitcoin", "btc"],
#         "ethereum": ["ethereum", "eth", "ether"],
#         "ripple": ["ripple", "xrp"],
#         "bitcoincash": ["bitcoincash", "bch"],
#         "eosio": ["eosio", "eos"],
#         "litecoin": ["litecoin", "ltc"],
#         "cardano": ["cardano", "ada"],
#         "stellar": ["stellar", "xlm"],
#         "iota": ["iota", "miota"],
#         "tron": ["tron", "trx"],
#         "neo": ["neo"],
#         "monero": ["monero", "xmr"],
#         "dash": ["dash"],
#         "nem": ["nem", "xem"],
#         "tether": ["tether", "usdt"],
#         "vechain": ["vechain", "ven"],
#         "ethereum_classic": ["ethereumclassic", "etc"],
#         "bytecoin": ["bytecoin", "bcn"],
#         "binance_coin": ["binancecoin", "bnb"],
#         "qtum": ["qtum"],
#         "zcash": ["zcash", "zec"],
#         "icon": ["icx"],
#         "omisego": ["omisego"],
#         "lisk": ["lisk", "lsk"],
#         "zilliqa": ["zilliqa", "zil"],
#         "bitcoingold": ["bitcoingold", "btg"],
#         "aeternity": ["aeternity", "ae"],
#         "ontology": ["ontology", "ont"],
#         "verge": ["verge", "xvg"],
#         "steem": ["steem"]
#     }

# mode =  'top1'
# mode =  'top2-5'
mode =  'top6-30'
coins = {}
x =[]
if mode == 'top1':
    x = top1
    coins = {
        "bitcoin": ["bitcoin", "btc"]
    }

elif mode == 'top2-5':
    x = top2_5
    coins = {
        "ethereum": ["ethereum", "eth", "ether"],
        "ripple": ["ripple", "xrp"],
        "bitcoincash": ["bitcoincash", "bch"],
        "eosio": ["eosio", "eos"],
    }

elif mode == 'top6-30':
    x = top6_30
    coins = {
        "litecoin": ["litecoin", "ltc"],
        "cardano": ["cardano", "ada"],
        "stellar": ["stellar", "xlm"],
        "iota": ["iota", "miota"],
        "tron": ["tron", "trx"],
        "neo": ["neo"],
        "monero": ["monero", "xmr"],
        "dash": ["dash"],
        "nem": ["nem", "xem"],
        "tether": ["tether", "usdt"],
        "vechain": ["vechain", "ven"],
        "ethereum_classic": ["ethereumclassic", "etc"],
        "bytecoin": ["bytecoin", "bcn"],
        "binance_coin": ["binancecoin", "bnb"],
        "qtum": ["qtum"],
        "zcash": ["zcash", "zec"],
        "icon": ["icx"],
        "omisego": ["omisego"],
        "lisk": ["lisk", "lsk"],
        "zilliqa": ["zilliqa", "zil"],
        "bitcoingold": ["bitcoingold", "btg"],
        "aeternity": ["aeternity", "ae"],
        "ontology": ["ontology", "ont"],
        "verge": ["verge", "xvg"],
        "steem": ["steem"]
    }

sorted_x = sorted(x.items(), key=operator.itemgetter(1), reverse=True)

top=20
coins_h2h = {}
for k, v in coins.items():
    h2hcount_list=[]
    for h2hcount in sorted_x:
        countMatch = 0
        # check if h2h contain considered crypto hashtag
        for hash in v:
            countMatch += h2hcount[0].startswith(hash) + h2hcount[0].endswith(hash)
        # If h2h is in the hashtag list, add to h2hcount list
        if countMatch > 0:
            h2hcount_list.append(h2hcount)
    # add h2hcount list to the coins list
    coins_h2h[k] = h2hcount_list

for c in coins_h2h:
    outdata = coins_h2h[c][0:20]
    # print(outdata)
    with open(c+'.csv', 'w') as f:
        writer = csv.writer(f , lineterminator='\n')
        for tup in outdata:
            print(tup)
            a = list(tup)
            a[0] = a[0].encode(sys.stdout.encoding, errors='replace')
            writer.writerow(a)
