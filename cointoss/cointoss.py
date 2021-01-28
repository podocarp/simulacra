import json
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

with open('settings.json') as f:
    settings = json.load(f)
    N = settings['N'] # number of coins
    trials = settings['trials']
    step = settings['step']

# Flip coins
flips = np.random.binomial(N, 0.5, trials)

fig, ax = plt.subplots()

x = np.arange(0, N, 1)
n, bins, patches = ax.hist(flips, x, density=True, edgecolor="black", align="left")

# CLT
mu = N/2
sigma = np.sqrt(N) * 0.5

x = np.arange(0, N, step)
y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
     np.exp(-0.5 * ((x - mu) / sigma)**2))
ax.plot(x, y, '-')
ax.set_xlabel('Number of heads')
ax.set_ylabel('Probability density')
ax.set_title(r"Histogram, {} coins, {} trials. $\mu={}, \sigma={}$"
    .format(N, trials, mu, round(sigma,2)))

plt.show()
