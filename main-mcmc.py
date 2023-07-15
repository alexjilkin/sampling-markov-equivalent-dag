import random
import igraph as ig
from matplotlib import pyplot as plt
import numpy as np

from probabilities import get_scores, score
from sampling import sample

def main():
    n = 10000

    non_markov_scores = []
    markov_scores = []
    G = ig.Graph(directed=True)
    G.add_vertices(len(get_scores()))
    
    for i in range(2):
        random.seed(i * 132)

        samples, G_markov = sample(G, n, True)
        plt.plot(np.arange(len(samples)), samples , label=f"Emtpy-{i+1}-markov", linestyle='dashed')
        markov_scores.append(score(G_markov))

        samples, G_no_markov = sample(G, n)
        plt.plot(np.arange(len(samples)), samples , label=f"Empty-{i}")
        non_markov_scores.append(score(G_no_markov))

    # print(f"markov:{np.array(markov_scores).mean()}")
    # print(f"non-markov:{np.array(non_markov_scores).mean()}")
    plt.legend()
    plt.show()

main()