import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append("/".join((parent_folder,'src')))
import modules.model_nWECs as model
import modules.distances as dis
import numpy as np
from parameters.read_params import read_params

p = read_params(pfile = 'src/parameters/parameters.csv')
N = 1
r = 5
L = 2*2
d = np.array([3.6e5])
x = model.pack_x(np.array([0]),np.array([0]),r,L,d)
model.run(x,p,time_data=True)
print("==================================================================================")

LCOE,AEP,rated_P,Xi = model.run(x,p,time_data=True,reactive=True)
print("==================================================================================")
print(f'The LCOE is {LCOE} $/kWh')
print(f'The AEP is {AEP} kWh')
print(f'The Rated Power is {rated_P} kW')
mind = dis.min_d(x,p)
print(f'The min spacing is {mind} m')
maxd = dis.max_d(x,p)
print(f'The max spacing is {maxd} m') 

