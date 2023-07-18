import Model.hydro_submethods.bem_interface as BEM
import Model.hydro_submethods.dynamics as dynamics
import Model.hydro_submethods.pwa_interface as PWA
import numpy as numps

def run(bodies,neighbors,omega,Amp,beta):
    # Babarit Step 1: BEM stuff
    initial_hydro = BEM.initial_hydrodynamics(bodies,neighbors,omega,beta)
    # Step 2: Initialize amplitude matrix
    a = {body1:{body2:0 for body2 in bodies} for body1 in bodies}
    for body in bodies:
        a[body][body] = Amp
    # Step 3: Solve for Motion
    Xi = dynamics.solve(initial_hydro,a,omega,bodies)
    # Step 4: Wierd PWA equations
    phi = PWA.calc_phi(bodies,neighbors,Xi,initial_hydro,a,omega)
    a = PWA.new_a_matrix(bodies,neighbors,phi,omega,a)
    # Step 5: Loop
    if len(bodies) > 1:
        converged = False
        while not converged:
            a_old = a
            Xi = dynamics.solve(initial_hydro,a,omega,bodies)
            phi = PWA.calc_phi(bodies,neighbors,Xi,initial_hydro,a,omega)
            a = PWA.new_a_matrix(bodies,neighbors,phi,omega,a)
            a_diff =[]
            
            for body1 in bodies:
                for body2 in bodies:
                    a_diff.append(numps.abs(a[body1][body2] - a_old[body1][body2]))
            if max(a_diff) <= 0.003:
                converged = True
    M ={body:initial_hydro[body]['M'] for body in bodies}
    return Xi,M