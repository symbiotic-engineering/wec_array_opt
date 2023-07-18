from numpy import pi as pi
import numpy as np
import modules.wec_array_initialization as array_init
import modules.hydro_terms as hydro
import modules.econ as econ
from modules.dynamics_controls import wec_dyn 
from modules.dynamics_controls import time_avg_power 
# x = [radius all wecs, lenght all wecs, x location, y location, pto damping, ... other wecs x y and d]
# p = [Wave Frequency, Wave Amplitude, density of WEC material, number of WECs]
def unpack_x(x,nWEC):
    wec_radius = x[0]
    wec_length = x[1]
    wecx = np.zeros(nWEC)
    wecy = np.zeros(nWEC)
    damp = np.zeros(nWEC)
    damp[0] = 10**x[2]
    for i in range(nWEC-1):
        wecx[i+1] = x[3+i*3]
        wecy[i+1] = x[4+i*3]
        damp[i+1] = 10**x[5+i*3]
    return wec_radius, wec_length, wecx, wecy, damp
def pack_x(N,wecx,wecy,r,L,d):
    x = np.zeros(3*(N-1) + 3)
    x[0] = r
    x[1] = L
    x[2] = np.log10(d[0])
    for ii in range(N-1):
        x[3+3*ii] = wecx[ii+1]
        x[4+3*ii] = wecy[ii+1]
        x[5+3*ii] = d[ii+1]
    return x

def run(x,p):
    nWEC = int(p[3])
    
    # Unpack Design Variables
    wec_radius, wec_length, wecx, wecy, damp = unpack_x(x,nWEC)
    
    # Unpack Parameters
    omega = p[0]
    wave_amp = p[1]
    beta = p[2]
    
    # Create Bodies
    bodies = array_init.run(wecx,wecy,wec_radius,wec_length,damp)

    # Hydro Module
    A,B,C,F,M = hydro.run(bodies,beta,omega)
    
    # Dynamics and Controls Modules
    Xi = wec_dyn(bodies,A,B,C,F,M,omega,wave_amp)
    P,P_indv = time_avg_power(bodies,Xi,omega)
    
    # Power Transmission and Economics Module
    LCOE,AEP = econ.run(nWEC,M,P_indv,bodies)
    return LCOE