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
    print(f"x is {wecx[0]}, y is {wecy[0]}")
    bodies = cyl.get_cylinder(wec_radius, wec_length, wecx, wecy, damp)
    A,B,C,F,M, RAO = hydro.run(bodies,beta = 0,omega = omega ,time_data = 0)
    print('config RAO',RAO)

   
    body = cyl.get_cylinder(wec_radius,wec_length,wecx[0],wecy[0],-1000*damp[0])
    omega = 1.047
    body.inertia_matrix = body.compute_rigid_body_inertia()
    body.hydrostatic_stiffness = body.compute_hydrostatic_stiffness()
    A,B,C,F,M, RAO = hydro.run([body],beta = 0,omega = omega ,time_data = 0)
    A = [list(v.values()) for k,v in A.items()][0][0][0] #because its nested
    B = [list(v.values()) for k,v in B.items()][0][0][0] #
    C = [v[0] for k,v in C.items()][0][0]#
    M = [v[0] for k,v in M.items()][0][0] #
    
    # find power produced by single WEC at that radius
    damp_single = (B**2+(omega*(M+A)-C/omega)**2)**0.5
    single_wec = np.array([wec_radius,wec_length/wec_radius,np.log10(damp_single)])
    print('single wec',single_wec)

    LCOE_new,AEP_new,P_isolated = model.run(single_wec,p)
    print(f'The Single WEC Rated Power is {P_isolated} kW')

    # power produced by isolated WECs with radii corresponding to the
    # radii on the Pareto front
    # i.e., P_isolated and P_array are functions of radius
    q_factor = rated_P/(P_isolated*N)
    q.append(q_factor)
    print("==================================================================================")

#instead off plotting with index range..let's plot with LCOE and Distance

df = pd.read_csv("../data/paretos/reactive_objectives.csv")   
lcoe = df.iloc[:,0]
dist = df.iloc[:,1]

#contour plot for q-factor
print(q)
np.savetxt('~/wec_array_opt/data/qfactor.out', np.asarray(q),delimiter=',')
lcoe_grid, dist_grid = np.meshgrid(lcoe, dist)
plt.contourf(lcoe_grid, dist_grid, q.reshape(lcoe_grid.shape))
plt.colorbar(label='q')  
plt.xlabel('lcoe')
plt.ylabel('dist')
plt.title('Variation of q-factor across pareto optimal design objectives')
plt.savefig('post_pro/plots/q_factor.pdf')
# np.savetxt('qfactor.out', np.asarray(q),delimiter=',')