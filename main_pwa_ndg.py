# PWA - NDG's attempt
import numpy as np
import time 
import wec_array_initialization as array_init
import bem_potentials as bem
# Define Array and Waves
wecx = [0, 10000000000]
wecy = [0, 0]
r = 1
omega = 1
beta = 0
g = 9.81

# Array Initialization
N = len(wecx)
bodies,neighbors = array_init.run(wecx,wecy,r)
print("Initialization completed. On to BEM...")
start_time = time.perf_counter()

# Step 1: BEM Potentials
phi = bem.phi_matrix(bodies,omega,beta)
print(phi)
end_time = time.perf_counter()
total_time = end_time-start_time
print(f"BEM completed in {total_time} seconds.")
print("On to PWA...")
start_time = time.perf_counter()

# Step 2: PWA
def calc_phi_star(bodies,neighbors,phi):        # uses equation 10 in the paper
    def pwa_interaction(body_i,body_j,phi_ij):  # calculates each term in the sumation
        k = omega**2/g
        x_i = body_i.home[0]
        y_i = body_i.home[1]
        x_j = body_j.home[0]
        y_j = body_j.home[1]
        theta = np.arctan2((y_j-y_i),(x_j-x_i))  # just some trig

        # First get the exponential term that multiplies the potential, should be bounded by -1 and 1
        phi_multiplier = np.exp(1j*k*((x_i-x_j)*np.cos(theta)+(y_i-y_j)*np.sin(theta))) 
        phi_term = phi_ij*phi_multiplier        # the term for eq 10, phi_ij times the exponential thingy
        return phi_term
    phi_star = {body: # for each body
                sum(pwa_interaction(neighbor,body,phi[neighbor][body]) for neighbor in neighbors[body]) # sum effects of neighbors
               for body in bodies}
    return phi_star

phi_star = calc_phi_star(bodies,neighbors,phi) # eq 10
print(phi_star)
end_time = time.perf_counter()
total_time = end_time-start_time
print(f"First PWA phi calculated in {total_time} seconds.")
