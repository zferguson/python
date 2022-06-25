''' 
Title:      Monte Carlo Simulation
Author:     Zach Ferguson
Last Edit:  2022-06-24
'''

# import modules
import random       as rd 
import numpy        as np
import scipy.stats  as sc
import matplotlib.pyplot as plt

# simulation parameters
numTrials = 1000
expReturn = 0.065
expSD = .105

# storing results
resultList = []
totalReturn = 0

# simulation loop
for i in range(1, numTrials + 1):
    randomProb = rd.uniform(0, 1)
    randomReturn = sc.norm.ppf(randomProb, expReturn, expSD)
    totalReturn += randomReturn
    resultList.append(totalReturn / i)

# arrange results
x = np.arange(1, numTrials + 1)
y = resultList
overallAvg = resultList[-1]

# plot results
plt.style.use('ggplot')
plt.plot(x, y, color = '#2E5984')
plt.suptitle('Portfolio Return Simulation', fontsize = 18)
plt.title('n = {0}, Avg CAGR = {1}%'.format(numTrials, round((overallAvg * 100),2)), fontsize = 10, color = '#808080')
plt.axhline(y = overallAvg, color = 'r', linestyle = 'dotted')
plt.show()