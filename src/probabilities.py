import igraph as ig
import numpy as np
from utils import plot, read_scores_from_file
from scipy.special import binom, logsumexp
from itertools import chain, combinations
import random


def N(G: ig.Graph):
    return get_edge_addition_count(G) + G.ecount() + G.ecount()


def P(M: ig.Graph):
    def f(n, G_i_count):
        return 1 / binom(n - 1, G_i_count)

    G_i_count = np.fromiter(
        map(lambda v: len(list(M.predecessors(v))), M.vs), int)

    return f(len(list(M.vs)), G_i_count).prod()


def R(M_i: ig.Graph, M_i_plus_1: ig.Graph, current_score, proposed_score):
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


def get_edge_reversal_count(G: ig.Graph):
    return len(G.es)


scores = []


def init_scores(name):
    global scores

    scores = read_scores_from_file(f'data/scores/{name}.jkl')


def init_pruned_scores():
    global scores

    vertices = list(scores.keys())

    for i in vertices:
        prune_scores(i, scores)


def get_scores():
    return scores


def get_pruned_scores():
    return scores


def psi(i, j, S: frozenset[int]):
    Rs = np.array([frozenset(subset) for subset in chain.from_iterable(combinations(list(S), r)
                                                                       for r in range(len(S)+1))
                  if j in subset])
    res = [pi(i, R)*w(R, S) for R in Rs]
    return logsumexp(res)


beta_R = 0.3
K = 3
eps = -300


def w(R, S):
    return (1+beta_R)**(len(R)-K) * (beta_R)**(len(S)-len(R))


def pi(v, pa_i):
    # local scores without prior
    k = len(pa_i)

    try:
        res = scores[v][pa_i]
    except KeyError:
        res = -np.inf

    return res


def prune_scores(i, scores):
    prune_count = 0

    for S in list(scores[i].keys()):
        if (len(S) == 0):
            break

        is_prune = True
        for j in list(S):
            # Opposite sign because of log prob
            if (pi(i, S) >= (eps + psi(i, j, S))):
                is_prune = False

        if (is_prune):
            del scores[i][S]
            prune_count += 1

    print(f'At {i} pruned {prune_count}')


def get_local_score(v, pa_i, n):
    k = len(pa_i)

    try:
        res = scores[v][pa_i]

        # Use Koivisto prior
        prior = np.log(1 / binom(n, k))
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

        score += local_score

    return score
