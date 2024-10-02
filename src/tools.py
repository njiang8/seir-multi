import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import collections
import csv

import random
import matplotlib.pyplot as plt
#from parameter_singe_disease import INTRO

# Random int generator based on normal distribution
def GenBoundedRandomNormal(meanVal, stdDev, lowerBound, upperBound):
    aRand = random.gauss(meanVal, stdDev)  # could also use: normalvariate()but gauss () is slightly faster.

    while (aRand < lowerBound or aRand > upperBound):
        aRand = random.gauss(meanVal, stdDev)
    return aRand


def plot_multi_SEIR(df, INTRO):
    print(df.head())
    fig, ax = plt.subplots(figsize=(25, 10))

    # plt.figure(figsize=(25,10))
    plt.xlabel('time $t$', fontsize=20, fontname="Arial")
    plt.ylabel('Population', fontsize=20, fontname="Arial")

    if INTRO == True:
        plt.plot(df.index, df.E1, marker='*', markerfacecolor='gray', markersize= 10, color='yellow', linewidth=2)
        plt.plot(df.index, df.E2, marker='+', markerfacecolor='gray', markersize= 10, color='orange', linewidth=2)

        plt.plot(df.index, df.I1, marker='*', markerfacecolor='gray', markersize=10, color='red', linewidth=2)
        plt.plot(df.index + 1, df.I2, marker='+', markerfacecolor='gray', markersize=10, color='pink', linewidth=2)

        plt.plot(df.index, df.R1, marker='*', markerfacecolor='gray', markersize=10, color='green', linewidth=2)
        plt.plot(df.index + 1, df.R2, marker='+', markerfacecolor='gray', markersize=10, color='springgreen', linewidth=2)

    #if INTRO == False:
    plt.plot(df.index, df.S, marker='o', markerfacecolor='gray', markersize=2, color='skyblue', linewidth=2)

    plt.plot(df.index, df.E, marker='o', markerfacecolor='gray', markersize=2, color='orange', linewidth=2)
        # plt.plot(df.index, df.E1, marker='*', markerfacecolor='gray', markersize= 10, color='yellow', linewidth=2)
        # plt.plot(df.index + 1, df.E2, marker='+', markerfacecolor='gray', markersize= 10, color='orange', linewidth=2)
        # plt.plot(df.index + 1, df.E3, marker='+', markerfacecolor='gray', markersize= 10, color='orange', linewidth=2)

    plt.plot(df.index, df.I, marker='o', markerfacecolor='gray', markersize=2, color='red', linewidth=2)
        # plt.plot(df.index, df.I1, marker='*', markerfacecolor='gray', markersize=10, color='red', linewidth=2)
        # plt.plot(df.index + 1, df.I2, marker='+', markerfacecolor='gray', markersize=10, color='pink', linewidth=2)
        # plt.plot(df.index + 1, df.I3, marker='+', markerfacecolor='gray', markersize= 10, color='darkred', linewidth=2)

    plt.plot(df.index, df.R, marker='o', markerfacecolor='gray', markersize=2, color='green', linewidth=2)
        # plt.plot(df.index, df.R1, marker='*', markerfacecolor='gray', markersize=10, color='green', linewidth=2)
        # plt.plot(df.index + 1, df.R2, marker='+', markerfacecolor='gray', markersize=10, color='springgreen', linewidth=2)

    #plt.plot(df.index, df.D, marker='o', markerfacecolor='gray', markersize=2, color='black', linewidth=2)
    # plt.legend(('Susceptible', 'Exposed', 'Infectious','Recovered', 'Dead'), prop={"size":20}, fancybox=True, framealpha=1, shadow=True,loc = 'upper right', ncol = 5)

    plt.gcf().autofmt_xdate()  # italics of x label
        # plt.savefig('SEIR_WL.png')
    plt.show()

def plot_overall_SEIR(df):
    #print(df.head())
    fig, ax = plt.subplots(figsize=(25,10))

    #plt.figure(figsize=(25,10))
    plt.xlabel('time $t$', fontsize = 20, fontname = "Arial")
    plt.ylabel('Population', fontsize = 20, fontname = "Arial")


    plt.plot(df.index, df.S, marker='o', markerfacecolor='gray', markersize=2, color='skyblue', linewidth=2)

    plt.plot(df.index, df.E, marker='o', markerfacecolor='gray', markersize=2, color='yellow', linewidth=2)


    plt.plot(df.index, df.I, marker='o', markerfacecolor='gray', markersize=2, color='red', linewidth=2)


    plt.plot(df.index, df.R, marker='o', markerfacecolor='gray', markersize=2, color='green', linewidth=2)


    #plt.plot(df.index, df.D, marker='o', markerfacecolor='gray', markersize=2, color='black', linewidth=2)

    #plt.legend(('Susceptible', 'Exposed', 'Infectious','Recovered', 'Dead'),
               #prop={"size":20}, fancybox=True, framealpha=1,
               #shadow=True,loc = 'upper right', ncol = 5)

    plt.gcf().autofmt_xdate() #italics of x label
    #plt.savefig('SEIR_WL.png')
    plt.show()

def plot_SEIR_with_shade(df_min, df_mean, df_max):
    fig, ax = plt.subplots(figsize=(25, 10))

    # plt.figure(figsize=(25,10))
    plt.xlabel('time $t$', fontsize=20, fontname="Arial")
    plt.ylabel('Population', fontsize=20, fontname="Arial")

    days = df_min['Day']  # Assuming Day is common across all DataFrames

    # Plotting the area between min and max
    plt.fill_between(days, df_min.S, df_max.S, color='skyblue', label='S-Min-Max Range', alpha=0.3)
    plt.fill_between(days, df_min.E, df_max.E, color='orange', label='E-Min-Max Range', alpha=0.3)
    plt.fill_between(days, df_min.I, df_max.I, color='red', label='I-Min-Max Range', alpha=0.3)
    plt.fill_between(days, df_min.R, df_max.R, color='green', label='R-Min-Max Range', alpha=0.3)

    # Plotting the average line
    plt.plot(days, df_mean.S, marker='o', markerfacecolor='gray', markersize=2, color='skyblue', linewidth=2)
    plt.plot(days, df_mean.E, marker='o', markerfacecolor='gray', markersize=2, color='orange', linewidth=2)
    plt.plot(days, df_mean.I, marker='o', markerfacecolor='gray', markersize=2, color='red', linewidth=2)
    plt.plot(days, df_mean.R, marker='o', markerfacecolor='gray', markersize=2, color='green', linewidth=2)

    # plt.plot(days, df_mean.S, color='black', label='Average')
    # Adding labels and title
    plt.legend()

    # Show the plot
    plt.show()


def display_Spread_Tree(spread_network):
    import networkx as nx
    # Adding the column names
    spread_network.columns = ["time", "target", "source", "extra"]

    # Drop the 'extra' column if not needed
    spread_network = spread_network.drop(columns=['extra'])

    # Reorganize the columns to match the desired format
    spread_network = spread_network[["target", "source", "time"]]

    G = nx.Graph()

    for i in spread_network[:10].index:
        node_1 = spread_network.iloc[i, 1]  # source
        # print(node_1)
        node_2 = spread_network.iloc[i, 0]  # target

        time_1 = spread_network.iloc[i, -1]
        time_2 = spread_network.iloc[i, -1] + 2

        # print(time)
        if G.has_node(node_1):
            # print(node_1, "has is true")
            # G.add_node(node_1, level = time_1)
            G.add_node(node_2, level=time_2)
            G.add_edge(node_1, node_2)
        else:
            G.add_node(node_1, level=time_1)
            G.add_node(node_2, level=time_2)
            G.add_edge(node_1, node_2)

        pos = nx.multipartite_layout(G, subset_key="level")

        nx.draw(G, pos, node_size=10, width=0.5)

        # shift position a little bit
        # shift = [0.1, 0]
        # shifted_pos ={node: node_pos + shift for node, node_pos in pos.items()}
        pos_attrs = {}
        labels = {}
        for node, coords in pos.items():
            pos_attrs[node] = (coords[0], coords[1] + 0.05)
            labels[node] = node

        ids = []
        for item in range(G.number_of_nodes()):
            ids.append(item)

        node_ids = []
        for n in G:
            # print(n)
            node_ids.append(n)
            # print(G.number_of_nodes())

        # using dictionary comprehension
        # to convert lists to dictionary
        # labels = dict(zip(ids, node_ids))
        import matplotlib.pylab as pl
        nx.draw_networkx_labels(G, pos_attrs, font_size=8, labels=labels, horizontalalignment="center", clip_on=False)
        # adjust frame to avoid cutting text, may need to adjust the value
        # axis = pl.gca()
        # axis.set_xlim([1.5*x for x in axis.get_xlim()])
        # axis.set_ylim([1.5*y for y in axis.get_ylim()])
        # turn off frame
        # pl.axis("off")
        plt.show()
