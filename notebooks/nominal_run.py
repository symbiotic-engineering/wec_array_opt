import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append("/".join((parent_folder,'src')))
import modules.model_nWECs as model
import modules.distances as dis
import numpy as np

# Set-up to match Balitsky Thesis
wave_freq = 2*np.pi/6  
wave_amp = 2/2
wave_dir = 0     
N = 18
r = 5
L = 2*2
basex = np.array([0,0,0,0,0,-30,-30,-30,-30]) # used to make wecx easier
wecx = np.concatenate((basex,basex + 500))
wecy = np.array([0,30,60,-30,-60,15,45,-15,-45,0,30,60,-30,-60,15,45,-15,-45])
damp = 3.6e5*np.ones(wecx.shape)

p = [wave_freq, wave_amp, wave_dir, N, 0]
x = model.pack_x(N,wecx,wecy,r,L,damp)
wec_radius, wec_length, wecx, wecy, damp = model.unpack_x(x,N)
print(f"WEC Radius: {wec_radius}")
print(f"WEC Length: {wec_length}")
print(f"X Locations: {wecx}")
print(f"Y Locations: {wecy}")

print("==================================================================================")

LCOE,AEP,P = model.run(x,p)
print("==================================================================================")
print(f'The LCOE is {LCOE} $/kWh')
print(f'The AEP is {AEP} kWh')
print(f'The Power is {P} kW')
mind = dis.min_d(x,p)
print(f'The min spacing is {mind} m')
maxd = dis.max_d(x,p)
print(f'The max spacing is {maxd} m') 