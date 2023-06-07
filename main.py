import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import hashlib

memo = {}
def count(G: nx.Graph):
    # G_hash = nx.graph_hashing.weisfeiler_lehman_graph_hash(G)

    hashable_graph = tuple(sorted(G.nodes.items()) + sorted(G.edges.items()))
    G_hash = hashlib.sha256(str(hashable_graph).encode()).hexdigest()

    try:
        res = memo[G_hash]
        return res
    except KeyError:
        pass
    
    clique_tree = nx.Graph()
    visited = []
    
    # Filter out cliques that are subsets of others
    maximal_cliques = list(map(lambda clique: tuple(sorted(clique)), nx.find_cliques(G)))
    clique_tree.add_nodes_from(maximal_cliques)

    # Builds graph out of maximal cliques by content intersection
    for clique1 in maximal_cliques:
        for clique2 in maximal_cliques:
            if (clique1 != clique2 and len(set(clique1).intersection(clique2)) > 0):
                if(len([edge for edge in clique_tree.edges() if clique1 in edge]) == 0):
                    clique_tree.add_edge(clique1, clique2)
                    break

    r = maximal_cliques[0]
    # print(f"r={r}")
    sum = 0

    Q = [r]
    visited = [r]

    # nx.draw_networkx(clique_tree)
    # plt.show()
    while len(Q) > 0:
        v = Q.pop(0)
        
        neighbors = list(filter(lambda neighbor: neighbor not in visited, clique_tree.neighbors(v)))
        Q.extend(neighbors)
        visited += neighbors

        # Count only maximal cliques
        if (v not in maximal_cliques):
            continue
        
        # product of #AMOs for the subproblems
        prod = 1
        for H in C(G, set(v)):
            res = count(H)
            prod = prod * res
            
        fp = FP(clique_tree, r, v)

        fp_len = list(map(lambda a: len(a) , fp))
        fp_len.insert(0, 0)
        phi_res =  phi(len(set(v)), 0, fp_len, {})
        # print(f"{v}: phi={phi_res}, fp={fp}, prod={prod}")
        sum += phi_res * prod
        
    memo[G_hash] = sum
    
    return sum

def FP(T, r, v):
    res = []

    path = list(nx.shortest_path(T, r, v))
    p = len(path)

    for i in range(0, p - 1):
        intersection = {value for value in path[i] if value in path[i + 1]}
        if (intersection.issubset(set(v))):
            res.append(intersection)
    
    # Converted to set for uniqness and sorted
    res = set(tuple(sorted(s)) for s in res)
    
    return list(res)

fmemo = {}

def fac(n):
    if n in fmemo.keys():
        return fmemo[n]
    
    if n <= 0:
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
    
    while len(S) != 0:
        X = list(filter(lambda s: len(s) != 0, S))[0]
        # v = list(X)[0]
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


def from_file():
    # file = open('./sample.gr', 'r')
    file = open('./interval-n=512-nr=1.gr', 'r')
    G = nx.Graph()
    lines = [tuple(map(int, line.strip().split(" "))) for line in file.readlines()]
    nodes_count = lines[0][0]
    edges = lines[1:]
    
    nodes = np.arange(1, nodes_count + 1)
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    print(f"#AMO={count(G)}")
        
# G = nx.Graph()

# G.add_nodes_from([1, 2, 3, 4, 5, 6])
# G.add_edges_from([(1, 2), (1, 3), (2,3), (2,5), (2, 6), (2,4), (3, 4), (3, 5), (3,6), (4, 5), (5, 6)])

# print(f"#AMO={count(G)}")

from_file()
