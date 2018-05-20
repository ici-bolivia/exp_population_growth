import numpy as np
import matplotlib.pylab as plt

''' Exponential population growth model

n : population
n(t+1) = An(t)

A: Projection Matrix
     0  0 F3
A = G1 P2  0
     0 G2 P3
'''

# 8 year data for materity and fledgling survival (Table 4, Maestri et al, 2017)
m = [0.0698, 0.0204, 0.1455, 0.1733, 0.0714, 0.2286, 0.1538, 0.0508]
l = [0.6667, 1.0, 0.75, 0.7692, 0.0, 0.5625, 0.3, 0.6667]
maternity_mean = np.mean(m)
maternity_std = np.std(m)
survival_mean = np.mean(l)
survival_std = np.std(l)

# Assuming a total population of 125 shared across fledglings, juveniles, and adults
n = np.array([[8], [18], [99]])
# Deterministic projection matrix values as used by Maestri et al.
P3 = 0.9565; F3 = 0.0692; G2 = 0.2337; P2 = 0.7398; G1 = 0.7000
A = np.matrix([[0, 0, F3], [G1, P2, 0], [0, G2, P3]])

# number of years to project
years = 100
x = np.arange(years)
y_det = []
y_det.append(n)
for i in range(1, years+1):
    n = np.dot(A,n)
    y_det.append(n)

plt.figure()
# plot deterministic population growth
y_det = np.asarray(y_det)[:,:,0]
plt.plot(y_det[:,2], color='r')

# compute independent monte-carlo simulations for stochastic model
monte_carlo_sims = 100
for r in range(monte_carlo_sims):
    n = np.array([[8], [18], [99]])
    y_sto = []
    for i in range(years+1):
        # apply clip to ensure random variables are within realistic bounds
        A[0,2] =  np.clip(np.random.normal(maternity_mean, maternity_std), 0.01, 1) * \
                  np.clip(np.random.normal(survival_mean, survival_std), 0.01, 1)
        n = np.dot(A,n)
        y_sto.append(n)
    
    plt.plot(np.asarray(y_sto)[:,2,0].T, alpha=0.2)

plt.grid()
plt.ylim(ymin=0)
plt.show()
