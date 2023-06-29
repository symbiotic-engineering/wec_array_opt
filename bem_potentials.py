import capytaine as capy
import numpy as np
from capytaine.bem.airy_waves import airy_waves_potential as incident_potential
# Returns phi matric with interaction terms, what 1 does on 2
def phi_matrix(bodies,omega,beta):
    # use BEM to get potentials, no real interactions yet, just look at potentials generated from each body individually       
    solver = solver = capy.BEMSolver()
    diff_problem = {body:capy.DiffractionProblem(body=body,omega=omega,wave_direction=beta) for body in bodies}
    diff_result = {body:solver.solve(diff_problem[body]) for body in bodies}
    rad_problem = {body:capy.DiffractionProblem(body=body,omega=omega) for body in bodies}
    rad_result = {body:solver.solve(rad_problem[body]) for body in bodies}
    rad_phi = {effecter: # the effecting wec
               {effected:solver.compute_potential(effected.home,rad_result[effecter])for effected in bodies} # the wec being effected
              for effecter in bodies}
    diff_phi = {effecter: # the effecting wec
           {effected:solver.compute_potential(effected.home,diff_result[effecter])for effected in bodies} # the wec being effected
          for effecter in bodies}
    phi = 0
    '''The above line(s) of code may be a bit confusing initially. Basically I'm making a 2d dictonary to act as the phi  matrix
    the first "dimension" is the effecting wec, and the second is the wec being effected. We then calculate the potential caused
    by the effecting wec (using the diffraction result) at the effected wec's home for every combination of effecting and 
    effected wec'''
    return phi

# Returns a vector of potentials, the potential at each wec due only to each itself
def phi_vector(bodies,omega,beta):
    # use BEM to get potentials, no real interactions yet, just look at potentials generated from each body individually       
    solver = solver = capy.BEMSolver()
    diff_problem = {body:capy.DiffractionProblem(body=body,omega=omega,wave_direction=beta) for body in bodies}
    diff_result = {body:solver.solve(diff_problem[body]) for body in bodies}
    rad_problem = {body:capy.DiffractionProblem(body=body,omega=omega) for body in bodies}
    rad_result = {body:solver.solve(rad_problem[body]) for body in bodies}
    diff_phi = {body:solver.compute_potential(body.home,diff_result[body]) for body in bodies}
    rad_phi = {body:solver.compute_potential(body.home,rad_result[body]) for body in bodies}
    inc_phi = {body:incident_potential(body.home,diff_problem[body]) for body in bodies}
    phi = {body:diff_phi[body] + rad_phi[body] + inc_phi[body] for body in bodies}
    return phi
