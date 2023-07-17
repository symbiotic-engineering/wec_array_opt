import numpy as np

def calc_phi(bodies,neighbors,Xi,initial_hydro,a,omega):
    sig_r = {body:initial_hydro[body]['sigma_r'] for body in bodies}
    sig_d = {body:{neighbor:initial_hydro[body]['sigma_d'][neighbor] for neighbor in neighbors[body]} for body in bodies}
    term1 = {body:sum(-1j*omega*sig_r[body]*Xi[body]) for body in bodies} # first term in integral
    term2_sub = {body:{neighbor:a[body][neighbor]*sig_d[body][neighbor] for neighbor in neighbors[body]} for body in bodies}
    term2 = {body:0+0j for body in bodies}
    for body in bodies:
        for neighbor in neighbors[body]:
            term2[body] += term2_sub[body][neighbor]
    phi = {body:
           {neighbor:
            -1/(4*np.pi)*neighbor.mesh.surface_integral(term1[neighbor]+term2[neighbor])
           for neighbor in neighbors[body]}
          for body in bodies}
    return phi

def new_a_matrix(bodies,neighbors,phi,omega,a):
    g = 9.81
    k = omega**2/g
    for body in bodies:
        for neighbor in neighbors[body]:
            a[body][neighbor] = phi[body][neighbor]*omega/(g*np.exp(1j*k*(body.home[0]*np.cos(neighbor.theta) + body.home[1]*np.sin(neighbor.theta))))
    return a