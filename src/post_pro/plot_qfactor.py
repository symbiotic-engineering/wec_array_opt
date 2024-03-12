import numpy as np

import pandas as pd
import matplotlib.pyplot as plt

q = np.loadtxt('../data/qfactor.out')
print(len(q))
df = pd.read_csv("../data/paretos/FINALdomObjective.csv",header = None)   
lcoe = df.iloc[:,0]
dist = df.iloc[:,1]

#contour plot for q-factor

lcoe_grid, dist_grid = np.meshgrid(lcoe, dist)
plt.scatter(lcoe, q)
#plt.scatter(dist, q)

plt.xlabel('lcoe')
plt.ylabel('q')
plt.title('Variation of q-factor across pareto optimal design objectives')
plt.savefig('post_pro/plots/q_factor_lcoe.pdf')
plt.close()


plt.scatter(dist, q)
plt.xlabel('dist')
plt.ylabel('q')
plt.title('Variation of q-factor across pareto optimal design objectives')
plt.savefig('post_pro/plots/q_factor_dist.pdf')