from numpy import pi as pi
import numpy as np
import modules.wec_array_initialization as array_init
import modules.hydro_terms as hydro
import modules.econ as econ
from modules.dynamics_controls import wec_dyn 
from modules.dynamics_controls import time_avg_power 
import time
# x = [radius all wecs, lenght all wecs, x location, y location, pto damping, ... other wecs x y and d]
# p = [Wave Frequency, Wave Amplitude, wave direction, number of WECs, time info switch, layout preset(optional)]

def unpack_x(x,nWEC):       # this function unpacks the design vector into the design variables
    #   x       ->  design vector
    #   nWEC    ->  number of WECs
    wec_radius = x[0]
    wec_length = x[1]*x[0]  # this variable is important to note, is is the length ratio, not the actual length
    wecx = np.zeros(nWEC)
    wecy = np.zeros(nWEC)
    damp = np.zeros(nWEC)
    damp[0] = 10**x[2]      # this variable is important to note, it is the damping coefficient exponent, not the actual damping coefficient
    for i in range(nWEC-1):
        wecx[i+1] = x[3+i*3]
        wecy[i+1] = x[4+i*3]
        damp[i+1] = 10**x[5+i*3]
    return wec_radius, wec_length, wecx, wecy, damp

def pack_x(N,wecx,wecy,r,L,d):  # packs variables into design vector
    #   N       ->  number of wecs in array
    #   wecx    ->  x locations
    #   wecy    ->  y location2
    #   r       ->  wec radius
    #   L       ->  wec length
    #   d       ->  pto damping coefficient
    x = np.zeros(3*(N-1) + 3)
    x[0] = r
    x[1] = L/r
    x[2] = np.log10(d[0])
    for ii in range(N-1):
        x[3+3*ii] = wecx[ii+1]
        x[4+3*ii] = wecy[ii+1]
        x[5+3*ii] = np.log10(d[ii+1])
    return x


def run(x,p):   # the big one, runs the whole thing
    #   x   ->  design vector
    #   p   ->  parameter vector
    start_time = time.time()
    nWEC = int(p[3])
    
    # Unpack Design Variables
    wec_radius, wec_length, wecx, wecy, damp = unpack_x(x,nWEC)
    
    # Unpack Parameters
    omega = p[0]
    wave_amp = p[1]
    beta = p[2]
    time_data = p[4] # switch parameter for if you want the time info or not, useful for a nominal run

    # Create Bodies
    if len(p)>5:        
        shape = p[5]    # these are our predefined geometries, parameter 6 is an optional way to use them
        if shape == 1:
            bodies = array_init.grid(wec_radius,wec_length,damp)
        elif shape == 2:
            bodies = array_init.line(wec_radius,wec_length,damp)
        elif shape == 3:
            bodies = array_init.random(wec_radius,wec_length,damp)
        else:
            print('Not a real shape')
    else:
        bodies = array_init.run(wecx,wecy,wec_radius,wec_length,damp)   # run this to use design vector instead of predefined layout
    end_time = time.time()
    if time_data == 1:  # prints time info if switched on
        print(f'Body set up time:  {end_time-start_time}')
        
    # Hydro Module
    A,B,C,F,M = hydro.run(bodies,beta,omega,time_data)
    
    # Dynamics and Controls Module
    start_time = time.time()
    Xi = wec_dyn(bodies,A,B,C,F,M,omega,wave_amp)   # WEC motion
    P,P_indv = time_avg_power(bodies,Xi,omega)      # Power calculation
    
    # Power Transmission and Economics Module
    LCOE,AEP = econ.run(nWEC,M,P_indv,bodies,wec_radius)
    end_time = time.time()
    if time_data == 1:  # prints time info if switched on
        print(f'Power/LCOE time:   {end_time-start_time}')
    return LCOE.item(),AEP.item(),P.item()