import matplotlib.pyplot as plt
import numpy as np
from utils import read_scores_from_file, random_dag
from count import count
import igraph as ig

import cProfile
import snakeviz

from probabilities import R, get_edge_addition_count, score
import random

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
def sample_markov_equivalent(G: ig.Graph):
    M = G.copy().to_undirected()
    
    AMOs = count(M, lambda x, y: None)
    print(AMOs)
    
def main():
    scores = read_scores_from_file('data/boston.jkl')

    n = 1000
    steps = range(n)

    G = ig.Graph(directed=True)
    G.add_vertices(len(scores))

    plt.plot(steps, sample(G, n), label="Empty")

    plt.legend()
    plt.show()

# G is a UCCG
def sample(G: ig.Graph, n=200):
    scores = []
    G_i = G
    steps = range(n)

    for i in steps: 
        a = get_edge_addition_count(G_i)
        r = len(list(G_i.es))

        # Choose uniformly from adding, removing or reversing an edge
        proposal_func_name = np.random.choice(['add', 'remove', 'reverse'], p=[a/(a+2*r), r/(a+2*r), r/(a+2*r)])
        
        # print(propose_func)
        G_i_plus_1 = globals()[f'propose_{proposal_func_name}'](G_i)

        A = np.min([1, R(G_i, G_i_plus_1)])
        if (np.random.uniform() < A):
            G_i = G_i_plus_1
            
        scores.append(score(G_i))
        if (i % 500 == 0):
            print(i)
    
    return scores

# profiler = cProfile.Profile()
# profiler.enable()
main()
# profiler.disable()

# profiler.dump_stats('sampling_profile_results.prof')
# snakeviz.stats('sampling_profile_results.prof')
