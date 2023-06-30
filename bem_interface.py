import capytaine as capy
import numpy as np
from capytaine.bem.airy_waves import airy_waves_potential as incident_potential

def total_phi(bodies,diff_problem,rad_problem):
    # solve problems
    solver = solver = capy.BEMSolver()
    diff_result = {body:solver.solve(diff_problem[body]) for body in bodies}
    rad_result = {body:solver.solve(rad_problem[body]) for body in bodies}

    # get individual phis
    rad_phi = {effecter: # the effecting wec
               {effected:solver.compute_potential(effected.home,rad_result[effecter])for effected in bodies} # the wec being effected
              for effecter in bodies}
    diff_phi = {effecter: # the effecting wec
                {effected:solver.compute_potential(effected.home,diff_result[effecter])for effected in bodies} # the wec being effected
               for effecter in bodies}
    '''The above line(s) of code may be a bit confusing initially. Basically I'm making a 2d dictonary to act as the phi  matrix
    the first "dimension" is the effecting wec, and the second is the wec being effected. We then calculate the potential caused
    by the effecting wec (using the diffraction result) at the effected wec's home for every combination of effecting and 
    effected wec'''
    inc_phi = {body:incident_potential(body.home,diff_problem[body]) for body in bodies}

    # sum totals
    phi = {effecter:
           {effected: rad_phi[effecter][effected]+diff_phi[effecter][effected] for effected in bodies}
          for effecter in bodies}
    # incident only adds to diagonal terms
    for body in bodies:
        phi[body][body] += inc_phi[body] # add in the incident potential
    return phi
    
# Returns phi matric with interaction terms, what 1 does on 2
def isolated_potentials(bodies,omega,beta):
    # use BEM to get potentials, no real interactions yet, just look at potentials generated from each body individually       
    diff_problem = {body:capy.DiffractionProblem(body=body,omega=omega,wave_direction=beta) for body in bodies}
    rad_problem = {body:capy.DiffractionProblem(body=body,omega=omega) for body in bodies}
    
    phi = total_phi(bodies,diff_problem,rad_problem)
    return phi

def update_bem_bnds(diff_problem,phi_star):
    diff_problem.boundary_condition += phi_star
    return diff_problem

def phi_vector2matrix(phi_star,bodies,omega,beta):
    diff_problem = {body:capy.DiffractionProblem(body=body,omega=omega,wave_direction=beta) for body in bodies}
    diff_problem = {body:update_bem_bnds(diff_problem[body],phi_star[body]) for body in bodies}
    rad_problem = {body:capy.DiffractionProblem(body=body,omega=omega) for body in bodies}
    phi = total_phi(bodies,diff_problem,rad_problem)
    return phi