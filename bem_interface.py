import capytaine as capy
import numpy as np
from capytaine.bem.airy_waves import airy_waves_potential as incident_potential
from capytaine.bem.airy_waves import froude_krylov_force as FK_force

def initial_hydrodynamics(bodies,omega,beta):
    rad_problem = {body:capy.RadiationProblem(body=body,omega=omega) for body in bodies}
    solver = capy.BEMSolver()
    rad_result = {body:solver.solve(rad_problem[body]) for body in bodies}
    A = {body:rad_result[body].added_masses['Heave'] for body in bodies}
    B = {body:rad_result[body].radiation_dampings['Heave'] for body in bodies}
    hydrostatics = {body:body.compute_hydrostatics() for body in bodies}
    C = {body:np.array(hydrostatics[body]["hydrostatic_stiffness"]) for body in bodies}
    M = {body:np.array(hydrostatics[body]["inertia_matrix"]) for body in bodies}
    sig_r = {body:rad_result[body].sources for body in bodies}
    
    diff_problem = {body:capy.DiffractionProblem(body=body,omega=omega,wave_direction=beta) for body in bodies}
    diff_result = {body:solver.solve(diff_problem[body]) for body in bodies}
    sig_d = {body:diff_result[body].sources for body in bodies}
    Fd = {body:diff_result[body].forces['Heave'] for body in bodies}
    Fk = {body:FK_force(diff_problem[body])['Heave'] for body in bodies}
    F = {body:Fd[body] + Fk[body] for body in bodies}
    initial_hydro = {body:{
                     'A':A[body],
                     'B':B[body],
                     'C':C[body],
                     'M':M[body],
                     'sigma_r':sig_r[body],
                     'sigma_d':sig_d[body],
                     'F':F[body]
                    } for body in bodies}
    return initial_hydro

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
    phi = diff_phi
    return phi
    
# Returns phi matric with interaction terms, what 1 does on 2
def isolated_potentials(bodies,omega,beta):
    # use BEM to get potentials, no real interactions yet, just look at potentials generated from each body individually       
    diff_problem = {body:capy.DiffractionProblem(body=body,omega=omega,wave_direction=beta) for body in bodies}
    rad_problem = {body:capy.RadiationProblem(body=body,omega=omega) for body in bodies}
    
    phi = total_phi(bodies,diff_problem,rad_problem)
    return phi

def update_bem_bnds(diff_problem,phi_star):
    diff_problem.boundary_condition += phi_star
    return diff_problem

def phi_vector2matrix(phi_star,bodies,omega,beta):
    diff_problem = {body:capy.DiffractionProblem(body=body,omega=omega,wave_direction=beta) for body in bodies}
    diff_problem = {body:update_bem_bnds(diff_problem[body],phi_star[body]) for body in bodies}
    rad_problem = {body:capy.RadiationProblem(body=body,omega=omega) for body in bodies}
    phi = total_phi(bodies,diff_problem,rad_problem)
    return phi