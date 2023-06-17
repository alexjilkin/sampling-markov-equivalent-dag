from count import count
import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from profiling import print_profiling 
import multiprocessing as mp

def from_file():
    start = time.process_time()

    # file = open('./sample.gr', 'r')
    file = open('./interval-n=1024-nr=1.gr', 'r')
    G = nx.Graph()
    lines = [tuple(map(int, line.strip().split(" "))) for line in file.readlines()]
    nodes_count = lines[0][0]
    edges = lines[1:]
    
    nodes = np.arange(1, nodes_count + 1)
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    start = time.process_time()
    
    # crap = count(G)

    print(f"#AMO={count(G)}")

    print(f"Total time: {time.process_time() - start}")
        
# print(f"#AMO={count(G)}")


from_file()
print_profiling()