import random
import igraph as ig
from matplotlib import pyplot as plt
import numpy as np

from probabilities import get_scores, score
from sampling import sample

def main():
    n = 5000

    G = ig.Graph(directed=True)
    G.add_vertices(len(get_scores()))
    
    for i in range(2):
        random.seed(i * 132)

        samples, G_markov = sample(G, n, True)
        plt.plot(np.arange(len(samples)), samples , label=f"Emtpy-{i+1}-markov", linestyle='dashed')

        samples, G_no_markov = sample(G, n)
        plt.plot(np.arange(len(samples)), samples , label=f"Empty-{i}")

    plt.legend()
    plt.show()

main()