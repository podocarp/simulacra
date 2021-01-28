import json
import matplotlib
import numpy as np
import scipy.special
import matplotlib.pyplot as plt

with open('settings.json') as f:
    settings = json.load(f)
    N = settings['N'] # number of coins
    trials = settings['trials']
    p = settings['p']
    plotExact = settings['plotExact']
    binomOrPoisson = settings['binomOrPoisson']
    if plotExact:
        step = settings['step']

# Flip coins
mu = N * p
sigma = np.sqrt(N) * 0.5
x = np.arange(0, N, 1)
if binomOrPoisson:
    flips = np.random.binomial(N, p, trials)
else:
    flips = np.random.poisson(mu, trials)

fig, ax = plt.subplots()

n, bins, patches = ax.hist(flips, x, density=True, edgecolor="black", align="left")

if plotExact:
    x = np.arange(0, N, step)
    if binomOrPoisson:
        # CLT, plot the approximate gaussian
        y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
            np.exp(-0.5 * ((x - mu) / sigma)**2))
    else:
        y = mu**x * np.exp(-mu) / scipy.special.factorial(x)
    ax.plot(x, y, '-')


ax.set_xlabel('Number of heads')
ax.set_ylabel('Probability density')
ax.set_title(r"Histogram, {} coins, {} trials. $\mu={}, \sigma={}$"
    .format(N, trials, mu, round(sigma,2)))
plt.show()
