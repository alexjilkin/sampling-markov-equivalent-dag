import networkx as nx
import random
import hashlib
import time
from profiling import record 
import multiprocessing as mp

memo = {}

def v_func(G, r, v, clique_tree):
        # product of #AMOs for the subproblems
        prod = 1
        subproblems = C(G, set(v))

        results = []

        results = [count(H) for H in subproblems]

        for res in results:
            prod *= res
            
        fp = FP(clique_tree, r, v)

        fp_len = list(map(lambda a: len(a) , fp))
        fp_len.insert(0, 0)
        phi_res =  phi(len(set(v)), 0, fp_len, {})
        # print(f"{v}: phi={phi_res}, fp={fp}, prod={prod}")
        return phi_res * prod

def count(G: nx.Graph, pool=None):
    start = time.process_time()

    hashable_graph = tuple(sorted(G.nodes.items()) + sorted(G.edges.items()))
    G_hash = hashlib.sha256(str(hashable_graph).encode()).hexdigest()
    record('hash', time.process_time() - start)

    try:
        res = memo[G_hash]
        return res
    except KeyError:
        pass
    
    clique_tree = nx.junction_tree(G)
    # clique_tree = maximal_clique_tree(G)
    
    visited = []
    
    # Sort maximal cliques members to acsending tuples
    maximal_cliques = list(map(lambda clique: tuple(sorted(clique)), nx.find_cliques(G)))
    
    # maximal_cliques = list(clique_tree.nodes)

    record('clique_tree', time.process_time() - start)
    r = list(clique_tree.nodes)[0]
    total_sum = 0

    # Divide into subprocesses only at the root
    if pool != None:
        parallel_v = [pool.apply_async(v_func, (G, r, v, clique_tree)) for v in maximal_cliques]
        results = [result.get() for result in parallel_v]

        total_sum += sum(results)
    else: 
        for v in maximal_cliques:
            total_sum += v_func(G, r, v, clique_tree)
        
    memo[G_hash] = total_sum

    return total_sum


def FP(T, r, v):
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

    record('fp', time.process_time() - start)
    
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
    global total_phi

    start = time.process_time()
    if i in pmemo.keys():
        return pmemo[i]
    
    sum = fac(cliquesize - fp[i])
    for j in range (i+1, len(fp)):
        sum -= fac(fp[j]-fp[i]) * phi(cliquesize, j, fp, pmemo)
    pmemo[i] = sum
    record('phi', time.process_time() - start)
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
            L.append(X)
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
    
    record('c', time.process_time() - start)
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
