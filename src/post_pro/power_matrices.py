## run the model for the recommended design and get the matrix for different Hs and Tp to answer: does the farm operates efficiently across a range of sea conditions?

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

def available_wave_power(H_s, T):
    """
    Calculate the available wave power per unit width (kW/m).
    """
    rho = 1023 #(kg/m^3)
    g = 9.8
    P_available = (rho * g**2) / (64 * np.pi) * H_s**2 * T  # in watts per meter
    return P_available / 1000  # convert to kW/m

def capture_width(P_captured, H_s, T):
    """
    Calculate the capture width of the WEC.
    """
    P_available = available_wave_power(H_s, T)
    CW = P_captured / P_available  
    return CW

#calculate capture width ratio (CWR)
def capture_width_ratio(P_captured, H_s, T, L=8):
    """
    Calculate the capture width ratio (CWR) of the WEC.
    L: Max sep for layouts?
    """
    CW = capture_width(P_captured, H_s, T)
    CWR = CW / (4*L) 
    return CWR

# define wave conditions

Hs_values = np.linspace(1, 5.0, num=10)
print(Hs_values)
T_values = np.linspace(5, 15, num=10)
power_matrix = np.zeros((len(Hs_values), len(T_values)))

LCOE_matrix = np.zeros((len(Hs_values), len(T_values)))
capture_width_matrix = np.zeros((len(Hs_values), len(T_values)))

# recommended design
x = [8.0,0.100000390005137,5.5762347794275575,33.27859672211952,58.573433541920565,5.591921577507208,37.872518187721504,18.691411350753484,5.537755861522799,-9.834722626629564,38.78588955445712,5.545080885661658]
p = read_params(pfile = 'src/parameters/parameters.csv')
omega = p[0]

for i, Hs in enumerate(Hs_values):
    for j, T in enumerate(T_values):
        omega = 2 * np.pi / T
        p[0] = omega
        p[2] = Hs /(2*np.sqrt(2)) #Hs = 2sqrt(2) (significant double amplitude)
        # nominal run for 
        LCOE,AEP,rated_P = model.run(x,p,time_data=True,reactive=True)
        power_matrix[i, j] = rated_P
        LCOE_matrix[i,j] = LCOE

        # Calculate available wave power for this Hs and T
        P_available = available_wave_power(Hs, T)
        
        # Calculate capture width
        capture_width_val = rated_P / P_available
        capture_width_matrix[i, j] = capture_width_val #/4 ?





plt.figure(figsize=(8, 6))
sns.heatmap(power_matrix, xticklabels= np.round(T_values), yticklabels=np.round(Hs_values,1), cmap='YlOrRd')
plt.title('2D Power(kW) Matrix for recommended design and layout')
plt.xlabel('Spectral Wave Period (s)')
plt.ylabel('Significant Wave Height (m)')
plt.savefig("src/post_pro/plots/power_matrix.pdf")


plt.figure(figsize=(8, 6))
sns.heatmap(LCOE_matrix, xticklabels= np.round(T_values), yticklabels=np.round(Hs_values), cmap='YlOrRd')
plt.title('LCOE  Matrix for recommended design and layout')
plt.xlabel('Spectral Wave Period (s)')
plt.ylabel('Significant Wave Height (m)')
plt.savefig("src/post_pro/plots/lcoe_matrix.pdf")



plt.figure(figsize=(10, 8))
plt.contourf(T_values, Hs_values, capture_width_matrix, cmap='Reds', levels=20)
plt.colorbar(label='Capture Width (m)')
plt.xlabel('Wave Period (T) [s]')
plt.ylabel('Significant Wave Height (Hs) [m]')
plt.title('Capture Width of WEC Layout')
plt.savefig("src/post_pro/plots/cw_matrix.pdf")