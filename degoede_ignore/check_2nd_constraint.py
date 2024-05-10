import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append("/".join((parent_folder,'src')))
import modules.model_nWECs as model
import modules.distances as dis
import numpy as np
from parameters.read_params import read_params
from optimization_interfaces.optimization_problems import check_motion, constraint
# Set-up to match Balitsky Thesis
p = read_params(pfile = 'src/parameters/parameters.csv')

x = np.array([4.0,0.10000179482154603,4.378113145205915,24.447710928456562,-15.313485461239296,4.4840146473585305,27.06533718896739,21.629165486489246,4.495203303908347,37.065142390441736,0.7121947218842212,4.387236950805816])

wec_radius, wec_length, wecx, wecy, damp, N = model.unpack_x(x)
print(f"WEC Radius: {wec_radius}")
print(f"WEC Length: {wec_length}")
print(f"X Locations: {wecx}")
print(f"Y Locations: {wecy}")

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
print("==================================================================================")
print(f'Motion check {check_motion(x,p,Xi)}')