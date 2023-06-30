import numpy as np

def calc_phi_star(bodies,neighbors,phi,omega):        # uses equation 10 in the paper
    def pwa_interaction(body_i,body_j,phi_ij):  # calculates each term in the sumation
        g = 9.81
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