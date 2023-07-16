import sys
import matplotlib.pyplot as plt
import numpy as np
from markov_equivalent import get_markov_equivalent
from utils import get_es_diff, plot
import igraph as ig

from probabilities import R, get_edge_addition_count, get_edge_reversal_count, get_scores, score
import random

# Increase recursion limit from 10^3
sys.setrecursionlimit(10**4)

def propose_add(G: ig.Graph) -> ig.Graph:
    new_G = G.copy()
    vertices = list(filter(lambda v: len(G.neighborhood(v)) < 6,new_G.vs))
    
    a, b = random.sample(vertices, k=2)
    if (new_G.are_connected(a, b) or new_G.are_connected(b, a)):
        return propose_add(G)
    
    new_G.add_edge(a, b)

    if new_G.is_dag():
        return new_G
    
    return propose_add(G)        

def propose_markov_equivalent(G: ig.Graph) -> ig.Graph:
    return get_markov_equivalent(G)
    
def propose_remove(G: ig.Graph) -> ig.Graph:
    new_G = G.copy()
    edges = list(new_G.es)
    
    e = random.choice(edges)
    new_G.delete_edges([e])

    return new_G

def propose_reverse(G: ig.Graph) -> ig.Graph:
    new_G = G.copy()
    edges = list(new_G.es)
    
    e = random.choice(edges)
    new_G.reverse_edges([e])
    
    if(new_G.is_dag()):
        return new_G
        
    return propose_reverse(G)
    
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
        proposal_func = np.random.choice([propose_add, propose_remove, propose_reverse], p=[a/total, remove/total, reverse/total])

        if (markov_equivalent and i > 2000):
            proposal_func = np.random.choice([proposal_func, propose_markov_equivalent], p=[0.95, 0.05])

        G_i_plus_1 = proposal_func(G_i)
       

        A = np.min([1, R(G_i, G_i_plus_1)]) 
        if (np.random.uniform() < A):
            if(proposal_func == propose_markov_equivalent):
                print(score(G_i), score(G_i_plus_1), get_es_diff(G_i_plus_1, G_i), i, proposal_func.__name__)
            G_i = G_i_plus_1

        scores.append(score(G_i))

        
    return scores, G_i

