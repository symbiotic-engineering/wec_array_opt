import numpy as np
import time 
import wec_array_initialization as array_init
import bem_interface as bem
import pwa_interface as pwa

# Define Array and Waves
wecx = [0, 100]
wecy = [0, 0]
r = 10
omega = 1
beta = 0
g = 9.81

# Array Initialization
N = len(wecx)
bodies,neighbors = array_init.run(wecx,wecy,r)

# Step 1: BEM Potentials
phi = bem.isolated_potentials(bodies,omega,beta)
print(phi)
print("======================================= BEM complete on to PWA =======================================")

# Step 2: PWA
for ii in range(2*N):
    phi_star = pwa.calc_phi_star(bodies,neighbors,phi,omega) # eq 10
    phi = bem.phi_vector2matrix(phi_star,bodies,omega,beta)
print(phi)