import random
import igraph as ig
from probabilities import get_local_score
from utils import plot
import itertools
from functools import reduce
import numpy as np
from scipy.special import binom
import copy

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

# Only parent sets with at least one member in the partition element 
# immediately to the right need to be included.
def P_v(partitions: list[set], v: int):
    flat_vertices = list(itertools.chain.from_iterable(partitions))
    n = len(flat_vertices)

    parent_sets = get_permissible_parent_sets(partitions, v)
    
    scores = [get_local_score(v, pa, n) for pa in parent_sets]
    return reduce(np.logaddexp, scores)

def get_permissible_parent_sets(partitions: list[set], v: int):
    partition_index = 0
    v_index_for_searching = 0
    
    # Find the partition containing v and its index.
    for i, partition in enumerate(partitions):
        if v in partition:
            partition_index = i
            break
        v_index_for_searching += len(partition)

    # If the vertex is in the last partition, return empty set
    if partition_index == len(partitions) - 1:
        return [frozenset()]

    # Get the vertices to the right of the current vertex's partition.
    vertices_to_right = list(itertools.chain.from_iterable(partitions[partition_index + 1:]))

    # Generator to yield permissible parent sets
    def parent_sets_generator():
        partition_to_the_right = partitions[partition_index + 1]
        for size in range(1, max_parents_size + 1):
            for p in itertools.permutations(vertices_to_right, size):
                parent_set = frozenset(p)
                if len(parent_set.intersection(partition_to_the_right)) > 0:
                    yield parent_set

    parent_sets = list(parent_sets_generator())
    parent_sets.append(frozenset())
    return parent_sets

def P_partition(partitions: list[set]) -> list[float]:
    flat_vertices = list(itertools.chain.from_iterable(partitions))

    scores = {v: P_v(partitions, v) for v in flat_vertices}
    return scores

def nbd_sum(partitions: list[set], m: int):
        return sum([sum([binom(len(partitions[i - 1]), c) for c in range(1, len(partitions[i - 1]))]) for i in range(1, m + 1)])

def nbd(partitions: list[set], m: int):
    return m - 1 + nbd_sum(partitions, m)

def sample_partition(prev_partitions: list[set], prev_scores: dict[int, float]):
    partitions = copy.deepcopy(prev_partitions)
    scores: dict[int, float] = copy.deepcopy(prev_scores)

    m = len(partitions)
    nbd = m - 1 + nbd_sum(partitions, m)

    j = random.randint(1, nbd)
    vertices_to_rescore = set()

    if (j < m):
        # Join partitions
        partition_1 = partitions.pop(j - 1)
        partition_2 = partitions.pop(j - 1)

        new_partition = partition_1 | partition_2
        partitions.insert(j-1, new_partition)
        vertices_to_rescore |= partition_1
        if j-2 >= 0:
            vertices_to_rescore |= partitions[j-2]

    else:
        # Split partition
        i_min = find_i_min(partitions, j)
        c_min = find_c_min(partitions, j, i_min)
        new_partition = set(random.sample(list(partitions[i_min - 1]), c_min))
        partitions[i_min - 1] -= new_partition
        partitions.insert(i_min - 1, new_partition)

        vertices_to_rescore |= new_partition
        if (i_min - 2 >= 0):
            vertices_to_rescore |= partitions[i_min - 2]

    for v in vertices_to_rescore:
        scores[v] = P_v(partitions, v)

    return partitions, scores

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


def sample_dag(partitions: list[set], v_count):
    G = ig.Graph(directed=True)
    G.add_vertices(v_count)
    flat_vertices = list(itertools.chain.from_iterable(partitions))
    n = len(flat_vertices)

    for v in flat_vertices:
        parent_sets = get_permissible_parent_sets(partitions, v)
        # target_sum = P_v(partitions, v)
        target_sum = sum([get_local_score(v, pa, n) for pa in parent_sets])

        current_sum = 0
        j = np.random.uniform(target_sum, 0)

        for pa_i in parent_sets:
            current_sum = current_sum + get_local_score(v, frozenset(pa_i), n)

            if current_sum < j:
                edges = [(p, v) for p in pa_i]
                G.add_edges(edges)
                break
        # print(sum)
    
    return G

        