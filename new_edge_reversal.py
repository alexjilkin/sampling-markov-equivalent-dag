from functools import reduce
import random
import igraph as ig
import numpy as np
from utils import plot
from probabilities import P, get_local_score, get_scores

def parent_set_score(Xi, pi):
    return get_local_score(Xi, frozenset(pi))

# Calculates Z (18) returns 
def get_Z1(M:ig.Graph, X) -> (int, list[set]):
    parent_sets = get_scores()[X].keys()
    
    # Checks the descendants to find cycles
    descendants = set(M.subcomponent(X, mode="out")) - set({X})
    parent_sets = list(filter(lambda parent_set: len(parent_set & descendants) == 0, parent_sets))

    return sum_scores(X, parent_sets), parent_sets

def sum_scores(X, parent_sets):
    scores_dict = get_scores()[X]
    scores = [scores_dict[pa] for pa in parent_sets]
    return reduce(np.logaddexp, scores)

# Calculates Z (19)
def get_Z2(M, Xn, Xm) -> (int, list[set]):
    parent_sets = get_scores()[Xn].keys()
    # Checks the descendants to find cycles
    descendants = set(M.subcomponent(Xn, mode="out")) - set({Xn})
    parent_sets = list(filter(lambda parent_set: I(parent_set, Xm) and len(parent_set & descendants) == 0, parent_sets))

    return sum_scores(Xn, parent_sets), parent_sets

def orphan_nodes(M, nodes):
    M_prime = M.copy()
    for node in nodes:
        M_prime.delete_edges([(parent, node) for parent in M.predecessors(node)])

    return M_prime

def I(pa, Xj):
    return Xj in pa

def new_edge_reversal_move(G: ig.Graph):
    M = G.copy()
    if (len(M.es) < 2):
        return G, False
    
    edge = np.random.choice(M.es) 
    Xi, Xj = edge.tuple 

    M_prime = orphan_nodes(M, [Xi, Xj])

    ## Second step, sample parent set for Xi ##
    Z2_i, parent_sets = get_Z2(M_prime, Xi, Xj)
    Q_i_p = np.array([parent_set_score(Xi, parent_set) - Z2_i for parent_set in parent_sets])

    # Normalize probability
    max_prob = np.max(Q_i_p)
    Q_i_p_norm = np.exp(Q_i_p - max_prob)
    Q_i_p_norm /= np.sum(Q_i_p_norm)

    new_pi = np.random.choice(parent_sets, p=Q_i_p_norm)
    M_plus = M_prime.copy()
    edges = [(parent, Xi) for parent in new_pi]
    M_plus.add_edges(edges)

    ## Third step, sample patern set pj ##
    Z1_j, parent_sets = get_Z1(M_plus, Xj)
    Q_j_p = np.array([parent_set_score(Xj, parent_set) - Z1_j for parent_set in parent_sets])
    max_prob = np.max(Q_j_p)
    Q_j_p_norm = np.exp(Q_j_p - max_prob)
    Q_j_p_norm /= np.sum(Q_j_p_norm)

    new_pj = np.random.choice(parent_sets, p=Q_j_p_norm)
    M_tilda = M_plus.copy()
    edges = [(parent, Xj) for parent in new_pj]
    M_tilda.add_edges(edges)

    if (np.random.uniform() < A(M, M_tilda, M_prime, Xi, Xj, Z2_i, Z1_j)):
        return M_tilda, 'REV'
    
    return G, False

# Acceptance rate
def A(M, M_tilda, M_prime, Xi, Xj, Z2_i, Z1_j):
    first = (len(M.es) / len(M_tilda.es))
    second = Z2_i - get_Z2(M_prime, Xj, Xi)[0]

    M_tilda_plus = orphan_nodes(M, [Xi])
    third = Z1_j - get_Z1(M_tilda_plus, Xi)[0]
    # fourth = P(M_tilda) / P(M)

    return np.min([1, first * np.exp(second + third)])