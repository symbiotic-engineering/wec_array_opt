import modules.model_nWECs as model
import modules.distances as dis
import numpy as np
import matplotlib.pyplot as plt

p = np.array([1.047,1,0,1,0])


damps = np.linspace(2,4,20)
P = np.zeros(len(damps))
for ii in range(len(damps)):
    x = np.array([2,1,damps[ii]])
    LCOE,AEP,P[ii] = model.run(x,p)
    print(P[ii])

plt.plot(damps,P)
plt.show()

# ~1000 kW for r = 10, ~5.5 damps, 1 L
#  ~900 kW for r =  2, ~3.1 damps, 0.2 L