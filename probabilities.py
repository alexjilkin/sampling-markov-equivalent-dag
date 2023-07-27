import igraph as ig
import numpy as np
from utils import plot, read_scores_from_file
from scipy.special import binom

def N(G: ig.Graph):
    return get_edge_addition_count(G) + G.ecount() +  G.ecount()

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
    if (proposed_score - current_score > 700):
        exp = 10e15
    else:
        exp = np.exp(proposed_score - current_score)

    # res = exp * (P(M_i_plus_1) / P(M_i)) * (N(M_i) / N(M_i_plus_1))
    # res = exp * (P(M_i_plus_1) / P(M_i))
    return exp  

# Calculate how many edges can be added without creating a cycle
def get_edge_addition_count(G: ig.Graph):
    n = G.vcount()
    
    return n*(n-1)

# Calculate how many edges can be added without creating a cycle
def get_edge_reversal_count(G: ig.Graph):
    return len(G.es)

scores = []

def init_scores(name):
    global scores
    scores = read_scores_from_file(f'data/scores/{name}.jkl')

def get_scores():
    return scores

def score(G: ig.Graph):
    score = 0
    
    def get_local_score(node):
        # Adjust from 0 to 1 counting system, boston starts from 1 but child-5000 starts from 0
        parents = frozenset(map(lambda x: x, G.predecessors(node)))
        
        try:
            res = scores[node.index][parents]
        except KeyError:
            res = -np.inf
        return res
        
    for v in G.vs:
        local_score = get_local_score(v)
        
        # If it is inf, just return
        if (local_score == -np.inf):
            return local_score
        
        score += local_score

    return score + np.log(P(G))
