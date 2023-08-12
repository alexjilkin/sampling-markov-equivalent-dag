import random
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

def nbd_sum(partitions: list[set], m: int):
        return sum([sum([binom(len(partitions[i - 1]), c) for c in range(1, len(partitions[i - 1]))]) for i in range(1, m + 1)])

def sample_partition(partitions: list[set]):
    m = len(partitions)
    nbd = m - 1 + nbd_sum(partitions, m)

    j = np.random.randint(1, nbd)

    if (j < m):
        new_partition = partitions.pop(j - 1) | partitions.pop(j - 1)
        partitions.insert(j-1, new_partition)
    else:
        i_min = find_i_min(partitions, j)
        c_min = find_c_min(partitions, j, i_min)
        new_partition = set(random.sample(list(partitions[i_min - 1]), c_min))
        partitions[i_min - 1] -= new_partition
        partitions.insert(i_min - 1, new_partition)

def find_i_min(partitions: list[set], j):
    m = len(partitions)
    sum = 0
    i_min = 0
    while sum < j:
        i_min += 1
        sum = m - 1 + nbd_sum(partitions, i_min)
        
    return i_min

def find_c_min(partitions: list[set], j, i_min):
    m = len(partitions)
    base_sum = nbd_sum(partitions, i_min - 1)
    res = 0
    c_min = 0
    while res < j:
        c_min += 1
        res = m - 1 + base_sum + sum([binom(len(partitions[i_min - 1]), c) for c in range(1, c_min + 1)])
        
    return c_min


