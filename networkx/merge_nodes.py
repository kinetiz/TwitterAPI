import numpy as np
import csv
import networkx as nx
import pandas as pd
import logging
import pickle
def load_object(filename):
    with open(filename, 'rb') as input:
        obj = pickle.load(input)
    return obj

logging.basicConfig(filename='merge_nodes.log',level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

def printlog(m):
    print(m)
    logging.info(m)

def merge_nodes(ggg, merged_nodes, new_node):
    # expect: nodes| NEW = 15, z = 5
    #         edges| NEW-NEW = 20, NEW-z = 20
    # ======== merge n`odes & edges ==============

    gg = ggg.copy()
    # merged_nodes = ['a', 'b', 'c']
    # new_node = 'NEW'

    # -- sum up weight of merging nodes
    sum_w = 0
    community = None
    for node, data in gg.nodes(data=True):
        # sum deg_w of merging nodes
        if node in merged_nodes:
            sum_w += data['deg_w']
            community = data['community']

    # -- replace merged nodes with new node and add to temp

    printlog('temp merge nodes')
    df_temp_edges = pd.DataFrame()
    rmv_edges = []
    for src, tar, w in gg.edges.data('weight'):
        if src in merged_nodes or tar in merged_nodes:
            rmv_edges.append((src, tar))

            temp_src = src
            temp_tar = tar

            # prepare src to temp
            if src in merged_nodes:
                temp_src = new_node

            # prepare target to temp
            if tar in merged_nodes:
                temp_tar = new_node

            # add to temp df
            df_temp_edges = df_temp_edges.append([[temp_src, temp_tar, w]])

    # -- Remove old edge
    printlog('remove_edges')
    gg.remove_edges_from(rmv_edges)

    # -- sum edges and add add to graph
    # name it to easy to process
    df_temp_edges.columns = ['src', 'tar', 'w']
    # sum up deg_w of merged edges
    a = df_temp_edges.groupby(['src', 'tar']).sum()
    # add merged edges with sum weight
    printlog('adding edges')

    for i in a.iterrows():
        grouped_cols = i[0]
        sum_cols = i[1]
        printlog(grouped_cols[0])
        gg.add_edge(grouped_cols[0], grouped_cols[1], weight=sum_cols.w)

    # -- Replace merged nodes with new_node
    printlog('remove nodes')

    gg.remove_nodes_from(merged_nodes)
    printlog('add new nodes')

    gg.add_node(new_node, deg_w=sum_w, community=community)
    printlog('af add new nodes')

    # nx.draw(gg, with_labels=True, font_weight='bold')
    return gg

def write_nodes_edges(gg):
    # -- write files
    # f_edges = pd.DataFrame()
    # printlog('save edges')
    # for src, tar, w in gg.edges.data('weight'):
    #     printlog(src)
    #     f_edges = f_edges.append([[src, tar, w]])
    # f_edges.columns = ['source', 'target', 'weight']
    # f_edges.to_csv('merged_edges.csv', index=False)
    nx.write_weighted_edgelist(gg,'merged_edges.csv',delimiter=',')

    printlog('save nodes')
    with open('merged_nodes.csv',mode='w',newline='') as f_nodes:
        writer = csv.writer(f_nodes, delimiter=',')
        writer.writerow(['id', 'weighted_degree', 'community'])
        for i in gg.nodes.data():
            # printlog(i[0])
            id = i[0]
            deg_w = i[1]['deg_w']
            community = i[1]['community']
            writer.writerow([id, deg_w, community])

    return 1


if __name__ == '__mergenodes__':

    # -- new graph imported from cotag nw
    g = nx.Graph()

    df_nodes = pd.DataFrame.from_csv("cotag//nodes.csv", header= None)
    for row in df_nodes.iterrows():
        g.add_node(row[0], deg_w=row[1][1], community=row[1][2])

    df_edges = pd.DataFrame.from_csv('cotag//edges.csv', header=None)
    for row in df_edges.iterrows():
        g.add_edge(row[0], row[1][1], weight=row[1][2])

    # nx.draw(g, with_labels=True, font_weight='bold')

    # #*test
    # ggg = nx.Graph()
    # ggg.add_edge('a','b',weight=10)
    # ggg.add_edge('a','c',weight=10)
    #
    # ggg.add_node('a', deg_w=5)
    # ggg.add_node('b', deg_w=5)
    # ggg.add_node('c', deg_w=5)
    #
    # nx.draw(ggg, with_labels=True, font_weight='bold')

    # -- load list of hashtag to be merged
    df_hashtag_list = pd.DataFrame.from_csv("C:\\Users\\Auu\\Desktop\\community_compare\\main\\uservector_hashtag_list.csv",index_col=None)
    dict_cointag_set = dict()
    for coin in df_hashtag_list.columns:
        dict_cointag_set[coin] = set(df_hashtag_list[coin].dropna())

    for coin_name, coin_tag_set in dict_cointag_set.items():

        # ========== Set parameters ==========
        merged_nodes = list(coin_tag_set)
        new_node = coin_name
        # -- call merge nodes
        g = merge_nodes(g, merged_nodes, new_node)
    # -- write merged nodes to files
    write_nodes_edges(g)
# #*test
# merged_nodes = ['cryptocurrency', 'crypto']
# new_node = 'ARAU'
#
# # -- call merge nodes
# new_g = merge_nodes(g, merged_nodes, new_node)
# # -- write merged nodes to files
# write_nodes_edges(new_g)
# #expect
# #node weight 3030.237844+3086.666389 = 6116.904233


if __name__ == "__genheatmapcsv__":
    edges = pd.DataFrame.from_csv('merged_edges.csv', index_col = None)
    coin_grp = pd.DataFrame.from_csv('coin_group.csv', index_col = None, header=None)
    group_names = coin_grp[0].values.tolist()

    list_source = []
    list_target = []
    list_weight = []
    for gn in group_names:
        allusernw_withvectors = edges[['weight', 'target']][edges.source == gn]
        b = edges[['weight', 'source']][edges.target == gn]
        b = b.drop(b[b.source==gn].index)

        list_weight += allusernw_withvectors.weight.values.tolist() + b.weight.values.tolist()
        list_target += allusernw_withvectors.target.values.tolist() + b.source.values.tolist()
        list_source += [gn for i in range(len(allusernw_withvectors) + len(b))]
    len(list_weight )
    len(list_target)
    len(list_source)
    df_heatmap = pd.DataFrame({'source': list_source, 'target': list_target, 'weight': list_weight})
    df_heatmap['log_weight'] = np.log(df_heatmap.weight)

    # change name - coins = rank_name | communities => remove prefix #_name
    for idx,name in enumerate(group_names[0:30]):
        df_heatmap = df_heatmap.replace(to_replace=name, value='%s_%s'%(idx+1,name))

    for idx,name in enumerate(group_names[30:]):
        df_heatmap = df_heatmap.replace(to_replace=name, value=name[2:])

if __name__ == "__calcorr__":
    ###################################################3
    # calculate correlation btw coins and communities
    ###################################################3
    df_heatmap = pd.DataFrame.from_csv('edges_heatmap.csv', index_col=None)
    df_coin_community =df_heatmap.dropna()

    df_coin_community.corr('pearson')
    df_coin_community.corr('spearman')
    df_coin_community.corr('kendall')

    crypto_news = df_coin_community[df_coin_community.source == 'MARKET&NEWS']
    trading = df_coin_community[df_coin_community.source == 'MONEY&TRADING']
    general = df_coin_community[df_coin_community.source == 'GENERAL']
    buzz = df_coin_community[df_coin_community.source == 'BUZZ&ADS']
    tech = df_coin_community[df_coin_community.source == 'BUSINESS&TECH']

    crypto_news.corr('pearson')
    crypto_news.corr('spearman')
    crypto_news.corr('kendall')

    trading.corr('pearson')
    trading.corr('spearman')
    trading.corr('kendall')

    general.corr('pearson')
    general.corr('spearman')
    general.corr('kendall')

    buzz.corr('pearson')
    buzz.corr('spearman')
    buzz.corr('kendall')

    tech.corr('pearson')
    tech.corr('spearman')
    tech.corr('kendall')


    # # testing check size of each coin must be 34-35
    # for i in group_names:
    #     print(df_heatmap[df_heatmap.source==i].shape)