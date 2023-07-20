import sys
import matplotlib.pyplot as plt
import numpy as np
from markov_equivalent import get_markov_equivalent
from utils import get_es_diff, plot
import igraph as ig

from probabilities import R, get_scores, score
import random

# Increase recursion limit from 10^3
sys.setrecursionlimit(10**4)

max_parents = 3
    
def propose_add(G: ig.Graph) -> ig.Graph:
    new_G = G.copy()
    a_s = list(new_G.vs)
    b_s = list(filter(lambda v: len(G.predecessors(v)) < max_parents, new_G.vs))
    
    random.shuffle(a_s)
    random.shuffle(b_s)

    for a in a_s:
        for b in b_s:
            if (a == b):
                continue

            if (new_G.are_connected(a, b) or new_G.are_connected(b, a)):
                return False
            
            new_G.add_edge(a, b)

            if new_G.is_dag():
                return new_G
            
            return False  

def propose_markov_equivalent(G: ig.Graph) -> ig.Graph:
    return get_markov_equivalent(G)
    
def propose_remove(G: ig.Graph) -> ig.Graph:
    new_G = G.copy()

    e = random.choice(list(new_G.es))
    new_G.delete_edges([e])

    return new_G

def propose_reverse(G: ig.Graph) -> ig.Graph:
    new_G = G.copy()
    edges = list(new_G.es)
    
    e = random.choice(edges)
    new_G.reverse_edges([e])
    
    if(new_G.is_dag()):
        return new_G
        
    return False
    
# G is a UCCG
def sample(G: ig.Graph, size, markov_equivalent = False):
    G_i = G.copy()

    steps = []
    AMOs = 1
    base_prob = 0.00001
    prob = 1 / 15
    
    while len(steps) < size:
        i = len(steps)
        n = len(list(G_i.vs))
        add = n * (n - 1)
        E = len(list(G_i.es))
        reverse = E 
        remove = E
        total = add+remove+reverse

        # Choose uniformly from adding, removing or reversing an edge
        proposal_func = np.random.choice([propose_add, propose_remove, propose_reverse], p=[add/total, remove/total, reverse/total])

        if markov_equivalent:
            proposal_func = propose_markov_equivalent if np.random.uniform() <= prob  else proposal_func
    
        if (proposal_func == propose_markov_equivalent):
            G_i_plus_1, AMOs = proposal_func(G_i)
            print(AMOs)
        else:
            G_i_plus_1 = proposal_func(G_i)

        # Rejection sampling
        if (not G_i_plus_1):
            continue

        current_score = score(G_i)
        proposed_score = score(G_i_plus_1)

        A = np.min([1, R(G_i, G_i_plus_1)]) 

        if (np.random.uniform() <= A):
            score_delta = proposed_score - current_score
            # if (score_delta > 2 and proposal_func != propose_markov_equivalent):
                # prob = base_prob

            print(f'{i} {current_score:.1f} {proposed_score:.1f} {get_es_diff(G_i_plus_1, G_i)} {proposal_func.__name__}')
            G_i = G_i_plus_1
        # else:
            # prob = prob + base_prob if prob <= 0.05 else prob

        steps.append(G_i)
        
    return steps, G_i
