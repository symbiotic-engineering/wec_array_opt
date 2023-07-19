import numpy as np
import capytaine as capy
from modules.kd_ratio import disturbance, kd_at_loc
from capytaine.bem.airy_waves import froude_krylov_force
import time
def run(bodies,beta,omega,max_loc,gps):
    start_time = time.time()
    wec_array = bodies[0]
    for ii in range(len(bodies)-1):
        wec_array+=bodies[ii+1]
    end_time = time.time()
    print(f'Array set up time: {end_time-start_time}')

    # Hydrostatics
    start_time = time.time()
    hydrostatics = {body:body.compute_hydrostatics() for body in bodies}
    C = {body:np.array(hydrostatics[body]["hydrostatic_stiffness"]) for body in bodies}
    M = {body:np.array(hydrostatics[body]["inertia_matrix"]) for body in bodies}
    end_time = time.time()
    print(f'Hydrostatics time: {end_time-start_time}')

    # Solve radiation problems, and diffraction problem
    start_time = time.time()
    solver = capy.BEMSolver()
    dofs = {body:f'{body.name}__Heave' for body in bodies}
    rad_prob = [capy.RadiationProblem(body=wec_array,omega=omega,radiating_dof=dofs[body]) for body in bodies]
    rad_result = solver.solve_all(rad_prob,keep_details=(True))
    diff_prob = capy.DiffractionProblem(body=wec_array, wave_direction=beta, omega=omega)
    diff_result = solver.solve(diff_prob,keep_details=(True))
    
    # Get the important stuff
    dataset = capy.assemble_dataset(rad_result + [diff_result])
    A = {body:np.array(dataset['added_mass'].sel(radiating_dof = dofs[body], influenced_dof = dofs[body])) for body in bodies}
    B = {body:np.array(dataset['radiation_damping'].sel(radiating_dof = dofs[body], influenced_dof = dofs[body])) for body in bodies}
    diff_F = {body:np.array(dataset['diffraction_force'].sel(influenced_dof = f'{body.name}__Heave')) for body in bodies}
    FK_F =  {body:np.array(dataset['Froude_Krylov_force'].sel(influenced_dof = f'{body.name}__Heave')) for body in bodies}
    F = {body:diff_F[body] + FK_F[body] for body in bodies}
    end_time = time.time()
    print(f'Hydro terms time:  {end_time-start_time}')

    # Get the Kd for each wec
    start_time = time.time()
    Kd, X, Y = disturbance(bodies,diff_result,rad_result,max_loc,gps)
    kd = kd_at_loc(bodies,Kd,X,Y)
    end_time = time.time()
    print(f'Disturbances time: {end_time-start_time}')
    kd_time = end_time-start_time
    return A,B,C,F,M,kd, kd_time