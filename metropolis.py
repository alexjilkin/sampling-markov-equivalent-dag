import numpy as np
import matplotlib.pyplot as plt
import math

x_t = 1
def f(x):
    return np.exp(-x**4)

samples = [x_t]

for i in range(10**6):
    x_proposal = np.random.normal(x_t, 1)
    alpha = f(x_proposal) / f(x_t)

    u = np.random.uniform(0, 1)
    if (u <= alpha):
        x_t = x_proposal    
    samples.append(x_t)

plt.hist(samples, bins=200, density=True)

x = np.linspace(-4, 4, 1000)
plt.plot(x, f(x))
plt.show()
