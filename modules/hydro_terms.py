import numpy as np
import capytaine as capy
from capytaine.bem.airy_waves import froude_krylov_force
import time
def run(bodies,beta,omega,time_data):
    start_time = time.time()
    wec_array = bodies[0]
    for ii in range(len(bodies)-1):
        wec_array+=bodies[ii+1]
    end_time = time.time()
    if time_data == 1:
        print(f'Array set up time: {end_time-start_time}')

    # Hydrostatics
    start_time = time.time()
    hydrostatics = {body:body.compute_hydrostatics() for body in bodies}
    C = {body:np.array(hydrostatics[body]["hydrostatic_stiffness"]) for body in bodies}
    M = {body:np.array(hydrostatics[body]["inertia_matrix"]) for body in bodies}
    end_time = time.time()
    if time_data == 1:
        print(f'Hydrostatics time: {end_time-start_time}')

    # Solve radiation problems, and diffraction problem
    start_time = time.time()
    engine = capy.HierarchicalToeplitzMatrixEngine(ACA_distance = 20,ACA_tol = 1e-1) #at least three radius
    solver = capy.BEMSolver(engine = engine)
    if len(bodies) > 1:
        dofs = {body:f'{body.name}__Heave' for body in bodies}
    else:
        dofs = {body:'Heave' for body in bodies} 
    rad_prob = [capy.RadiationProblem(body=wec_array,omega=omega,radiating_dof=dofs[body]) for body in bodies]
    rad_result = solver.solve_all(rad_prob,keep_details=(True),n_jobs=10)
    diff_prob = capy.DiffractionProblem(body=wec_array, wave_direction=beta, omega=omega)
    diff_result = solver.solve(diff_prob,keep_details=(True))
    
    # Get the important stuff
    dataset = capy.assemble_dataset(rad_result + [diff_result])
    A = {body:np.array(dataset['added_mass'].sel(radiating_dof = dofs[body], influenced_dof = dofs[body])) for body in bodies}
    B = {body:np.array(dataset['radiation_damping'].sel(radiating_dof = dofs[body], influenced_dof = dofs[body])) for body in bodies}
    diff_F = {body:np.array(dataset['diffraction_force'].sel(influenced_dof = dofs[body])) for body in bodies}
    FK_F =  {body:np.array(dataset['Froude_Krylov_force'].sel(influenced_dof = dofs[body])) for body in bodies}
    F = {body:diff_F[body] + FK_F[body] for body in bodies}
    end_time = time.time()
    if time_data == 1:
        print(f'Hydro terms time:  {end_time-start_time}')
    return A,B,C,F,M
