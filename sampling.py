import sys
import matplotlib.pyplot as plt
import numpy as np
from markov_equivalent import CPDAG, get_markov_equivalent, test_top_orders_distribution
from new_edge_reversal import new_edge_reversal_move
# from new_edge_reversal import new_edge_reversal_move
from utils import get_es_diff, get_graph_hash_ig, plot
import igraph as ig

from probabilities import R, score
import random

# Increase recursion limit from 10^3
sys.setrecursionlimit(10**4)

def propose_markov_equivalent(G: ig.Graph) -> ig.Graph:
    return get_markov_equivalent(G)

def count_equivalence_classes(steps):
    equivalence_classes_dict = {}
    for G, _ in steps:
        CPDAG_undirected, CPDAG_directed = CPDAG(G)
        G_cpdag_hash = get_graph_hash_ig(CPDAG_undirected) + get_graph_hash_ig(CPDAG_directed)
        if G_cpdag_hash not in equivalence_classes_dict:
            equivalence_classes_dict[G_cpdag_hash] = 0

        equivalence_classes_dict[G_cpdag_hash] += 1
    return equivalence_classes_dict

# G is a UCCG
def sample(G: ig.Graph, size, is_markov_equivalent = False, markov_prob = 0.1, is_REV=False):
    G_i = G.copy()

    steps = []
    AMOs = ''
    
    for i in range(int(size)):
        # Maybe remove i > 100
        G_i_plus_1, step_type = propose_next(G_i, is_markov_equivalent, markov_prob, i > 100 and is_REV)       

        current_score = score(G_i)
        proposed_score = score(G_i_plus_1)

        is_changed = False    
        if (step_type == 'REV'):
            print(f'{i} {current_score:.2f} {proposed_score:.2f} {AMOs} {get_es_diff(G_i_plus_1, G_i)}, {step_type}')
            G_i = G_i_plus_1    
        elif (step_type):
            A = np.min([1, R(G_i, G_i_plus_1)]) 
            if (np.random.uniform() <= A):
                print(f'{i} {current_score:.2f} {proposed_score:.2f} {AMOs} {get_es_diff(G_i_plus_1, G_i)}, {step_type}')
                G_i = G_i_plus_1

        steps.append((G_i, current_score))
    return steps, count_equivalence_classes(steps)

def propose_next(G_i: ig.Graph, is_markov_equivalent, markov_prob, is_REV):
    a, b = random.sample(list(G_i.vs), k=2)
    G_i_plus_1 = G_i.copy()

    if (is_REV and np.random.uniform() < 0.06):
        return new_edge_reversal_move(G_i_plus_1)
    if is_markov_equivalent and np.random.uniform() < markov_prob:
        G_i_plus_1, AMOs = propose_markov_equivalent(G_i)
        return G_i_plus_1, 'equiv'
    
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
    
    return G_i, False
