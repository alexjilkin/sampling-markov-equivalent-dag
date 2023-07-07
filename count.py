import networkx as nx
import random
import time
from functools import reduce
from operator import mul
import numpy as np
from utils import get_graph_hash

memo = {}
v_func_memo = {}

def v_func(G, r, v, clique_tree, record):
    try:
        res = v_func_memo[frozenset(v)]
        return res
    except KeyError:
        pass
    
    start = time.time()
    K = set(v)
    subproblems = C(G, K)
    
    # record('C_G', time.time() - start)

    results = [count(H, record) for H in subproblems]

    prod = reduce(mul, results) if len(results) > 0 else 1
    
    fp = FP(clique_tree, r, v)

    fp_lens = list(map(lambda a: len(a) , fp))
    fp_lens.insert(0, 0)

    # print(f"{v}: phi={phi_res}, fp={fp}, prod={prod}")
    res = phi(len(set(v)), 0, fp_lens, {}) * prod

    v_func_memo[frozenset(v)] = res
    
    return res

def count(G: nx.Graph, record=lambda x, y: None, pool=None):
    start = time.time()

    G_hash = get_graph_hash(G)

    # G_hash = nx.weisfeiler_lehman_graph_hash(G)
    record('hash', time.time() - start)

    try:
        res = memo[G_hash]
        return res
    except KeyError:
        pass
    
    # Get connected components of the graph
    G_subs = [G.subgraph(component) for component in nx.connected_components(G)]
    results = []

    # For each subgraph, count the AMOs and return the product
    for G_sub in G_subs:
        result = 0
        start = time.time()
        clique_tree = nx.junction_tree(G_sub)

        # clique_tree = maximal_clique_tree(G)
        # maximal_cliques = list(map(lambda clique: tuple(sorted(clique)), nx.find_cliques(G)))
        maximal_cliques = get_maximal_cliques(clique_tree)

        r = maximal_cliques[0]
        record('clique_tree', time.time() - start)

        # Divide into subprocesses only at the root
        # if pool != None:
        #     parallel_v_results = [pool.apply_async(v_func, (G_sub, r, v, maximal_clique_tree, record)) for v in maximal_cliques]

        #     result += sum([r.get() for r in parallel_v_results])
        # else: 
        for v in maximal_cliques:
            result += v_func(G_sub, r, v, clique_tree, record)

        results.append(result)

    # Product of each component
    result = reduce(lambda x, y: x*y, results)
    memo[G_hash] = result

    return result

def FP(T, r, v):
    res = []
    
    path = list(nx.shortest_path(T, r, v))
    p = len(path)
    # except nx.exception.NetworkXNoPath:
    #     return []

    for i in range(0, p - 1):
        intersection = {value for value in path[i] if value in path[i + 1]}
        if (intersection.issubset(set(v))):
            res.append(intersection)
    
    # Converted to set for uniqness and sorted
    res = set(tuple(sorted(s)) for s in res)
    
    return list(res)

fmemo = {}

def fac(n):
    if n in fmemo:
        return fmemo[n]
    
    if n <= 0:
        return 0
    if n == 1:
        return 1
    
    res = fac(n - 1) * n
    fmemo[n] = res
    return res

def phi(cliquesize, i, fp, pmemo):
    if i in pmemo:
        return pmemo[i]
    
    sum = fac(cliquesize - fp[i])
    for j in range (i+1, len(fp)):
        sum -= fac(fp[j]-fp[i]) * phi(cliquesize, j, fp, pmemo)
    pmemo[i] = sum
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


# C_G(K) - algorithm 4
def C(G: nx.Graph, K: set):
    S = [K, set(G.nodes) - K]

    to = []
    L = set()
    output = []
    
    while S:
        X = next(s for s in S if len(s) != 0)
        if X is None:
            break

        v = random.choice(list(X))
        to.append(v)

        if not any(v in el for el in L) and (v not in K):
            L.add(frozenset(X))
            # Output the undirected components of G[X].
            subgraphs = [G.subgraph(component) for component in nx.connected_components(G.subgraph(X))]

            output.extend(subgraphs)
        
        X.remove(v)
        S_new = []
        neighbors_v = set(G.neighbors(v))
        for Si in S:
            S_new.append(Si & neighbors_v)
            S_new.append(Si - neighbors_v)
        
        S = [Si for Si in S_new if Si]
    
    return output

def get_maximal_cliques(clique_tree: nx.Graph):
    maximal_cliques = []
    for clique1 in clique_tree.nodes:
        is_maximal = True
        for clique2 in clique_tree.nodes:
            if (clique1 != clique2 and set(clique1).issubset(clique2)):
                is_maximal = False
        if is_maximal:
            maximal_cliques.append(clique1)

    return maximal_cliques
