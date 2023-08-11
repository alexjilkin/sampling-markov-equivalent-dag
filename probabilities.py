import igraph as ig
import numpy as np
from utils import plot, read_scores_from_file
from scipy.special import binom

def N(G: ig.Graph):
    return get_edge_addition_count(G) + G.ecount() +  G.ecount()

# Koivisto prior
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
        exp = 1
    else:
        exp = np.exp(proposed_score - current_score)

    # res = exp * (P(M_i_plus_1) / P(M_i)) * (N(M_i) / N(M_i_plus_1))
    # return exp * (P(M_i_plus_1) / P(M_i))
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

def get_local_score(v, pa_i, n):
    k = len(pa_i)
    
    try:
        res = scores[v][pa_i]
        prior = np.log( 1 / binom(n, k))
        res += prior
    except KeyError:
        res = -np.inf

    return res

def score(G: ig.Graph):
    score = 0
    n = len(G.vs)

    for v in G.vs:
        pi = frozenset(map(lambda x: x, G.predecessors(v)))
        local_score = get_local_score(v.index, pi, n)
        
        # If it is inf, just return
        if (local_score == -np.inf):
            return local_score
        
        k = len(G.predecessors(v))
        
        score += local_score 

    return score
    