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
    
def propose_remove(G: nx.DiGraph) -> nx.DiGraph:
    new_G = G.copy()
    edges = list(new_G.edges)
    
    edge = random.choice(edges)
    new_G.remove_edge(*edge)

    return new_G

def propose_reverse(G: nx.DiGraph) -> nx.DiGraph:
    new_G = G.copy()
    edges = list(new_G.edges)
    
    edge = random.choice(edges)
    new_G.remove_edge(*edge)
    new_G.add_edge(*reversed(edge))
    
    try:
        nx.find_cycle(new_G)
        return propose_reverse(G)
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

    n = 200
    steps = range(n)

    plt.plot(steps, sample(G, n), label="Random")

    G = nx.DiGraph()
    G.add_nodes_from(range(1, len(scores) + 1))
    plt.plot(steps, sample(G, n), label="Empty")

    plt.legend()
    plt.show()

# G is a UCCG
def sample(G: nx.DiGraph, n=200):
    A = get_edge_addition_count(G)
    scores = []
    G_i = G
    steps = range(n)
    for _ in steps: 
        a = get_edge_addition_count(G_i)
        r = len(list(G_i.edges))

        # Choose uniformly from adding, removing or reversing an edge
        propose_func = np.random.choice([propose_add, propose_reverse, propose_reverse], p=[a/(a+2*r), r/(a+2*r), r/(a+2*r)])

        G_i_plus_1 = propose_func(G_i)


        A = np.min([1, R(G_i, G_i_plus_1)])
        if (np.random.uniform() < A):
            G_i = G_i_plus_1
        scores.append(score(G_i))
    
    return scores
main()
