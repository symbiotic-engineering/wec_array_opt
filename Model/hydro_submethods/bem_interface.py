import capytaine as capy
import numpy as np
from capytaine.bem.airy_waves import airy_waves_potential as incident_potential
from capytaine.bem.airy_waves import froude_krylov_force as FK_force

def initial_hydrodynamics(bodies,neighbors,omega,beta):
    rad_problem = {body:capy.RadiationProblem(body=body,omega=omega) for body in bodies}
    solver = capy.BEMSolver()
    rad_result = {body:solver.solve(rad_problem[body]) for body in bodies}
    A = {body:rad_result[body].added_masses['Heave'] for body in bodies}
    B = {body:rad_result[body].radiation_dampings['Heave'] for body in bodies}
    hydrostatics = {body:body.compute_hydrostatics() for body in bodies}
    C = {body:np.array(hydrostatics[body]["hydrostatic_stiffness"]) for body in bodies}
    M = {body:np.array(hydrostatics[body]["inertia_matrix"]) for body in bodies}
    sig_r = {body:rad_result[body].sources for body in bodies}
    
    # Diagonal Diffraction
    diff_problem = {body:capy.DiffractionProblem(body=body,omega=omega,wave_direction=beta) for body in bodies}
    diff_result = {body:solver.solve(diff_problem[body]) for body in bodies}
    sig_d_diag = {body:diff_result[body].sources for body in bodies}
    Fd_diag = {body:diff_result[body].forces['Heave'] for body in bodies}
    Fk = {body:FK_force(diff_problem[body])['Heave'] for body in bodies}
    F_diag = {body:Fk[body] + Fd_diag[body] for body in bodies}
    # Off-Diagonal Diffraction
    diff_problem = {body:{neighbor:
                          capy.DiffractionProblem(body=body,omega=omega,wave_direction=neighbor.theta) 
                    for neighbor in neighbors} for body in bodies}
    diff_result = {body:{neighbor:solver.solve(diff_problem[body][neighbor]) for neighbor in neighbors} for body in bodies}
    sig_d_off = {body:{neighbor:diff_result[body][neighbor].sources for neighbor in neighbors} for body in bodies}
    F_off = {body:{neighbor:diff_result[body][neighbor].forces['Heave'] for neighbor in neighbors} for body in bodies}

    # Put it all together
    F = {body:{neighbor:[] for neighbor in bodies} for body in bodies}
    sig_d = {body:{neighbor:[] for neighbor in bodies} for body in bodies}
    for body in bodies:
        for neighbor in bodies:
            if neighbor == body:
                F[body][neighbor] = F_diag[body]
                sig_d[body][neighbor] = sig_d_diag[body]
            else:
                F[body][neighbor] = F_off[body][neighbor]
                sig_d[body][neighbor] = sig_d_off[body][neighbor]
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