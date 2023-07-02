import itertools
import igraph as ig

import numpy as np

from utils import read_scores_from_file, get_graph_hash_ig
from scipy.special import binom

get_graph_hash = get_graph_hash_ig


def N(G: ig.Graph):
    count = 0
    M = G

    # Add edges
    count += get_edge_addition_count(G)
    count += get_edge_reversal_count(G)

    # Removing edges
    count += len(list(M.es))

    return count

def P(M: ig.Graph):
    def f(n, G_i_count):    
        return 1 / binom(n - 1, G_i_count)
    G_i_count = np.fromiter(map(lambda vertex: len(list(M.predecessors(vertex))), M.vs), int)
    
    return f(len(G_i_count), G_i_count).prod()

     
def R(M_i: ig.Graph, M_i_plus_1: ig.Graph):
    return np.exp(score(M_i_plus_1) - score(M_i)) * (P(M_i_plus_1) / P(M_i)) * (N(M_i) / N(M_i_plus_1))


# edge_addition_memo = {}
# Calculate how many edges can be added without creating a cycle
def get_edge_addition_count(G: ig.Graph):
    # graph_hash = get_graph_hash(G)
    # try:
    #     return edge_addition_memo[graph_hash]
    # except KeyError:
    #     pass

    count = 0
    M = G.copy()
    
    # Try adding edges
    for a, b in  itertools.product(M.vs, repeat=2):
        if(a == b or M.are_connected(a, b) or M.are_connected(b, a)):
            continue
        M.add_edge(a, b)
        if (M.is_dag()):
            count += 1
            
        M.delete_edges([(a, b)])
    
    # edge_addition_memo[graph_hash] = count
    return count

# edge_reversal_memo = {}

# Calculate how many edges can be added without creating a cycle
def get_edge_reversal_count(G: ig.Graph):
    # graph_hash = get_graph_hash(G)
    # try:
    #     return edge_reversal_memo[graph_hash]
    # except KeyError:
    #     pass

    count = 0
    M = G.copy()

    # Reversing edges
    for e in M.es:
        G.delete_edges([e])
        G.add_edge(e.target, e.source)
        if (G.is_dag()):
            count += 1

        G.delete_edges([(e.target, e.source)])
        G.add_edge(e.source, e.target)

    # edge_reversal_memo[graph_hash] = count
    return count

scores = read_scores_from_file('data/boston.jkl')

# score_memo = {}
def score(G: ig.Graph):
    # graph_hash = get_graph_hash(G)
    # try:
    #     res = score_memo[graph_hash]
    #     return res
    # except KeyError:
    #     pass

    score = 0
    
    def local_score(node):
        parents = frozenset(G.predecessors(node))
        if (len(parents) == 0):
            return scores[node.index + 1][frozenset({})]
        
        try:
            res = scores[node.index + 1][parents]
        except KeyError:
            res = 0
        return res
        
    for node in G.vs:
        score += local_score(node)

    # score_memo[graph_hash] = score
    return score
