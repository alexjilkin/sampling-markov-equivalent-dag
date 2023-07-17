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
    
    x = np.arange(n)
    # figure, axis = plt.subplots(1, 2)

    for i in range(3):
        # random.seed(i * 12)

        samples, G_markov = sample(G, n, True)
        plt.plot(x, samples , label=f"Emtpy-{i+1}-Markov", linestyle='dashed')

        samples, G_no_markov = sample(G, n)
        plt.plot(np.arange(len(samples)), samples , label=f"Empty-{i}")
    # axis[1].hist(samples, bins=100)

    plt.legend()
    plt.show()

main()