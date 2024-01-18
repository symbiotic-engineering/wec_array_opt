import modules.model_nWECs as model
import numpy as np
# This module is used to find the maximum and minimum spacing in the WEC array

def min_d(x,p):                     # Minimum spacing
    #   x   ->  design vector
    #   p   ->  parameters
    nwec = int(p[3])                # Number of WECs
    if nwec == 1:
        return np.inf               # If there are no other wecs, it is not very close to anyone
    wec_radius, wec_length, wecx, wecy, damp = model.unpack_x(x,nwec)
    d = []
    for i in range(nwec):
        for j in range(i+1,nwec):
            d.append(((wecx[i]-wecx[j])**2 + (wecy[i]-wecy[j])**2)**(1/2))      # Compute the distance between wec i and wec j
    mind = min(d)               # What is the shortest distance?
    return (mind)

def max_d(x,p):                     # Maximum spaceing
    #   x   ->  design vector
    #   p   ->  parameters
    nwec = int(p[3])                # Number of WECs
    if nwec == 1:
        return 0                    # if there are no other wecs, the array is small
    wec_radius, wec_length, wecx, wecy, damp = model.unpack_x(x,nwec)
    d = []
    for i in range(nwec):
        for j in range(i+1,nwec):
            d.append(((wecx[i]-wecx[j])**2 + (wecy[i]-wecy[j])**2)**(1/2))      # Compute the distance between wec i and wec j
    maxd = max(d)               # What is the longest distance?
    return (maxd)