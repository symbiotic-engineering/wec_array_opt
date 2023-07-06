import numpy as np

def calc_phi(bodies,neighbors,Xi,initial_hydro,a,omega):
    sig_r = {body:initial_hydro[body]['sigma_r'] for body in bodies}
    sig_d = {body:initial_hydro[body]['sigma_d'] for body in bodies}
    term1 = {body:sum(-1j*omega*sig_r[body]*Xi[body]) for body in bodies} # first term in integral
    term2 = {body:{neighbor:a[body][neighbor]*sig_d[neighbor] for neighbor in neighbors[body]} for body in bodies}
    phi = {body:
           {neighbor:
            -1/(2*np.pi)*2*sum(term1[body]+term2[body][neighbor]) # When I integrate I need to multiply by dS, I do not do this rn
           for neighbor in neighbors[body]}
          for body in bodies}
    return phi

def new_a_matrix(bodies,neighbors,phi,omega,a):
    g = 9.81
    k = omega**2/g
    for body in bodies:
        for neighbor in neighbors[body]:
            a[body][neighbor] = phi[body][neighbor]/(np.exp(1j*k*((neighbor.home[0]-body.home[0])*np.cos(neighbor.theta) + (neighbor.home[1]-body.home[1])*np.sin(neighbor.theta))))
    return a