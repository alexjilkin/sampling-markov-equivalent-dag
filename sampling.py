import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from utils import read_graph_from_file

def main():
    G = read_graph_from_file('sample.gr', True)
    d_G = nx.DiGraph(G)
    sample(d_G)

# G is a UCCG
def sample(G: nx.DiGraph):
    

    # nx.draw_networkx(d_G, arrows=True)
    # labels = nx.get_edge_attributes(d_G,'weight')
    # pos = nx.spring_layout(d_G)
    # nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    # plt.show()

    print(score(G))



def score(G: nx.DiGraph):
    score = 1
    def local_score(node):
        parents_score = list(map(lambda in_edge: G.get_edge_data(*in_edge)['weight'], G.in_edges(node)))
        return np.array(parents_score).sum()
    
    for node in G.nodes:
        score = score * local_score(node)
        
    return np.abs(score)
main()
