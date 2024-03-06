import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append("/".join((parent_folder,'src')))
import modules.model_nWECs as model
import modules.distances as dis
import numpy as np
wave_freq = 1.047 
wave_amp = 1
wave_dir = 0     
N = 4

p = [wave_freq, wave_amp, wave_dir, N, 0]
x =np.array([5.325203438444657,0.14353262885406554,1.2530055440922019,-589.4684883771776,351.18125657271526,4.426026020185715,-674.6244906553854,-108.97963359757523,3.899335279090678,-115.35450094492194,-62.74147042703967,3.3221155388429606])

wec_radius, wec_length, wecx, wecy, damp,N = model.unpack_x(x)
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