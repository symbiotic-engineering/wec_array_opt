import modules.model_nWECs as model
import numpy as np
# This module is used to find the maximum and minimum spacing in the WEC array

def distances(x):
    wec_radius, wec_length, wecx, wecy, damp, nwec = model.unpack_x(x)
    d = []
    for i in range(nwec):
        weci = np.array([wecx[i], wecy[i]])
        for j in range(i+1,nwec):
            wecj = np.array([wecx[j], wecy[j]])
            d.append(np.linalg.norm(weci,wecj))      # Compute the distance between wec i and wec j
    return d,nwec

def min_d(x,p):                 # Minimum spacing
    #   x   ->  design vector
    #   p   ->  parameters
    d,nwec = distances(x,p)     # compute ditances
    if nwec == 1:
        return np.inf           # If there are no other wecs, it is not very close to anyone
    mind = min(d)               # What is the shortest distance?
    return (mind)

def max_d(x,p):                 # Maximum spaceing
    #   x   ->  design vector
    #   p   ->  parameters
    d,nwec = distances(x,p)     # compute distances
    if nwec == 1:
        return 0                # if there are no other wecs, the array is small
    maxd = max(d)               # What is the longest distance?
    return (maxd)