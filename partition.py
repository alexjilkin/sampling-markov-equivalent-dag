import igraph as ig
from utils import plot
import itertools

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
    
def P_partition(partitions: list[set], v: int):
    current_permutation = list(itertools.chain.from_iterable(partitions))

    # Find the index of vertices "right" to the tested vertex
    index_for_searching = 0 
    for partition in partitions:
        index_for_searching += len(partition)

        if (v in partition):
            break

    vertices =  current_permutation[index_for_searching:]

    parent_sets = [p for size in range(1, max_parents_size + 1) for p in itertools.permutations(vertices, size)]

    print('s')
