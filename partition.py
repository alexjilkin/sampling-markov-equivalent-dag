import igraph as ig
from probabilities import get_local_score
from utils import plot
import itertools
from functools import reduce
import numpy as np
from scipy.special import binom

max_parents_size = 3

def create_pratition(G: ig.Graph) -> list[set]:
    G_t: ig.Graph = G.copy()
    partitions = []

    for v in G_t.vs:
        v['original_index'] = v.index

    while len(G_t.vs) > 0:
        outpoints = [v for v in G_t.vs if G_t.degree(v, mode='in') == 0]
        partitions.insert(0, set([v['original_index'] for v in outpoints]))

        G_t.delete_vertices(outpoints)
    
    return partitions
    
def P_v(partitions: list[set], v: int):
    flat_vertices = list(itertools.chain.from_iterable(partitions))
    n = len(flat_vertices)

    # Find the index of vertices "right" to the tested vertex
    index_for_searching = 0 
    for partition in partitions:
        index_for_searching += len(partition)

        if (v in partition):
            break

    vertices =  flat_vertices[index_for_searching:]

    if (len(vertices) == 0):
        return 0
    
    parent_sets = [p for size in range(1, max_parents_size + 1) for p in itertools.permutations(vertices, size)]
    scores = [get_local_score(v, frozenset(p), n) for p in parent_sets]
    return reduce(np.logaddexp, scores)

    
def P_partition(partitions: list[set]):
    flat_vertices = list(itertools.chain.from_iterable(partitions))

    scores = [P_v(partitions, v) for v in flat_vertices]
    return sum(scores)

def sample_partition(partitions: list[set]):
    def nbd_sum(m):
        return sum([sum([binom(len(partitions[i]), c) for c in range(1, len(partitions[i]) + 1)]) for i in range(0, m)])
    
    m = len(partitions)
    nbd = m - 1 + nbd_sum(m)

    j = np.random.randint(1, nbd)

    if (j < m):
        print('join')
    else:
     
     flat_vertices = list(itertools.chain.from_iterable(partitions))

