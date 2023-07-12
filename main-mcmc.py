import random
import igraph as ig
from matplotlib import pyplot as plt
import numpy as np

from probabilities import get_scores, score
from sampling import sample

def main():
    n = 15000

    non_markov_scores = []
    markov_scores = []
    G = ig.Graph(directed=True)
    G.add_vertices(len(get_scores()))
    
    for i in range(1):
        random.seed(i * 132)

        samples, G_markov = sample(G, n, True)
        plt.plot(np.arange(len(samples)), samples , label=f"Random-{i+1}-markov", linestyle='dashed')
        markov_scores.append(score(G_markov))

        samples, G_no_markov = sample(G, n)
        plt.plot(np.arange(len(samples)), samples , label=f"Random")
        non_markov_scores.append(score(G_no_markov))

    plt.legend()
    plt.show()

main()