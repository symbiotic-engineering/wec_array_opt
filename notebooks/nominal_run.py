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

# Nate's guess for min Spacing
r = 2
L = 0.2
wecx = np.array([0,2**(1/2)*10,10*np.cos(np.pi/4),10*np.cos(np.pi/4)])
wecy = np.array([0,0,10*np.sin(np.pi/4),-10*np.sin(np.pi/4)])

i = 0.07                # interest rate
n_avail = 0.95          # availability coefficient (from global avg estimates) **conservative**
life = 25                  # lifetime of WEC
array_scaling_factor = 0.65     # account for fact that OPEX does not scale linearly (very simplified)
p = [wave_freq, wave_amp, wave_dir, i,n_avail,life,array_scaling_factor,1]
x = model.pack_x(wecx,wecy,r,L,damp)
x = np.array([ 2.0001, 0.10001, 5.5563025, 14.3213562, 0., 5.5563025, 7.07106781, 7.37106781, 5.5563025,  7.07106781, -7.37106781, 5.5563025 ])
print(x)
wec_radius, wec_length, wecx, wecy, damp, N = model.unpack_x(x)
print(f"WEC Radius: {wec_radius}")
print(f"WEC Length: {wec_length}")
print(f"X Locations: {wecx}")
print(f"Y Locations: {wecy}")

print("==================================================================================")

LCOE,AEP,rated_P = model.run(x,p)
print("==================================================================================")
print(f'The LCOE is {LCOE} $/kWh')
print(f'The AEP is {AEP} kWh')
print(f'The Rated Power is {rated_P} kW')
mind = dis.min_d(x,p)
print(f'The min spacing is {mind} m')
maxd = dis.max_d(x,p)
print(f'The max spacing is {maxd} m') 