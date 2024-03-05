# calculating the q-factor for pareto optimal designs
# CURRENTLY USING DUMMY NUMBERS
import numpy as np
import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
grandparent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append("/".join((grandparent_folder,'sea-lab-utils')))
script_dir = os.path.dirname(__file__)

###### CHANGE 'domDesign' TO THE CORRECT CSV FILE !!!!!!!!!!!!!!!!!!!!!!!!
csv_file_path = os.path.join(script_dir, '..', '..', 'data/paretos', 'domDesign.csv')
import modules.model_nWECs as model
import modules.distances as dis
import pandas as pd
import matplotlib.pyplot as plt

# Set-up to match Balitsky Thesis
wave_freq = 2*np.pi/6  
wave_amp = 2/2
wave_dir = 0     
i = 0.07                # interest rate
n_avail = 0.95          # availability coefficient (from global avg estimates) **conservative**
life = 25                  # lifetime of WEC
array_scaling_factor = 0.65     # account for fact that OPEX does not scale linearly (very simplified)

p = [wave_freq, wave_amp, wave_dir, i,n_avail,life,array_scaling_factor]
x = pd.read_csv(csv_file_path, delimiter=',',header=None)

# setting an index such that we get a few points along the Pareto front
end = len(x.iloc[:,0])
#index_range = np.arange(0, end, int(0.1 * end), dtype=int)
index_range = np.arange(0, end, 1, dtype=int)
# for loop to calculate q-factor for Pareto optimal points
q = []

for index in index_range:
    row = x.iloc[index,:]           # choosing a row from the optimal design matrix
    wec_radius, wec_length, wecx, wecy, damp, N = model.unpack_x(row)   # unpacking the variables
    print(f"WEC Radius: {wec_radius}")

    LCOE,AEP,rated_P = model.run(row,p)     # running power calculations
    print(f'The Rated Power is {rated_P} kW')

    # find power produced by single WEC at that radius
    single_wec = np.array([wec_radius,wec_length/wec_radius,np.log10(damp[0])])
    print('single wec',single_wec)
    LCOE_new,AEP_new,P_isolated = model.run(single_wec,p)
    print(f'The Single WEC Rated Power is {P_isolated} kW')

    # power produced by isolated WECs with radii corresponding to the
    # radii on the Pareto front
    # i.e., P_isolated and P_array are functions of radius
    q_factor = rated_P/(P_isolated*N)
    print('q_factor',q_factor)
    q.append(q_factor)
    print("==================================================================================")

plt.plot(index_range,q)
plt.show()