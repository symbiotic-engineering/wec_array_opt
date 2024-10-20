## run the model for the recommended design and get the matrix for different Hs and Tp
import numpy as np
import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append("/".join((parent_folder,'src')))
sys.path.insert(0,parent_folder)
import modules.model_nWECs as model
import modules.distances as dis
import matplotlib.pyplot as plt
import seaborn as sns
from parameters.read_params import read_params
#nominal run fo grid of Hs and Tp /omega.. store the power rating

# define wave conditions

Hs_values = np.linspace(0.5, 5.0, num=10)
T_values = np.linspace(5, 15, num=10)
power_matrix = np.zeros((len(Hs_values), len(T_values)))


# recommended design
x = [8.0,0.100000390005137,5.5762347794275575,5.591921577507208,5.537755861522799,5.545080885661658]
p = read_params(pfile = 'src/parameters/parameters.csv')
omega = p[0]

for i, Hs in enumerate(Hs_values):
    for j, T in enumerate(T_values):
        omega = 2 * np.pi / T
        p[0] = omega
        p[2] = Hs /2 #Hs = 2A (significant double amplitude)
        # nominal run for 
        LCOE,AEP,rated_P = model.run(x,p,time_data=True,reactive=True)
        power_matrix[i, j] = rated_P




plt.figure(figsize=(8, 6))
sns.heatmap(power_matrix, xticklabels=T_values, yticklabels=Hs_values, cmap='viridis')
plt.title('2D Power Matrix for WEC')
plt.xlabel('Spectral Wave Period (s)')
plt.ylabel('Significant Wave Height (m)')
plt.savefig("src/post_pro/plots/power_matrix.pdf")
