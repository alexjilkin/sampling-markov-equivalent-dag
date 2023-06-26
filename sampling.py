import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from utils import read_scores_from_file
import random

def main():
    scores = read_scores_from_file('data/boston.jkl')
    G = nx.DiGraph()
    G.add_nodes_from(range(1, len(scores) + 1))

    nodes_list = list(G.nodes)
    a, b = random.choices(nodes_list, k = 2)
    G.add_edge(a, b)

    nx.draw_networkx(G)
    plt.show()
    sample(G, scores)

# G is a UCCG
def sample(G: nx.DiGraph, scores):
    

    # nx.draw_networkx(d_G, arrows=True)
    # labels = nx.get_edge_attributes(d_G,'weight')
    # pos = nx.spring_layout(d_G)
    # nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    # plt.show()

    print(score(G, scores))



def score(G: nx.DiGraph, scores):
    score = 1
    def local_score(node):
        parents = frozenset(G.predecessors(node))
        if (len(parents) == 0):
            return scores[node][frozenset({})]
        
        return scores[node][parents]
        
    for node in G.nodes:
        score = score * local_score(node)
        
    return score

main()
