import numpy as np
from scipy.special import logsumexp
from itertools import chain, combinations


K = None
beta_R = None
eps = None
scores = None
b = None


def init_pruning(_scores, _K, _eps, _b):
    global scores, K, eps, beta_R, b
    scores = _scores
    K = _K
    beta_R = 1 / K
    eps = _eps
    b = _b


def prune_scores():
    global scores, eps

    orig_count = count_scores(scores)
    vertices = list(scores.keys())

    for i in vertices:
        prune_scores_node(i)

    pruned_count = count_scores(scores)
    print(f'b={b} From {orig_count} to {pruned_count}')


def count_scores(scores):
    count = 0
    for v in list(scores.keys()):
        count += len(scores[v])
    return count


def psi(i, j, S: frozenset[int]):
    global scores

    Rs = np.array([frozenset(subset)
                   for subset in chain.from_iterable(combinations(list(S), r)
                                                     for r in range(len(S)+1))
                  if j in subset])
    res = [pi(i, R)+np.log(w(R, S)) for R in Rs]
    return logsumexp(res)


def w(R, S):
    return (1+beta_R)**(len(R)-K) * (beta_R)**(len(S)-len(R))


def pi(v, pa_i):
    global scores, b

    # local scores without prior
    k = len(pa_i)

    try:
        res = scores[v][pa_i]
    except KeyError:
        res = -np.inf

    return res*b


def prune_scores_node(i):
    global scores

    prune_count = 0

    for S in list(scores[i].keys()):
        if (len(S) == 0):
            break

        is_prune = True
        for j in list(S):
            if (pi(i, S) >= (np.log(eps) + psi(i, j, S))):
                is_prune = False
                break

        if (is_prune):
            del scores[i][S]
            prune_count += 1
