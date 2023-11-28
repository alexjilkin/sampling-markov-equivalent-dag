from probabilities import get_scores, init_scores
from pruning import count_scores, init_pruning, prune_scores
import matplotlib.pyplot as plt
import copy
import numpy as np


score_names = ['mushrooms-100',
               'mushrooms-1000']  # , 'mushrooms']
#    'insurance-600', 'insurance-800', 'insurance-1000']

# score_names = ['hailfinder-100', 'hailfinder-200',
#                'hailfinder-500', 'hailfinder-800', 'hailfinder-1000']
# score_names = ['hepar2-200', 'hepar2-500']
# score_names = ['agaricus-lepiota-200',
#                'agaricus-lepiota-500', 'agaricus-lepiota']

# epss = [0.1]
epss = [0.1, 0.5, 1, 2]
n = len(score_names)


all_values = []
fig, axs = plt.subplots(1, n)

for i in range(0, n):
    score_name = score_names[i]
    plt.title(score_name)
    init_scores(score_name)

    for j in range(len(epss)):
        eps = epss[j]

        scores = get_scores()

        pruning_results = []
        bs = np.linspace(0, 1, 10)
        # bs = np.linspace(1, 1, 1)
        for b in bs:
            pruned_scores = copy.deepcopy(scores)
            init_pruning(pruned_scores, 4, eps, b)

            prune_scores()
            pruned_scores_count = count_scores(pruned_scores)
            pruning_results.append(pruned_scores_count)
            all_values.append(pruned_scores_count)

        axs[i].plot(bs, pruning_results, label=f'eps={eps}')
        axs[i].set_title(f'{score_name}')
        plt.xlabel('b')

all_values = np.array(all_values)
for ax in axs:
    ax.set_ylim(all_values.min() * 0.98, all_values.max()*1.02)

plt.legend()
plt.show()
