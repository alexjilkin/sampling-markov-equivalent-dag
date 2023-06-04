import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

memo = []
# print(r)
    # print(list(clique_tree.neighbors(r)))
   

def count(G: nx.Graph):
    if G in memo:
        return G
    
    clique_tree = nx.junction_tree(G)
    r = list(clique_tree.nodes)[0]

    sum = 0
    Q = [r]

    # nx.draw_networkx(G)
    nx.draw_networkx(clique_tree)
    plt.show()
    while len(Q) > 0:
        v = Q.pop(0)
        # Q.append(list(clique_tree.neighbors(v)))
        prod = 1
        C_G_k = C(G, set(v))
        print(C_G_k)


# C_G(K) - algorithem 4
def C(G: nx.Graph, K: set):
    S = [K, set(G.nodes) - K]

    to = []
    L = []
    result = []
    while len(S) != 0:
        X = S[0]
        # Should be arbitrary
        v = random.choice(list(X))
        to.append(v)

        is_in_L = any((v in el) for el in L)
        if (not is_in_L and (v not in K)):
            L.append(X)
            # TODO: Output the undirected components of G[X].
            result.append(X.copy())
        
        X.remove(v)
        S_new = []
        for Si in S:
            Nv = set(G.neighbors(v))
            S_new.append(Si.intersection(Nv))
            S_new.append(Si - Nv)
        
        S = list(filter(lambda S_new_i: len(S_new_i) > 0, S_new))
    
    return result

    
# def phi(clique_tree, v):


G = nx.Graph()

G.add_nodes_from([1, 2, 3, 4, 5, 6, 7])
G.add_edges_from([(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4), (3,5), (3,6),(4,5), (4,6), (5,6), (5, 7), (6, 7)])

count(G)

# def sample(G)
#     clique