import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import hashlib
import time

memo = {}

total_clique_tree = 0
total_hash = 0

def count(G: nx.Graph):
    global total_clique_tree, total_hash

    start = time.process_time()

    hashable_graph = tuple(sorted(G.nodes.items()) + sorted(G.edges.items()))
    G_hash = hashlib.sha256(str(hashable_graph).encode()).hexdigest()
    total_hash += time.process_time() - start
    try:
        res = memo[G_hash]
        return res
    except KeyError:
        pass
    
    print(f"Hash - {time.process_time() - start}")

    clique_tree = nx.junction_tree(G)
    # clique_tree = maximal_clique_tree(G)
    
    visited = []
    
    # Sort maximal cliques members to acsending tuples
    # maximal_cliques = list(map(lambda clique: tuple(sorted(clique)), nx.find_cliques(G)))
    maximal_cliques = list(clique_tree.nodes)

    total_clique_tree += (time.process_time() - start)
    r = list(clique_tree.nodes)[0]
    sum = 0

    Q = [r]
    visited = [r]

    # print(f"Finding junction tree - {time.process_time() - start}")
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

total_FP = 0

def FP(T, r, v):
    global total_FP

    start = time.process_time()
    res = []

    path = list(nx.shortest_path(T, r, v))
    p = len(path)

    for i in range(0, p - 1):
        intersection = {value for value in path[i] if value in path[i + 1]}
        if (intersection.issubset(set(v))):
            res.append(intersection)
    
    # Converted to set for uniqness and sorted
    res = set(tuple(sorted(s)) for s in res)

    total_FP += (time.process_time() - start)
    
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

total_phi = 0
def phi(cliquesize, i, fp, pmemo):
    global total_phi

    start = time.process_time()
    if i in pmemo.keys():
        return pmemo[i]
    
    sum = fac(cliquesize - fp[i])
    for j in range (i+1, len(fp)):
        sum -= fac(fp[j]-fp[i]) * phi(cliquesize, j, fp, pmemo)
    pmemo[i] = sum
    total_phi += (time.process_time() - start)
    return sum


def maximal_clique_tree(G: nx.Graph):
    clique_tree = nx.Graph()
    maximal_cliques = list(map(lambda clique: tuple(sorted(clique)), nx.find_cliques(G)))

    clique_tree.add_nodes_from(maximal_cliques)

    # Builds graph out of maximal cliques by content intersection
    for clique1 in maximal_cliques:
        for clique2 in maximal_cliques:
            if (clique1 != clique2 and len(set(clique1).intersection(clique2)) > 0):
                # if(len([edge for edge in clique_tree.edges() if clique1 in edge]) == 0):
                clique_tree.add_edge(clique1, clique2)

    clique_tree = nx.maximum_spanning_tree(clique_tree, algorithm="kruskal")
    return clique_tree

total_C = 0

# C_G(K) - algorithm 4
def C(G: nx.Graph, K: set):
    global total_C

    start = time.process_time()
    S = [K, set(G.nodes) - K]

    to = []
    L = []
    output = []
    
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
    
    total_C += (time.process_time() - start)
    return output


def from_file():
    start = time.process_time()

    # file = open('./sample.gr', 'r')
    file = open('./interval-n=1024-nr=1.gr', 'r')
    G = nx.Graph()
    lines = [tuple(map(int, line.strip().split(" "))) for line in file.readlines()]
    nodes_count = lines[0][0]
    edges = lines[1:]
    
    nodes = np.arange(1, nodes_count + 1)
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    print(f"Read graph - {time.process_time() - start}")
    start = time.process_time()
    print(f"#AMO={count(G)}")

    print(f"#AMO - {time.process_time() - start}")
        
# G = nx.Graph()

# G.add_nodes_from([1, 2, 3, 4, 5, 6])
# G.add_edges_from([(1, 2), (1, 3), (2,3), (2,5), (2, 6), (2,4), (3, 4), (3, 5), (3,6), (4, 5), (5, 6)])

# print(f"#AMO={count(G)}")

from_file()

print(f"total_C={total_C} \n total_FP={total_FP} \n total_phi={total_phi} \n total__clique_tree={total_clique_tree} \n total_hash={total_hash}")
