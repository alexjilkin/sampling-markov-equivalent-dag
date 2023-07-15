import itertools
import igraph as ig
import numpy as np

from utils import plot, read_scores_from_file
from scipy.special import binom

def N(G: ig.Graph):
    return get_edge_addition_count(G) + get_edge_reversal_count(G) + len(list(G.es))

def P(M: ig.Graph):
    def f(n, G_i_count):    
        return 1 / binom(n - 1, G_i_count)
    G_i_count = np.fromiter(map(lambda v: len(list(M.predecessors(v))), M.vs), int)
    
    return f(len(list(M.vs)), G_i_count).prod()

     
def R(M_i: ig.Graph, M_i_plus_1: ig.Graph):
    proposed_score = score(M_i_plus_1)
    current_score = score(M_i)

    if (proposed_score == -np.inf):
        return 0

    # Prevent overlow
    if (proposed_score - current_score > 250):
        exp = 10000
    else:
        exp = np.exp(proposed_score - current_score)

    res = exp * (P(M_i_plus_1) / P(M_i)) * (N(M_i) / N(M_i_plus_1))
    return res  

# Calculate how many edges can be added without creating a cycle
def get_edge_addition_count(G: ig.Graph):
    n = len(G.vs)

    # Because of DAG topological ordering
    return ((n*(n-1)) / 2) - len(G.es)

def other_count(G):
    count = 0
    M = G.copy()

    # Try adding edges
    for a, b in  itertools.product(M.vs, repeat=2):
        if(a == b or M.are_connected(a, b) or M.are_connected(b, a)):
            continue
        
        M.add_edges([(a, b)])
        if (M.is_dag()):
            count += 1
            
        M.delete_edges([(a, b)])
    
    return count

# Calculate how many edges can be added without creating a cycle
def get_edge_reversal_count(G: ig.Graph):
    count = 0
    M = G.copy()

    # Reversing edges
    for e in M.es:
        # a, b = e.source, e.target
        M.reverse_edges([e])
        if (M.is_dag()):        
            count += 1
        M.reverse_edges([e])

    return count

scores = read_scores_from_file('data/boston.jkl')

def get_scores():
    return scores

def score(G: ig.Graph):
    score = 0
    
    def get_local_score(node):
        # Adjust from 0 to 1 counting system, boston starts from 1 but child-5000 starts from 0
        parents = frozenset(map(lambda x: x + 1, G.predecessors(node)))
        
        try:
            res = scores[node.index][parents]
        except KeyError:
            res = -np.inf
        return res
        
    for node in G.vs:
        local_score = get_local_score(node)
        
        # If it is inf, just return
        if (local_score == -np.inf):
            return local_score
        
        score += local_score

    return score
