import random
import igraph as ig
from matplotlib import pyplot as plt
import numpy as np

from probabilities import get_scores, score
from sampling import sample

def seed(s):
    np.random.seed(s * 1 + 1)
    random.seed(s * 2 + 3)

def main():
    n = 100000
    G = ig.Graph(directed=True)
    G.add_vertices(len(get_scores()))

    for i in range(1):
        seed(i + 1)
        steps, _ = sample(G, n, True)
        scores = [score(G) for G in steps]
        plt.plot(np.arange(len(scores)), scores , label=f"Emtpy-{i+1}-Markov", linestyle='dashed')
        
        seed(i + 2)
        steps, _ = sample(G, n)
        scores = [score(G) for G in steps]
        plt.plot(np.arange(len(scores)), scores , label=f"Empty-{i+1}")

    plt.legend()
    plt.show()

main()