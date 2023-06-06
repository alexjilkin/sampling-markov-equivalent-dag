import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import math

memo = {}
# print(r)
    # print(list(clique_tree.neighbors(r)))
   

def count(G: nx.Graph):
    if G in memo:
        return G
    
    clique_tree = nx.junction_tree(G)
    visited = []
    
    r = list(clique_tree.nodes)[0]

    sum = 0
    Q = [r]

    # nx.draw_networkx(G)
    # print(r)
    # nx.draw_networkx(clique_tree)
    plt.show()
    while len(Q) > 0:
        v = Q.pop(0)
        visited.append(v)
        neighbours = list(filter(lambda neighbour: neighbour not in visited, clique_tree.neighbors(v)))
        Q.extend(neighbours)

        # product of #AMOs for the subproblems
        prod = 1
        for H in C(G, set(v)):
            res = count(H)
            prod = prod * res
            
        fp = FP(clique_tree, r, v)
         # Add zero to ease calculations
        fp = set(tuple(s) for s in fp)
        fp = list(map(set, fp))
        fp.append({})
        
        fp_len = list(map(lambda a: len(a) , fp))
        fp_len.reverse()
        phi_res =  phi(len(set(v)), 0, fp_len, {})
        print(f"{v}: phi={phi_res}, prod={prod}")
        sum += phi_res * prod 
        
    memo[G] = sum
    
    return sum


def FP(T, r, v):
    res = []
    if (r == v):
        return res
    
    path = list(nx.shortest_path(T, r, v))
    p = len(path)

    for i in range(0, p - 1):
        intersection = {value for value in path[i] if value in path[i + 1]}
        res.append(intersection)
    
    return res

fmemo = {}

def fac(n):
    if n in fmemo.keys():
        return fmemo[n]
    
    if n == -1:
        return 0
    if n == 1:
        return 1
    
    res = fac(n - 1) * n
    fmemo[n] = res
    return res

def phi(cliquesize, i, fp, pmemo):
    if i in pmemo.keys():
        return pmemo[i]
    
    sum = fac(cliquesize - fp[i])
    for j in range (i+1, len(fp)):
        sum -= fac(fp[j]-fp[i]) * phi(cliquesize, j, fp, pmemo)
    pmemo[i] = sum
    return sum

# C_G(K) - algorithm 4
def C(G: nx.Graph, K: set):
    S = [K, set(G.nodes) - K]

    to = []
    L = []
    output = []
    visited = []
    
    while len(S) != 0:
        X = list(filter(lambda s: len(s) != 0, S))[0]
        v = random.choice(list(X))
        to.append(v)

        is_in_L = any((v in el) for el in L)
        if (not is_in_L and (v not in K)):
            L.append(X.copy())
            # Output the undirected components of G[X].
            components = nx.connected_components(G.subgraph(X))
            subgraphs = [G.subgraph(component) for component in components]

            output += subgraphs
        
        X.remove(v)
        S_new = []
        for Si in S:
            Nv = set(G.neighbors(v))
            S_new.append(Si.intersection(Nv))
            S_new.append(Si - Nv)
        
        S = list(filter(lambda S_new_i: len(S_new_i) > 0, S_new))
    
    return output

    
G = nx.Graph()

G.add_nodes_from([1, 2, 3, 4, 5, 6])
G.add_edges_from([(1, 2), (1, 3), (2,3), (2,5), (2, 6), (2,4), (3, 4), (3, 5), (3,6), (4, 5), (5, 6)])

# G.add_nodes_from([1, 2, 3, 4, 5, 6, 7])
# G.add_edges_from([(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4), (3,5), (3,6),(4,5), (4,6), (5,6), (5, 7), (6, 7)])
print(f"#AMO={count(G)}")

# def sample(G)
#     clique