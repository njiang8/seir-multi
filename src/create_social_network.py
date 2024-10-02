import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import collections
import csv


def create_edges(x, g):
    if len(x) <= 5:
        sw = nx.complete_graph(len(x))
    else:
        sw = nx.newman_watts_strogatz_graph(len(x), 4, 0.3)
    sw = nx.relabel_nodes(sw, dict(zip(sw.nodes(), x.index.values)))# what's this line for?
    g.add_edges_from(sw.edges())


def create_network(people, type):
    g = nx.Graph()
    g.add_nodes_from(people.index)
    if type == "school":
        grouped = people[people.age < 18].groupby('wp')
        grouped.apply(lambda x: create_edges(x, g))
    if type == 'work':
        grouped = people[people.age >= 18].groupby('wp')
        grouped.apply(lambda x: create_edges(x, g))
    if type == 'hhold':
        grouped = people.groupby('hhold')
        grouped.apply(lambda x: create_edges(x, g))
    return g

def get_neighbors(x, g):
    return [n for n in g.neighbors(x)]

def to_csv(g, population, output_name): #args: social networktype, population, output filename
    col1 = list(population.index)
    col2 = population.index.map(lambda x: get_neighbors(x, g))
    col2 = list(col2)
    for i in range(len(col2)):
        col2[i] = [col1[i]] + col2[i]
    with open(output_name + '.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(col2)


#Visualization of Networks
def display_degree(G, tname):#social network graph, figure tile name
    #pre calculate
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
    # print ("Degree sequence", degree_sequence)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())

    #create figure
    figure, ax = plt.subplots(figsize=(12, 8))

    plt.bar(deg, cnt, width=0.80, color='#43a2ca')
    plt.title(tname, fontsize=20, fontname="Arial")
    plt.ylabel("Frequency", fontsize=16, fontname="Arial")
    plt.xlabel("Degree", fontsize=16, fontname="Arial")

    ax.set_xticks([d for d in deg])
    ax.set_xticklabels(deg)

    rects = ax.patches

    # For each bar: Place a label
    for rect in rects:
        # Get X and Y placement of label from rect.
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        # Number of points between bar and label. Change to your liking.
        space = 5
        # Vertical alignment for positive values
        va = 'bottom'

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = 'top'

        # Use Y value as label and format number with one decimal place
        label = "{:.1f}".format(y_value)

        # Create annotation
        plt.annotate(
            label,  # Use `label` as label
            (x_value, y_value),  # Place label at end of the bar
            xytext=(0, space),  # Vertically shift label by `space`
            textcoords="offset points",  # Interpret `xytext` as offset in points
            ha='center',  # Horizontally center label
            va=va)  # Vertically align label differently for
        # positive and negative values.