# calculating the q-factor for pareto optimal designs

import numpy as np
import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
grandparent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append("/".join((grandparent_folder,'sea-lab-utils')))
script_dir = os.path.dirname(__file__)

csv_file_path =  '../data/paretos/reactive_designs.csv'
import modules.model_nWECs as model
import modules.distances as dis
import pandas as pd
import matplotlib.pyplot as plt
import modules.hydro_terms as hydro
import modules.wec_array_initialization as cyl
from parameters.read_params import read_params

p = read_params()
x = pd.read_csv(csv_file_path, delimiter=',',header=None)
print(x.head())
# setting an index such that we get a few points along the Pareto front
end = len(x.iloc[:,0])
#index_range = np.arange(0, end, int(0.1 * end), dtype=int)
index_range = np.arange(0, end, 1, dtype=int)
# for loop to calculate q-factor for Pareto optimal points
q = []

for index in index_range:
    row = x.iloc[index,:]           # choosing a row from the optimal design matrix
    wec_radius, wec_length, wecx, wecy, damp, N = model.unpack_x(row)   # unpacking the variables
    print(f"WEC Radius: {wec_radius} and wec_length is {wec_length}")

    LCOE,AEP,rated_P = model.run(row,p)     # running power calculations
    print(f'The Rated Power is {rated_P} kW')


    x_single = model.pack_x(np.array([0]),np.array([0]),wec_radius,wec_length,np.array([3.6e5]))
    LCOE,AEP,P_isolated = model.run(x_single,p,q_single=True)

    print(f'The Single WEC Rated Power is {P_isolated} kW')

    # power produced by isolated WECs with radii corresponding to the
    # radii on the Pareto front
    # i.e., P_isolated and P_array are functions of radius
    q_factor = rated_P/(P_isolated*N)
    q.append(q_factor)
    print("==================================================================================")

np.savetxt('../data/qfactor.out', np.asarray(q),delimiter=',')