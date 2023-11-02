from probabilities import get_scores, init_scores
from pruning import count_scores, init_pruning, prune_scores
import matplotlib.pyplot as plt
import copy
import numpy as np


score_names = ['insurance-100', 'insurance-400',
               'insurance-600', 'insurance-800']  # 'insurance-1000']

# score_names = ['hailfinder-100',  'hailfinder-500', 'hailfinder-800']

epss = [1e-1, 1e-2, 1e-3, 1e-4]  # 1e-5, 1e-6]
n = len(score_names)


all_values = []
fig, axs = plt.subplots(1, n, figsize=(15, 3))

for i in range(n):
    score_name = score_names[i]
    plt.title(score_name)
    for j in range(len(epss)):
        eps = epss[j]

        init_scores(score_name)
        scores = get_scores()

        pruning_results = []
        bs = np.linspace(1e-10, 1, 10)
        for b in bs:
            pruned_scores = copy.deepcopy(scores)
            init_pruning(pruned_scores, 3, eps, b)

            prune_scores()
            pruning_results.append(pruned_scores)
            all_values.append(count_scores(pruned_scores))

        counts = [count_scores(s) for s in pruning_results]
        axs[i].plot(bs, counts, label=f'eps={eps}')
        axs[i].set_title(f'{score_name}')
        plt.xlabel('b')

all_values = np.array(all_values)
for ax in axs:
    ax.set_ylim(all_values.min(), all_values.max())

plt.legend()
plt.show()
