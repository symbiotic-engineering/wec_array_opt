from numpy import pi as pi
import numpy as np
import modules.wec_array_initialization as array_init
import modules.hydro_terms as hydro
import modules.econ as econ
from modules.dynamics_controls import wec_dyn 
from modules.dynamics_controls import time_avg_power 
import time
# x = [radius all wecs, lenght all wecs, x location, y location, pto damping, ... other wecs x y and d]
# p = [Wave Frequency, Wave Amplitude, wave direction, interest rate, wave availability, life span, array scaling factor]

def unpack_x(x):       # this function unpacks the design vector into the design variables
    #   x       ->  design vector
    #   nWEC    ->  number of WECs
    nWEC = int(len(x)/3)
    wec_radius = x[0]/2
    wec_length = x[1]*wec_radius  # this variable is important to note, it is the length ratio, not the actual length
    wecx = np.zeros(nWEC)
    wecy = np.zeros(nWEC)
    damp = np.zeros(nWEC)
    damp[0] = 10**x[2]      # this variable is important to note, it is the damping coefficient exponent, not the actual damping coefficient
    for i in range(nWEC-1):
        wecx[i+1] = x[3+i*3]
        wecy[i+1] = x[4+i*3]
        damp[i+1] = 10**x[5+i*3]
    return wec_radius, wec_length, wecx, wecy, damp, nWEC

def pack_x(wecx,wecy,r,L,d):  # packs variables into design vector
    #   wecx    ->  x locations
    #   wecy    ->  y location2
    #   r       ->  wec radius
    #   L       ->  wec length
    #   d       ->  pto damping coefficient
    N = int(len(wecx))
    x = np.zeros(3*(N-1) + 3)
    x[0] = r*2
    x[1] = L/r
    x[2] = np.log10(d[0])
    for ii in range(N-1):
        x[3+3*ii] = wecx[ii+1]
        x[4+3*ii] = wecy[ii+1]
        x[5+3*ii] = np.log10(d[ii+1])
    return x

def run(x,p,reactive=True,check_condition=True,sensitivity_run=False,time_data=False,shape=None,qfactor_single=False):   # the big one, runs the whole thing
    #   x               ->  design vector
    #   p               ->  parameter vector
    #   reactive        ->  boolean to set if reactive (true) or resistive (false) control is used
    #   check_condition ->  boolean to set if the condition number is checked on the A and B matricies
    #   sensitivity_run ->  boolean to set if the sensitivity run is happening (chages what happend on hydro error)
    #   time_data       ->  boolean to set if time data should be printed or not
    #   shape           ->  used to optimize on predefined shapes 1=grid, 2=line, 3="random"
    #   qfactor_single  ->  boolean to set if you want to calculate the damping instead of use the design variable (True)
    start_time = time.time()
    
    # Unpack Design Variables
    wec_radius, wec_length, wecx, wecy, damp, nWEC = unpack_x(x)
    
    # Unpack Parameters
    omega = p[0]
    wave_amp = p[1]
    beta = p[2]
    F_max = p[7]

    # Create Bodies     
    if shape == None: bodies = array_init.run(wecx,wecy,wec_radius,wec_length,damp) # use design vector
    elif shape == 1: bodies = array_init.grid(wec_radius,wec_length,damp)           # use grid layout
    elif shape == 2: bodies = array_init.line(wec_radius,wec_length,damp)           # use line layout
    elif shape == 3: bodies = array_init.random(wec_radius,wec_length,damp)         # use "random" layout
    else: print('Not a real shape')

    end_time = time.time()
    if time_data:  # prints time info if switched on
        print(f'Body set up time:  {end_time-start_time}')
        
    # Hydro Module
    try:
        A,B,C,F,M = hydro.run(bodies,beta,omega,time_data)
    except RuntimeError:
        with open("../data/skipped.txt", "a") as file:            
            r_str = str(wec_radius)
            L_str = str(wec_length)
            file.write(r_str + ", " + L_str + "\n")
        if sensitivity_run:
            return None,0,{body:0 for body in bodies}
        return 1e3,0,{body:0 for body in bodies}
    # Dynamics and Controls Module
    start_time = time.time()
    Xi = wec_dyn(bodies,A,B,C,F,M,omega,wave_amp,reactive,F_max,check_condition,qfactor_single=False)   # WEC motion
    P,P_indv = time_avg_power(bodies,Xi,omega)      # Power calculation
    
    # Power Transmission and Economics Module
    econ_pvec = np.array([p[3],p[4],p[5],p[6]])
    LCOE,AEP,rated_P = econ.run(M,P_indv,bodies,econ_pvec)
    end_time = time.time()
    if time_data:  # prints time info if switched on
        print(f'Power/LCOE time:   {end_time-start_time}')
    return LCOE.item(),AEP.item(),P.item()
