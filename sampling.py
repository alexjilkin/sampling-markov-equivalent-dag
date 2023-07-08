import matplotlib.pyplot as plt
import numpy as np
from meeks import CPDAG
from utils import plot, read_scores_from_file
from count import FP, count, get_maximal_cliques, v_func, C
import igraph as ig
import networkx as nx

from probabilities import R, get_edge_addition_count, get_edge_reversal_count, score
import random

def random_dag(G: ig.Graph) -> ig.Graph:
    new_G = G.copy()

    for i in range(23):
        vertices = list(new_G.vs)
    
        a, b = random.sample(vertices, k=2)
        if not new_G.are_connected(b, a) and not new_G.are_connected(a, b):
            new_G.add_edge(a, b)

    if(new_G.is_dag() and score(new_G) != -np.inf):
        return new_G
    else:
        return random_dag(G)
        

def propose_add(G: ig.Graph) -> ig.Graph:

    new_G = G.copy()
    vertices = list(new_G.vs)
    
    a, b = random.sample(vertices, k=2)
    if (new_G.are_connected(a, b) or new_G.are_connected(b, a)):
        return propose_add(G)
    
    new_G.add_edge(a, b)

    if new_G.is_dag():
        return new_G
    
    return propose_add(G)        
    
def propose_markov_equivalent(G: ig.Graph) -> ig.Graph:
    essential_g = CPDAG(G)

    # Create a networkx graph to be used with count()
    U = nx.Graph()

    for e in essential_g.es:
        U.add_edge(e.source, e.target)

    tos = sample_markov_equivalent(U)

    if len(tos) == 0:
        return G
    
    equivalent_G = ig.Graph(directed=True)
    equivalent_G.add_vertices(len(G.vs))
    for to in tos:
        # Direct based on to
        for v in to:
            ids = G.incident(v, mode="all")
        
            for id in ids:
                e = G.es[id]
                if not (e.source in to and e.target in to):
                    continue
                if (equivalent_G.are_connected(e.source, e.target) or equivalent_G.are_connected(e.target, e.source)):
                    continue
                if (to.index(e.source) < to.index(e.target)):
                    equivalent_G.add_edge(e.source, e.target)
                else:
                    equivalent_G.add_edge(e.target, e.source)

    for e in G.es:
        if not (equivalent_G.are_connected(e.source, e.target) or equivalent_G.are_connected(e.target, e.source)):
            equivalent_G.add_edge(e.source, e.target)

    return equivalent_G
    
def propose_remove(G: ig.Graph) -> ig.Graph:
    new_G = G.copy()
    edges = list(new_G.es)
    
    edge = random.choice(edges)
    new_G.delete_edges([edge])

    return new_G

def propose_reverse(G: ig.Graph) -> ig.Graph:
    new_G = G.copy()
    edges = list(new_G.es)
    
    e = random.choice(edges)
    new_G.reverse_edges([e])
    
    if(new_G.is_dag()):
        return new_G
        
    return propose_reverse(G)

# Gets a UCCG
    
def main():
    scores = read_scores_from_file('data/boston.jkl')

    n = 10000

    G = ig.Graph(directed=True)
    G.add_vertices(len(scores))
    G = random_dag(G)

    for i in range(2):
        samples, G_no_markov = sample(G, n)
        plt.plot(np.arange(len(samples)), samples , label=f"Random-{i+1}")

        samples, G_markov = sample(G, n, True)
        plt.plot(np.arange(len(samples)), samples , label=f"Random-{i+1}-markov", linestyle='dashed')

    plt.legend()
    plt.ylim([-22000, -19500])
    plt.show()
    # plot(G_no_markov)
    # plot(G_markov)

# G is a UCCG
def sample(G: ig.Graph, n, markov_equivalent = False):
    scores = []
    G_i = G.copy()
    steps = range(n)

    for i in steps: 
        a = get_edge_addition_count(G_i)
        reverse = get_edge_reversal_count(G_i)
        remove = len(list(G_i.es))
        total = a+reverse+remove
        
        # Choose uniformly from adding, removing or reversing an edge
        proposal_func_name = np.random.choice(['add', 'remove', 'reverse'], p=[a/total, remove/total, reverse/total])
        
        if i!= 0 and i % 500 == 0 and markov_equivalent:
            G_i_plus_1 = propose_markov_equivalent(G_i)
    
            a = set(map(lambda e: (e.source, e.target), G_i.es))
            b = set(map(lambda e: (e.source, e.target), G_i_plus_1.es))  
            # print(score(G_i), score(G_i_plus_1), a - b)

        else:
            G_i_plus_1 = globals()[f'propose_{proposal_func_name}'](G_i)

        A = np.min([1, R(G_i, G_i_plus_1)])
        if (np.random.uniform() < A):
            G_i = G_i_plus_1
        
        scores.append(score(G_i))
        
    return scores, G_i


# G is a the essential graph
def sample_markov_equivalent(U: nx.Graph):
    # For each subgraph, count the AMOs and return the product

    def sub_sample_markov_equivalent(UCCG):
        # pre-process
        AMO = count(UCCG)

        clique_tree = nx.junction_tree(UCCG)
        maximal_cliques = get_maximal_cliques(clique_tree)
        r = maximal_cliques[0]

        p = list(map(lambda v: v_func(UCCG, r, v, clique_tree) / AMO, maximal_cliques))
        
        # Maximal clique drawn with probability proportional to v_func
        v = maximal_cliques[np.random.choice(np.arange(0, len(p)), p=p)]

        K = set(v)
        to = list(K)

        # uniformly drawn permutation of ι(v) without prefix in FP(v, T )
        is_good = False
        while not is_good:
            random.shuffle(to)

            is_good = True
            for fp in FP(clique_tree, r, v):
                if (np.array_equal(to[:len(fp)], fp)):
                    is_good = False
        
        for H in C(UCCG, K):
            to += sub_sample_markov_equivalent(H)
        return to
    
    UCCGs = [U.subgraph(component) for component in nx.connected_components(U)]
    tos = list(map(lambda UCCG: sub_sample_markov_equivalent(UCCG),  UCCGs))

    return tos
main()
