import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from utils import read_scores_from_file, random_dag
from count import count

from probabilities import R, get_edge_addition_count, score
import random

def propose_add(G: nx.DiGraph) -> nx.DiGraph:
    new_G = G.copy()
    vertices = list(new_G.nodes)
    
    a, b = random.choices(vertices, k=2)
    new_G.add_edge(a, b)

    try:
        nx.find_cycle(new_G)
        return propose_add(G)
    except:
        return new_G

# Gets a UCCG
def sample_markov_equivalent(G: nx.DiGraph):
    M = G.copy().to_undirected()
    
    AMOs = count(M, lambda x, y: None)
    print(AMOs)
    
def main():
    scores = read_scores_from_file('data/boston.jkl')
    G = nx.DiGraph()
    G.add_nodes_from(range(1, len(scores) + 1))

    G = random_dag(G)
    # nx.draw_networkx(G)
    # plt.show()
    sample(G)

    G = nx.DiGraph()
    G.add_nodes_from(range(1, len(scores) + 1))
    sample(G)

    plt.show()

# G is a UCCG
def sample(G: nx.DiGraph):
    A = get_edge_addition_count(G)
    results = []
    G_i = G
    steps = range(200)
    for _ in steps: 
        G_i_plus_1 = propose_add(G_i)

        A = np.min([1, R(G_i, G_i_plus_1)])
        if (np.random.uniform() < A):
            G_i = G_i_plus_1
        results.append(score(G_i))
    
    plt.plot(steps, results)
main()
