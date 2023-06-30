import networkx as nx
import itertools

import numpy as np

from utils import read_scores_from_file
from scipy.special import binom

def N(G: nx.DiGraph):
    count = 0
    M = G.copy()

    # Add edges
    count += get_edge_addition_count(G)
    count += get_edge_reversal_count(G)

    # Removing edges
    count +=  len(list(M.edges))

    return count

def P(M: nx.DiGraph):
    def f(n, G_i_count):    
        return 1 / binom(n - 1, G_i_count)
    G_i = np.fromiter(map(lambda vertex: len(list(M.predecessors(vertex))), M.nodes), int)
    
    return f(len(G_i), G_i).prod()

     
def R(M_i: nx.DiGraph, M_i_plus_1: nx.DiGraph):
    return (score(M_i_plus_1) - score(M_i)) * (P(M_i_plus_1) / P(M_i)) * (N(M_i_plus_1) / N(M_i))


# Calculate how many edges can be added without creating a cycle
def get_edge_addition_count(G: nx.DiGraph):
    count = 0
    M = G.copy()
    
    # Try adding edges
    for a, b in  itertools.product(M.nodes, repeat=2):
        if(a == b or M.has_edge(a, b) or M.has_edge(b, a)):
            continue
        M.add_edge(a, b)
        try:
            nx.find_cycle(M)
        except:
            count += 1
        M.remove_edge(a, b)
        
    return count

# Calculate how many edges can be added without creating a cycle
def get_edge_reversal_count(G: nx.DiGraph):
    count = 0
    M = G.copy()

    # Reversing edges
    for e in M.edges:
        G.remove_edge(*e)
        G.add_edge(*reversed(e))
        try:
            nx.find_cycle(M)
        except:
            count += 1

        G.remove_edge(*reversed(e))
        G.add_edge(*e)

    return count

scores = read_scores_from_file('data/boston.jkl')

def score(G: nx.DiGraph):
    score = 0
    
    def local_score(node):
        parents = frozenset(G.predecessors(node))
        if (len(parents) == 0):
            return scores[node][frozenset({})]
        
        try:
            res = scores[node][parents]
        except KeyError:
            res = 0
        return res
        
    for node in G.nodes:
        score += local_score(node)
        
    return score
