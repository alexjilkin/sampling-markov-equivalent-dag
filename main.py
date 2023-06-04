import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

memo = []
# print(r)
    # print(list(clique_tree.neighbors(r)))
    # nx.draw_networkx(clique_tree)
    # plt.show()

def count(G: nx.Graph):
    if G in memo:
        return G
    
    clique_tree = nx.junction_tree(G)
    r = list(clique_tree.nodes)[0]

    sum = 0
    Q = [r]

    while len(Q) > 0:
        v = Q.pop(0)
        Q.append(clique_tree.neighbors(v))
        prod = 1


        fo



# C_G(K) - algorithem 4
def C(G: nx.Graph, K: nx.Graph):
    n = G.number_of_nodes

    for i in range(1, n + 1):
        if i < 

    
def phi(clique_tree, v):


G = nx.Graph()

G.add_nodes_from([1, 2, 3, 4])
G.add_edges_from([(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)])

count(G)

# def sample(G)
#     clique