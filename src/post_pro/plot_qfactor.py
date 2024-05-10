import numpy as np

import pandas as pd
import matplotlib.pyplot as plt

q = np.loadtxt('../data/qfactor2.out')
print(len(q))
df = pd.read_csv("../data/paretos/obj.csv",header = None)   
lcoe = df.iloc[:120,0]
dist = df.iloc[:120,1]

print(len(lcoe))
plt.scatter(lcoe, q)

plt.xlabel('lcoe')
plt.ylabel('q')
plt.title('Variation of q-factor across pareto optimal design objectives')
plt.savefig('post_pro/plots/q_factor_lcoe2.pdf')
plt.close()


plt.scatter(dist, q)
plt.xlabel('dist')
plt.ylabel('q')
plt.title('Variation of q-factor across pareto optimal design objectives')
plt.savefig('post_pro/plots/q_factor_dist2.pdf')