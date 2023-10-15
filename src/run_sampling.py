import igraph as ig
from matplotlib import pyplot as plt
import numpy as np
import partition
import os
import sys

from probabilities import get_scores, init_scores, score, P
from sampling import sample
import partition
from utils import plot

# score_name = sys.argv[1]
# i = int(sys.argv[2])
# n = int(sys.argv[3])

score_name = 'asia'
i = 1
n = 1000


def test_convergence():
    init_scores(score_name)

    G = ig.Graph(directed=True)
    v_count = len(get_scores())
    G.add_vertices(v_count)

    # if not os.path.exists(f'res/{score_name}/'):
    #     os.makedirs(f'res/{score_name}/')

    for i in range(1):
        step_size = 5

        steps, equivalence_classes = sample(G, n * step_size * 2, False, False)
        print(
            f'Classes visited with equivalence: {len(equivalence_classes)}, n={n}')
        scores = [step[1] for step in steps][::(step_size * 2)]
        plt.plot(np.arange(len(scores)), scores, 'm-',
                 label="Structural basic" if i == 0 else "")
        # with open(f"res/{score_name}/stractural_basic_{i}.csv", "w") as f:
        #     f.write(','.join(map(str, scores)))

        steps, equivalence_classes = sample(G, n * step_size, False, True)
        print(
            f'Classes visited with equivalence: {len(equivalence_classes)}, n={n}')
        scores = [step[1] for step in steps][::step_size]
        plt.plot(np.arange(len(scores)), scores, 'c-',
                 label="Structural w/ REV" if i == 0 else "")
        # with open(f"res/{score_name}/stractural_rev_{i}.csv", "w") as f:
        #     f.write(','.join(map(str, scores)))

        steps = partition.sample_chain(G, n, False, 0, True, 0.066)
        dag_scores = [score(step[2]) for step in steps]

        plt.plot(np.arange(len(dag_scores)), dag_scores,  'g--',
                 label="DAG from partition w/ REV" if i == 0 else "")
        # with open(f"res/{score_name}/partition_w_rev_{i}.csv", "w") as f:
        #     f.write(','.join(map(str, dag_scores)))

        steps = partition.sample_chain(G, n, True, 0.066, True, 0.066)
        dag_scores = [score(step[2]) for step in steps]
        plt.plot(np.arange(len(dag_scores)), dag_scores,  'b--',
                 label="DAG from partition w/ REV and MES" if i == 0 else "")
        # with open(f"res/{score_name}/partition_w_ref_a_mes_{i}.csv", "w") as f:
        #     f.write(','.join(map(str, dag_scores)))

        plt.xlabel('')
        plt.ylabel('Score')

    plt.title(f'{score_name}')
    plt.legend()
    plt.show()


def test_count_equivalences():
    score_name = 'hailfinder-100'
    markov_prob = 0.1

    init_scores(score_name)
    ns = np.arange(10000, 200001, 30000)

    markov_rev_classes_means = []
    classes_means = []
    rev_classes_means = []

    G = ig.Graph(directed=True)
    G.add_vertices(len(get_scores()))

    for n in ns:
        rev_equivalence_classes = []
        markov_rev_equivalence_classes = []
        simple_equivalence_classes = []

        for i in range(7):
            steps, equivalence_classes = sample(G, n, True, markov_prob, False)
            print(
                f'Classes visited with equivalence and REV step: {len(equivalence_classes)}, n={sum(equivalence_classes.values())}')
            markov_rev_equivalence_classes.append(equivalence_classes)

            # steps, equivalence_classes = sample(G, n, False, markov_prob, False)
            # print(f'Classes visited with REV step: {len(equivalence_classes)}, n={sum(equivalence_classes.values())}')
            # rev_equivalence_classes.append(equivalence_classes)

            steps, equivalence_classes = sample(G, n)
            simple_equivalence_classes.append(equivalence_classes)
            print(
                f'Classes visited: {len(equivalence_classes)} n={sum(equivalence_classes.values())}')

        markov_rev_classes_means.append(
            np.array([len(a) for a in markov_rev_equivalence_classes]).mean())
        # rev_classes_means.append(np.array([len(a) for a in rev_equivalence_classes]).mean())
        classes_means.append(
            np.array([len(a) for a in simple_equivalence_classes]).mean())

    plt.plot(ns, classes_means, label="Structure")
    plt.scatter(ns, classes_means)

    plt.plot(ns, markov_rev_classes_means, label="Markov REV")
    plt.scatter(ns, markov_rev_classes_means)

    # plt.plot(ns, rev_classes_means, label="REV")
    # plt.scatter(ns, rev_classes_means)

    plt.title(f"{score_name} markov_p={markov_prob}")
    plt.legend()
    plt.show()


test_convergence()
