import numpy as np
import capytaine as capy
from capytaine.bem.airy_waves import froude_krylov_force

def run(bodies,beta,omega):
    wec_array = bodies[0]
    for ii in range(len(bodies)-1):
        wec_array+=bodies[ii+1]
    
    hydrostatics = {body:body.compute_hydrostatics() for body in bodies}
    C = {body:np.array(hydrostatics[body]["hydrostatic_stiffness"]) for body in bodies}
    M = {body:np.array(hydrostatics[body]["inertia_matrix"]) for body in bodies}

    solver = capy.BEMSolver()
    #rad_prob = {body:capy.RadiationProblem(body=body,omega=omega) for body in bodies}
    #rad_result = {body:solver.solve(rad_prob[body],keep_details=(True)) for body in bodies}
    #A = {body:rad_result[body].added_masses['Heave'] for body in bodies}
    #B = {body:rad_result[body].radiation_dampings['Heave'] for body in bodies}
    dofs = {body:f'{body.name}__Heave' for body in bodies}
    rad_prob = [capy.RadiationProblem(body=wec_array,omega=omega,radiating_dof=dofs[body]) for body in bodies]
    rad_result = solver.solve_all(rad_prob,keep_details=(True))
    
    diff_prob = capy.DiffractionProblem(body=wec_array, wave_direction=beta, omega=omega)
    diff_result = solver.solve(diff_prob,keep_details=(True))
    dataset = capy.assemble_dataset(rad_result + [diff_result])
    A = {body:np.array(dataset['added_mass'].sel(radiating_dof = dofs[body], influenced_dof = dofs[body])) for body in bodies}
    B = {body:np.array(dataset['radiation_damping'].sel(radiating_dof = dofs[body], influenced_dof = dofs[body])) for body in bodies}
    diff_F = {body:np.array(dataset['diffraction_force'].sel(influenced_dof = f'{body.name}__Heave')) for body in bodies}
    FK_F =  {body:np.array(dataset['Froude_Krylov_force'].sel(influenced_dof = f'{body.name}__Heave')) for body in bodies}
    F = {body:diff_F[body] + FK_F[body] for body in bodies}
    return A,B,C,F,M