import networkx as nx
import matplotlib.pyplot as plt
from utils import read_graph_from_file

def main():
    G = read_graph_from_file('sample.gr')
    sample(G)

# G is a UCCG
def sample(G: nx.Graph):
    d_G = nx.DiGraph(G)

    nx.draw_networkx(d_G, arrows=True)
    plt.show()

main()
