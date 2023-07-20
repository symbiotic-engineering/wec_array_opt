import modules.model_nWECs as model
import numpy as np
def min_d(x,p):
    nwec = int(p[3])                 # Number of WECs
    wec_radius, wec_length, wecx, wecy, damp = model.unpack_x(x,nwec)
    d = []
    for i in range(nwec):
        for j in range(i+1,nwec):
            d.append(((wecx[i]-wecx[j])**2 + (wecy[i]-wecy[j])**2)**(1/2))      # Compute the distance
    mind = min(d)               # What is the shortest distance?
    return (mind)