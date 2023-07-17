import numpy as np
import Model.wec_array_initialization as array_init
import Model.hydrodynamics as hydro
import Model.time_avg_power as power

# x = [r_1, L_1, x_1, y_1, d_1, r_2, L_2, x_2, y_2, d_2, ..., r_n, L_n, x_n, y_n, d_n]
# p = [omega, A, beta]
def unpack_x(x):
    N = int(len(x)/5)
    wecx = np.zeros(N)
    wecy = np.zeros(N)
    r = np.zeros(N)
    L = np.zeros(N)
    d = np.zeros(N)
    for ii in range(N):
        r[ii] = x[5*ii]
        L[ii] = x[1+5*ii]
        wecx[ii] = x[2+5*ii]
        wecy[ii] = x[3+5*ii]
        d[ii] = x[4+5*ii]
    return N,wecx,wecy,r,L,d
def pack_x(N,wecx,wecy,r,L,d):
    x = np.zeros(5*N)
    for ii in range(N):
        x[5*ii] = r[ii]
        x[1+5*ii] = L[ii]
        x[2+5*ii] = wecx[ii]
        x[3+5*ii] = wecy[ii]
        x[4+5*ii] = d[ii]
    return x

def run(x,p):
    # Unpack Design Vector
    N,wecx,wecy,r,L,d = unpack_x(x)
    # Unpack Parameters
    omega = p[0]
    A = p[1]
    beta = p[2]
    # Initialize WEC Array
    bodies,neighbors = array_init.run(wecx,wecy,r,L,d)
    # Run BEM-PWA combo hydrodynamics module
    Xi,M = hydro.run(bodies,neighbors,omega,A,beta)
    # Calculate Time Average Power
    P,P_indv = power.run(bodies,Xi,omega)
    # Economics
    
    return P