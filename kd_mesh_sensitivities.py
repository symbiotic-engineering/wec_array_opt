import modules.model_nWECs as model
import modules.distances as dis
import numpy as numps
import matplotlib.pyplot as plt
# Runs one array of wecs with different mesh parameters to see what effect they have on run time and AEP
            #  r  L d  x  y d
x = numps.array([10,10,4,100,100,4])    # Design
omega = 0.5
Amp = 1
beta = 0
N = 2
max_locs = numps.linspace(100,1000,10)  # Whole space
max_loc = 300                           # default case
gp_rates = numps.linspace(0.1,2,20)     # whole space
gp_rate = 0.5                           # default case


# Mesh area
kd_time = numps.zeros(len(max_locs))
AEP = numps.zeros(len(max_locs))
for ii in range(len(max_locs)):
    p = numps.array([omega,Amp,beta,N,max_locs[ii],gp_rate])
    LCOE,AEP[ii],kd_time[ii] = model.run(x,p)
    print("=========================================")

plt.figure(1)
plt.plot(max_locs,AEP)
plt.xlabel('1/2 Mesh dimension [m]')
plt.ylabel('AEP [kWh]')
plt.figure(2)
plt.plot(max_locs,kd_time)
plt.xlabel('1/2 Mesh dimension [m]')
plt.ylabel('Disturbacne Time [s]')

# How fine is the mesh?
kd_time = numps.zeros(len(gp_rates))
AEP = numps.zeros(len(gp_rates))
for ii in range(len(gp_rates)):
    p = numps.array([omega,Amp,beta,N,max_loc,gp_rates[ii]])
    LCOE,AEP[ii],kd_time[ii] = model.run(x,p)
    print("=========================================")

plt.figure(3)
plt.plot(gp_rates,AEP)
plt.xlabel('Grid points per 2 m')
plt.ylabel('AEP [kWh]')
plt.figure(4)
plt.plot(gp_rates,kd_time)
plt.xlabel('Grid points per 2 m')
plt.ylabel('Disturbacne Time [s]')

plt.figure(1)
plt.show()
plt.figure(2)
plt.show()
plt.figure(3)
plt.show()
plt.figure(4)
plt.show()