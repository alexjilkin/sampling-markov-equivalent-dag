from count import count
import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from profiling import print_profiling, record
import multiprocessing as mp

vertices = [16, 32, 64, 256]

def from_file():
    times = []
    graph_type = 'subtree-logn'
    for vertex_count in vertices:
        start = time.time()

        # file = open('./sample.gr', 'r')
        file = open(f"./{graph_type}/n={vertex_count}.gr", 'r')
        G = nx.Graph()
        lines = [tuple(map(int, line.strip().split(" "))) for line in file.readlines()]
        nodes_count = lines[0][0]
        edges = lines[1:]
        
        nodes = np.arange(1, nodes_count + 1)
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        start = time.time()
        
        amo = count(G, record, mp.Pool(mp.cpu_count()))

        runtime = time.time() - start
        print(f"|V|={vertex_count}\n#AMO={amo}")
        times.append(runtime)
        print(f"Total time: {runtime}")
        print_profiling()

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xticks(vertices)
    ax.set_xticklabels(vertices)

    ax.set_xscale('log', base=2)

    ax.plot(vertices, times, marker='o')
    ax.set_xlabel('Number of vertices')
    ax.set_ylabel('Seconds')

    plt.title(graph_type)
    # plt.show()

if __name__ == '__main__':
    from_file()