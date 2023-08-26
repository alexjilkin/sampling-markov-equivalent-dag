import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from count import count, get_maximal_cliques
import math

def better_count(G: nx.Graph):
    # G = nx.Graph()
    # G.add_edges_from([(1,2), (2,3), (1, 3), (2,4), (2,5), (2, 6), (3, 4), (3, 5), (3,6), (6,5), (5,4)])
    # # G.add_edges_from([(1,2),(2,3), (3, 4), (4, 1), (1,3), (2,4)])
    # # G.add_edges_from([(2,3), (3, 4), (4, 1), (1,3), (2,4)])
    # # G.add_edges_from([(1, 2), (1, 3)])

    clique_tree = nx.junction_tree(G)
    maximal_cliques = get_maximal_cliques(clique_tree)
    sum = 0

    for c in maximal_cliques:
        sum += math.factorial(len(c))
    print(maximal_cliques)
    nx.draw_networkx(clique_tree)
    plt.show()
    print(count(G))
    print(sum)
# file = open('./data/sample.gr', 'r')
file = open(f"./data/subtree-logn/n=32.gr", 'r')
G = nx.Graph()
lines = [tuple(map(int, line.strip().split(" "))) for line in file.readlines()]
nodes_count = lines[0][0]
edges = lines[1:]

nodes = np.arange(1, nodes_count + 1)
G.add_nodes_from(nodes)
G.add_edges_from(edges)

amo = better_count(G)