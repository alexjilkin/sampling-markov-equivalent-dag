import networkx as nx
import numpy as np
def read_graph_from_file(filename):

    # file = open('./sample.gr', 'r')
    file = open(filename, 'r')
    G = nx.Graph()
    lines = [tuple(map(int, line.strip().split(" "))) for line in file.readlines()]
    nodes_count = lines[0][0]
    edges = lines[1:]
    
    nodes = np.arange(1, nodes_count + 1)
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    return G