import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append("/".join((parent_folder,'src')))
import modules.model_nWECs as model
import modules.distances as dis
import numpy as np
from parameters.read_params import read_params

# Set-up to match Balitsky Thesis
p = read_params(pfile = 'src/parameters/parameters.csv')
p[0] = (2*np.pi)/6  # slightly different freqeuncy
N = 18
r = 5
L = 2*2
basex = np.array([0,0,0,0,0,-30,-30,-30,-30]) # used to make wecx easier
wecx = np.concatenate((basex,basex + 500))
wecy = np.array([0,30,60,-30,-60,15,45,-15,-45,0,30,60,-30,-60,15,45,-15,-45])
damp = 3.6e5*np.ones(wecx.shape)

# Set-up Diamond array
'''r = 7
L = 0.7
space = r*3.6
wecx = np.array([0,1,2,1])*space
wecy = np.array([0,1,0,-1])*space
damp = 10**5.7*np.ones(wecx.shape)'''

x = model.pack_x(wecx,wecy,r,L,damp)

wec_radius, wec_length, wecx, wecy, damp, N = model.unpack_x(x)
print(f"WEC Radius: {wec_radius}")
print(f"WEC Length: {wec_length}")
print(f"X Locations: {wecx}")
print(f"Y Locations: {wecy}")

print("==================================================================================")

LCOE,AEP,rated_P = model.run(x,p,time_data=True,reactive=True)
print("==================================================================================")
print(f'The LCOE is {LCOE} $/kWh')
print(f'The AEP is {AEP} kWh')
print(f'The Rated Power is {rated_P} kW')
mind = dis.min_d(x,p)
print(f'The min spacing is {mind} m')
maxd = dis.max_d(x,p)
print(f'The max spacing is {maxd} m') 