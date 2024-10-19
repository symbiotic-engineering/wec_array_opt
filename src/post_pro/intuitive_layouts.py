import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0,parent_folder)


import modules.model_nWECs as model
import modules.distances as dis
import numpy as np
from parameters.read_params import read_params

# LCOE for line, circle and other layout and comparsion with optimal layout
# using optimal DVs for the design only as the layout location is different for recommended 
# design
p = read_params(pfile = 'parameters/parameters.csv')
omega = p[0] 

#suggested point --84 index 
#r,L/r,log_d1,log_d2,log_d3,log_d4,LCOE,distance
recommended_design = [8.0,0.100000390005137,5.5762347794275575,5.591921577507208,5.537755861522799,5.545080885661658,0.2246059498436074,67.36699575224688]
# only use design vars not layouts
#84: 8.0,0.100000390005137,5.5762347794275575,33.27859672211952,58.573433541920565,5.591921577507208,37.872518187721504,18.691411350753484,5.537755861522799,-9.834722626629564,38.78588955445712,5.545080885661658,0.2246059498436074,67.36699575224688
r = 4
L = 0.100000390005137 * r
spacing = 40

# Set-up circle array
wecy = np.array([0,0,0,0]) 
wecx = np.array([0,1.0,2.0,3.0])*spacing 
damp = 10**np.array([5.5762347794275575 , 5.591921577507208, 5.537755861522799 ,5.545080885661658 ])

# optimal locs
optimal_wecx = [0,33.27859672211952,37.872518187721504,-9.83]
optimal_wecy = [0,58.573433541920565,18.69,38.78]

x = model.pack_x(optimal_wecx,optimal_wecy,r,L,damp)

wec_radius, wec_length, wecx, wecy, damp, N = model.unpack_x(x)
print(f"WEC Radius: {wec_radius}")
print(f"WEC Length: {wec_length}")
print(f"X Locations: {wecx}")
print(f"Y Locations: {wecy}")
print(f"Damping: {damp}")

print("==================================================================================")

LCOE,AEP,rated_P = model.run(x,p,time_data=True,reactive=True)
print("==================================================================================")
print(f'The LCOE is {LCOE} $/kWh')
print(f'The AEP is {AEP} kWh')
print(f'The Rated Power is {rated_P} kW')
mind = dis.min_d(x,p)
print(f'The min spacing is {mind} m')
maxd = dis.max_d(x,p)
print(f'The max spacing is {maxd} m') 


# for line (b=0 ,(x,y=0) layout:  The LCOE is 0.3527 $/kWh
# for line (b=0 ,(x=0,y) layout : The LCOE is 0.43086 $/kWh
# for diagonal 
    # wecy = np.array([0,0.5,1.0,1.5])*spacing 
    #wecx = np.array([0,0.5,1.5,1.0])(b=0 , x=y) 
    # : The LCOE is 0.39330767496918834 $/kWh

# compared to LCOE of recommended design = 0.2246059498436074
# compared to MIN LCOE design  = 0.21960154836577783
# compared to compact design possible = 0.23059542357914817