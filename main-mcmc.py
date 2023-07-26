import random
import igraph as ig
from matplotlib import pyplot as plt
import numpy as np

from probabilities import get_scores, init_scores, score
from sampling import sample
from utils import plot, seed


def main():
    score_name = 'win95pts-500'
    init_scores(score_name)

    ns = np.arange(1e4, 3e5, 2e4)

    markov_classes_means = []
    classes_means = []
    n = 50000
    G = ig.Graph(directed=True)
    G.add_vertices(len(get_scores()))
    markov_equivalence_classes = []
    simple_equivalence_classes = []

    for i in range(4):
        seed(i+1)
        steps, G_res, equivalence_classes = sample(G, n, True)
        print(f'Classes visited with equivalence step: {len(equivalence_classes)}')
        markov_equivalence_classes.append(equivalence_classes)
        scores = [score(G) for G in steps]
        plt.plot(np.arange(len(scores)), scores , 'b--')
        
        seed(i+2)
        steps, _, equivalence_classes = sample(G, n)
        simple_equivalence_classes.append(equivalence_classes)
        print(f'Classes visited: {len(equivalence_classes)}')
        scores = [score(G) for G in steps]
        plt.plot(np.arange(len(scores)), scores ,  'r-')

        markov_classes_means.append(np.array([len(a) for a in markov_equivalence_classes]).mean())
        classes_means.append(np.array([len(a) for a in simple_equivalence_classes]).mean())

    # plt.plot(ns, classes_means, label="Structure")
    # plt.scatter(ns, classes_means)
    # plt.plot(ns, markov_classes_means, label="Markov")
    # plt.scatter(ns, markov_classes_means)
    plt.title(score_name)
    plt.show()

main()