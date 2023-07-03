import matplotlib.pyplot as plt
import numpy as np
from utils import plot, read_scores_from_file
from count import count
import igraph as ig
import math

from probabilities import R, get_edge_addition_count, get_edge_reversal_count, score
import random

def random_dag(G: ig.Graph) -> ig.Graph:
    new_G = G.copy()

    for i in range(10):
        vertices = list(new_G.vs)
    
        a, b = random.sample(vertices, k=2)
        if not new_G.are_connected(b, a):
            new_G.add_edge(a, b)

    if(new_G.is_dag() and score(new_G) != -np.inf):
        return new_G
    else:
        return random_dag(G)
        

def propose_add(G: ig.Graph) -> ig.Graph:
    
    new_G = G.copy()
    vertices = list(new_G.vs)
    
    a, b = random.sample(vertices, k=2)
    if (new_G.are_connected(a, b) or new_G.are_connected(b, a)):
        return propose_add(G)
    
    new_G.add_edge(a, b)

    if new_G.is_dag():
        return new_G
    
    return propose_add(G)        
      
def propose_remove(G: ig.Graph) -> ig.Graph:
    new_G = G.copy()
    edges = list(new_G.es)
    
    edge = random.choice(edges)
    new_G.delete_edges([edge])

    return new_G

def propose_reverse(G: ig.Graph) -> ig.Graph:
    new_G = G.copy()
    edges = list(new_G.es)
    
    e = random.choice(edges)
    new_G.reverse_edges([e])
    
    if(new_G.is_dag()):
        return new_G
        
    return propose_reverse(G)

# Gets a UCCG
def sample_markov_equivalent(G: ig.Graph):
    M = G.copy().to_undirected()
    
    AMOs = count(M, lambda x, y: None)
    print(AMOs)
    
def main():
    scores = read_scores_from_file('data/boston.jkl')

    n = 2000
    steps = range(n)

    G = ig.Graph(directed=True)
    G.add_vertices(len(scores))
    G = random_dag(G)
    samples = sample(G, n)
    plt.plot(np.arange(len(samples)), samples , label="Random")

    G = ig.Graph(directed=True)
    G.add_vertices(len(scores))
    samples = sample(G, n)
    plt.plot(np.arange(len(samples)), samples , label="Empty")

    plt.legend()
    plt.ylim([-22000, -19500])
    plt.show()

# G is a UCCG
def sample(G: ig.Graph, n):
    scores = []
    G_i = G
    steps = range(n)

    for i in steps: 
        a = get_edge_addition_count(G_i)
        reverse = get_edge_reversal_count(G_i)
        remove = len(list(G_i.es))
        total = a+reverse+remove
        
        # Choose uniformly from adding, removing or reversing an edge
        proposal_func_name = np.random.choice(['add', 'remove', 'reverse'], p=[a/total, remove/total, reverse/total])
        
        # print(propose_func)
        G_i_plus_1 = globals()[f'propose_{proposal_func_name}'](G_i)

        A = np.min([1, R(G_i, G_i_plus_1)])
        if (np.random.uniform() < A):
            G_i = G_i_plus_1
        
        scores.append(score(G_i))
        # if(scores[-1] > -21400):
        #     plot(G_i)
    
    return scores

main()
