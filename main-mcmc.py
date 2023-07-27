import random
import igraph as ig
from matplotlib import pyplot as plt
import numpy as np

from probabilities import get_scores, init_scores, score
from sampling import sample
from utils import plot, seed


def test_count_equivalences():
    score_name = 'hailfinder-100'
    init_scores(score_name)

    ns = np.arange(1e4, 3e5, 2e4)

    markov_classes_means = []
    classes_means = []
    G = ig.Graph(directed=True)
    G.add_vertices(len(get_scores()))
    markov_equivalence_classes = []
    simple_equivalence_classes = []

    for n in ns:
        for i in range(30):
            steps, equivalence_classes = sample(G, n, True)
            print(f'Classes visited with equivalence step: {len(equivalence_classes)}, n={n}')
            markov_equivalence_classes.append(equivalence_classes)

            steps, equivalence_classes = sample(G, n)
            simple_equivalence_classes.append(equivalence_classes)
            print(f'Classes visited: {len(equivalence_classes)} n={n}')

            markov_classes_means.append(np.array([len(a) for a in markov_equivalence_classes]).mean())
            classes_means.append(np.array([len(a) for a in simple_equivalence_classes]).mean())

    plt.plot(ns, classes_means, label="Structure")
    plt.scatter(ns, classes_means)
    plt.plot(ns, markov_classes_means, label="Markov")
    plt.scatter(ns, markov_classes_means)
    plt.title(score_name)
    plt.show()

def test_convergence():
    score_name = 'win95pts-500'
    init_scores(score_name)

    n = 40000
    x = np.arange(n)
    G = ig.Graph(directed=True)
    G.add_vertices(len(get_scores()))

    for i in range(2):
        steps, equivalence_classes = sample(G, n, True)
        print(f'Classes visited with equivalence step: {len(equivalence_classes)}, n={n}')
        scores = [step[1] for step in steps]
        plt.plot(x, scores , 'b--')

        steps, equivalence_classes = sample(G, n)
        print(f'Classes visited: {len(equivalence_classes)} n={n}')
        scores = [step[1] for step in steps]
        plt.plot(x, scores ,  'r-')

    plt.title(score_name)
    plt.show()

test_convergence()