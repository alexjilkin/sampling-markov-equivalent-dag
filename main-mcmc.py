import random
import igraph as ig
from matplotlib import pyplot as plt
import numpy as np

from probabilities import get_scores, init_scores, score
from sampling import sample
from utils import get_next_color, plot, seed


def test_count_equivalences():
    score_name = 'hepar2-500'
    markov_prob = 0.1
    init_scores(score_name)

    ns = np.arange(10000, 21000, 5000)

    markov_rev_classes_means = []
    classes_means = []
    rev_classes_means = []

    G = ig.Graph(directed=True)
    G.add_vertices(len(get_scores()))

    for n in  ns:
        rev_equivalence_classes = []
        markov_rev_equivalence_classes = []
        simple_equivalence_classes = []

        for i in range(4):
            steps, equivalence_classes = sample(G, n, True, markov_prob, True)
            print(f'Classes visited with equivalence and REV step: {len(equivalence_classes)}, n={n}')
            markov_rev_equivalence_classes.append(equivalence_classes)

            steps, equivalence_classes = sample(G, n, False, markov_prob, True)
            print(f'Classes visited with REV step: {len(equivalence_classes)}, n={n}')
            rev_equivalence_classes.append(equivalence_classes)

            steps, equivalence_classes = sample(G, n)
            simple_equivalence_classes.append(equivalence_classes)
            print(f'Classes visited: {len(equivalence_classes)} n={n}')

        markov_rev_classes_means.append(np.array([len(a) for a in markov_rev_equivalence_classes]).mean())
        rev_classes_means.append(np.array([len(a) for a in rev_equivalence_classes]).mean())
        classes_means.append(np.array([len(a) for a in simple_equivalence_classes]).mean())

    plt.plot(ns, classes_means, label="Structure")
    plt.scatter(ns, classes_means)

    plt.plot(ns, markov_rev_classes_means, label="Markov REV")
    plt.scatter(ns, markov_rev_classes_means)
    
    plt.plot(ns, rev_classes_means, label="REV")
    plt.scatter(ns, rev_classes_means)

    plt.title(f"{score_name} markov_p={markov_prob}")
    plt.legend()
    plt.show()

def test_convergence():
    score_name = 'hepar2-500'
    markov_prob = 0.2
    init_scores(score_name)

    n = 15000
    G = ig.Graph(directed=True)
    G.add_vertices(len(get_scores()))

    for _ in range(2):
        steps, equivalence_classes = sample(G, n, True, markov_prob, True)
        print(f'Classes visited with REV and equivalence step: {len(equivalence_classes)}, n={n}')
        scores = [step[1] for step in steps]
        plt.plot(np.arange(len(scores)), scores, 'g--')

        steps, equivalence_classes = sample(G, n, False, markov_prob, True)
        print(f'Classes visited with REV step: {len(equivalence_classes)}, n={n}')
        scores = [step[1] for step in steps]
        plt.plot(np.arange(len(scores)), scores, 'b--')

        steps, equivalence_classes = sample(G, n)
        print(f'Classes visited: {len(equivalence_classes)} n={n}')
        scores = [step[1] for step in steps]
        plt.plot(np.arange(len(scores)), scores ,  'r-')

    plt.title(score_name)
    plt.show()

test_convergence()