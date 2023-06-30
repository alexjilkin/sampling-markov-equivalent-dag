import networkx as nx
import numpy as np
import hashlib
from itertools import chain

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

def read_scores_from_file(filename):

    # file = open('./sample.gr', 'r')
    file = open(filename, 'r')
    G = nx.Graph()
    lines = [tuple(line.strip().split(" ")) for line in file.readlines()]
    n = int(lines[0][0])

    lines = lines[1:]
    scores = {}

    for i in range(1, n + 1):
        v = lines[0][0]
        j_count = int(lines[0][1])
        scores[i] = {}

        for j in range(1, j_count + 1):
            score = float(lines[j][0])
            
            parents = frozenset(map(int, lines[j][2:]))
            scores[i][parents] = score
        
        lines = lines[j_count + 1:]

    return scores

def random_dag(G: nx.DiGraph) -> nx.DiGraph:
    new_G = G.copy()

    nodes_list = list(new_G.nodes)
    np.random.shuffle(nodes_list)
    
    for i in range(len(nodes_list) - 1):
        a, b = nodes_list[i], nodes_list[i + 1]
        new_G.add_edge(a, b)

    try:
        nx.find_cycle(new_G)
        return random_dag(G)
    except:
        return new_G

def hash_graph(G: nx.Graph) -> str:
    hashable_graph = tuple(chain(G.nodes.items(), G.edges.items()))
    return hashlib.sha256(str(hashable_graph).encode()).hexdigest()