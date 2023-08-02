from functools import reduce
import random
import igraph as ig
import numpy as np
from utils import plot
from probabilities import get_local_score, get_scores

def calculate_score(Xi, pi):
    return get_local_score(Xi, frozenset(pi))

def get_Z1(M:ig.Graph, Xn):
    scores_dict = get_scores()[Xn]
    parent_sets = scores_dict.keys()
    scores = []

    for parent_set in parent_sets:
        edges = [(parent, Xn) for parent in parent_set]
        M.add_edges(edges)
        if (M.is_dag()):
            scores.append(scores_dict[parent_set])
        M.delete_edges(edges)
    
    return reduce(np.logaddexp, scores)

def get_Z2(M, Xn, Xm):
    scores_dict = get_scores()[Xn]
    parent_sets = scores_dict.keys()
    parent_sets = list(filter(lambda parent_set: Xm in parent_set, parent_sets))
    scores = []

    for parent_set in parent_sets:
        edges = [(parent, Xn) for parent in parent_set]
        M.add_edges(edges)
        if (M.is_dag()):
            scores.append(scores_dict[parent_set])

        M.delete_edges(edges)
    return reduce(np.logaddexp, scores)

def orphan_nodes(M, nodes):
    M_prime = M.copy()
    for node in nodes:
        M_prime.delete_edges([(parent, node) for parent in M.predecessors(node)])

    return M_prime

def I(pa, Xj):
    return Xj in pa

def delta(M, X, pas):
    edges = [(pa, X) for pa in pas]

    M.add_edges(edges)
    is_dag = M.is_dag()
    M.delete_edges(edges)

    return is_dag

def new_edge_reversal_move(G: ig.Graph):
    M = G.copy()
    if (len(M.es) < 2):
        return G, False
    
    edge = np.random.choice(M.es)  # Randomly select one edge
    Xi, Xj = edge.tuple 

    M_prime = orphan_nodes(M, [Xi, Xj])

    # Second step, sample parent set for Xi
    parent_sets = get_scores()[Xi].keys()

    descendants = set(M_prime.subcomponent(Xi, mode="out")) - set({Xi})
    parent_sets = list(filter(lambda parent_set: I(parent_set, Xj) and len(parent_set & descendants) == 0, parent_sets))

    Z2_i = get_Z2(M_prime, Xi, Xj)
    Q_i_p = np.array([calculate_score(Xi, parent_set) - Z2_i for parent_set in parent_sets])

    # Normalize probability
    max_prob = np.max(Q_i_p)
    Q_i_p_norm = np.exp(Q_i_p - max_prob)
    Q_i_p_norm /= np.sum(Q_i_p_norm)

    new_pi = np.random.choice(parent_sets, p=Q_i_p_norm)
    M_plus = M_prime.copy()
    edges = [(parent, Xi) for parent in new_pi]
    M_plus.add_edges(edges)

    # Third step, sample patern set pj
    parent_sets = get_scores()[Xj].keys()
    descendants = set(M_plus.subcomponent(Xj, mode="out")) - set({Xj})
    parent_sets = list(filter(lambda parent_set: len(parent_set & descendants) == 0, parent_sets))

    Z1_j = get_Z1(M_plus, Xj)
    Q_j_p = np.array([calculate_score(Xj, parent_set) - Z1_j for parent_set in parent_sets])
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

def A(M, M_tilda, M_prime, Xi, Xj, Z2_i, Z1_j):
    first = (len(M.es) / len(M_tilda.es))
    second = Z2_i - get_Z2(M_prime, Xj, Xi)
    third = Z1_j - get_Z1(orphan_nodes(M, [Xi]), Xi)

    res = first * np.exp(second + third)
    return np.min([1,  res ])