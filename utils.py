import random
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
import hashlib
from itertools import chain
import igraph as ig


def read_graph_from_file(filename, random_weights=False):

    # file = open('./sample.gr', 'r')
    file = open(filename, 'r')
    G = nx.Graph()
    lines = [tuple(map(int, line.strip().split(" "))) for line in file.readlines()]
    nodes_count = lines[0][0]
    edges = lines[1:]
    
    nodes = np.arange(1, nodes_count + 1)
    G.add_nodes_from(nodes)
    for edge in edges:
        weight = np.round(np.random.normal(), 2) if random_weights else 1

        G.add_edge(edge[0], edge[1], weight=weight)
    G.add_edges_from(edges)

    return G

# def random_dag(G: ig.Graph) -> ig.Graph:
#     new_G = G.copy()

#     for i in range(25):
#         vertices = list(new_G.vs)
    
#         a, b = random.sample(vertices, k=2)
#         if not new_G.are_connected(b, a) and not new_G.are_connected(a, b):
#             new_G.add_edge(a, b)

#     if(new_G.is_dag() and score(new_G) != -np.inf):
#         return new_G
#     else:
#         return random_dag(G)

def read_scores_from_file(filename):
    file = open(filename, 'r')
    lines = [tuple(line.strip().split(" ")) for line in file.readlines()]
    n = int(lines[0][0])

    lines = lines[1:]
    scores = {}

    for i in range(0, n):
        v = int(lines[0][0])
        j_count = int(lines[0][1])
        scores[v] = {}

        for j in range(1, j_count + 1):
            score = float(lines[j][0])
            
            parents = frozenset(map(int, lines[j][2:]))
            scores[v][parents] = score
        
        lines = lines[j_count + 1:]

    return scores

def get_graph_hash(G: nx.Graph) -> str:
    hashable_graph = tuple(chain(G.nodes.items(), G.edges.items()))
    return hashlib.sha256(str(hashable_graph).encode()).hexdigest()

def get_graph_hash_ig(G: ig.Graph) -> str:
    hashable_graph = tuple(chain(G.vs, G.es))
    return hashlib.sha256(str(hashable_graph).encode()).hexdigest()

memo = {}

def memo_by_graph(G: nx.DiGraph, key: str, value):
    if (key not in memo):
        memo[key] = {}

def plot(G, title=""):
    _, ax = plt.subplots()
    visual_style = {}
    visual_style["vertex_label"] = list(map(lambda x: x, G.vs.indices))
    ig.plot(G, target=ax, **visual_style)
    plt.show()

def get_es_diff(G1: ig.Graph, G2: ig.Graph):
    G1_set = set(map(lambda e: (e.source, e.target), G1.es))
    G2_set = set(map(lambda e: (e.source, e.target), G2.es))

    both = G1_set.intersection(G2_set)
    return (G1_set - both).union(G2_set - both)