import sys
import matplotlib.pyplot as plt
import numpy as np
from markov_equivalent import CPDAG, get_markov_equivalent
from utils import get_es_diff, get_graph_hash_ig, plot
import igraph as ig

from probabilities import R, get_scores, score
import random

# Increase recursion limit from 10^3
sys.setrecursionlimit(10**4)

max_parents = 5
    
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
def sample(G: ig.Graph, size, is_markov_equivalent = False):
    G_i = G.copy()

    steps = []
    AMOs = ''
    equivalence_classes_dict = {}

    for i in range(size):
        i = len(steps)
        G_i_plus_1, step_type = propose_next(G_i, is_markov_equivalent, i)

        if (step_type != ''):
            current_score = score(G_i)
            proposed_score = score(G_i_plus_1)

            A = np.min([1, R(G_i, G_i_plus_1)]) 

            if (np.random.uniform() <= A):
                print(f'{i} {current_score:.2f} {proposed_score:.2f} {AMOs} {get_es_diff(G_i_plus_1, G_i)}, {step_type}')

                G_i = G_i_plus_1
            # If rejected, try for an equivalence step
            elif is_markov_equivalent and np.random.uniform() <= 0.25:
                G_i_plus_1, AMOs = propose_markov_equivalent(G_i)
                proposed_score = score(G_i_plus_1)
                print(f'{i} {score(G_i):.2f} {proposed_score:.2f} {AMOs} {get_es_diff(G_i_plus_1, G_i)}, equivalence')
                G_i = G_i_plus_1


            G_cpdag = CPDAG(G_i)
            G_cpdag_hash = get_graph_hash_ig(G_cpdag)
            if G_cpdag_hash not in equivalence_classes_dict:
                equivalence_classes_dict[G_cpdag_hash] = 0

            equivalence_classes_dict[G_cpdag_hash] += 1

        steps.append(G_i)
    return steps, G_i, equivalence_classes_dict

def propose_next(G_i: ig.Graph, is_markov_equivalent, i):
    a, b = random.sample(list(G_i.vs), k=2)
    G_i_plus_1 = G_i.copy()
    
    if (G_i.are_connected(a, b)):
        G_i_plus_1.delete_edges([(a,b)])
        return G_i_plus_1, 'remove'
    elif (G_i.are_connected(b, a)):
        G_i_plus_1.delete_edges([(b, a)])
        G_i_plus_1.add_edges([(a, b)])

        if G_i_plus_1.is_dag():
            return G_i_plus_1, 'reverse'
    else:
        G_i_plus_1.add_edges([(a, b)])
        if G_i_plus_1.is_dag():
            return G_i_plus_1, 'add'
    
    return G_i, ''
