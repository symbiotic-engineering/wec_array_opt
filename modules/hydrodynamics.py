import numpy as np
import capytaine as capy
from capytaine.bem.airy_waves import froude_krylov_force
from capytaine.io.xarray import assemble_dataset, hydrostatics_dataset
from capytaine.post_pro.rao import rao
import time
# This module is used to get all the hydro terms. Forces, added mass, damping, hydrostatic stiffness, and mass

def run(bodies,beta,omega,time_data):
    start_time = time.time()
    wec_array = bodies[0]           # build the array by putting all the bodies together
    for ii in range(len(bodies)-1):
        wec_array+=bodies[ii+1]
    end_time = time.time()
    if time_data == 1:  # prints time info if switched on
        print(f'Array set up time: {end_time-start_time}')

    # Hydrostatics - gets hydrostatic stiffness and mass
    start_time = time.time()
    hydrostatics = {body:body.compute_hydrostatics() for body in bodies}                # solves hydrostatics problem (no waves)
    C = {body:np.array(hydrostatics[body]["hydrostatic_stiffness"]) for body in bodies} # hydrostatic stiffness
    M = {body:np.array(hydrostatics[body]["inertia_matrix"]) for body in bodies}        # mass
    end_time = time.time()
    if time_data == 1:  # prints time info if switched on
        print(f'Hydrostatics time: {end_time-start_time}')

    # Solve radiation problems, and diffraction problem
    start_time = time.time()
    engine = capy.HierarchicalToeplitzMatrixEngine(ACA_distance = 30,ACA_tol = 1e-1,matrix_cache_size=2) #at least three radius - ???
    #engine = capy.BasicMatrixEngine()
    solver = capy.BEMSolver(engine = engine)    # creates the solver using the defined engine
    
    # select DOFs
    if len(bodies) > 1: # if an array of more than 1
        dofs = {body:f'{body.name}__Heave' for body in bodies}  # add the dofs of all wecs
    else:
        dofs = {body:'Heave' for body in bodies}                # just do heave if only 1 wec
        
    # create problems and solve
    rad_prob = [capy.RadiationProblem(body=wec_array,omega=omega,radiating_dof=dofs[body]) for body in bodies]  # radiation
    rad_result = solver.solve_all(rad_prob,keep_details=(True))
    diff_prob = capy.DiffractionProblem(body=wec_array, wave_direction=beta, omega=omega)                       # diffraction
    diff_result = solver.solve(diff_prob,keep_details=(True))
    
    # Get the important stuff
    dataset = capy.assemble_dataset(rad_result + [diff_result])
    A = {effected:{effecting:np.array(dataset['added_mass'].sel(radiating_dof = dofs[effecting], influenced_dof = dofs[effected])) for effecting in bodies} for effected in bodies} # added mass
    B = {effected:{effecting:np.array(dataset['radiation_damping'].sel(radiating_dof = dofs[effecting], influenced_dof = dofs[effected])) for effecting in bodies} for effected in bodies} # damping
    diff_F = {body:np.array(dataset['diffraction_force'].sel(influenced_dof = dofs[body])) for body in bodies}  # diffraction force
    FK_F =  {body:np.array(dataset['Froude_Krylov_force'].sel(influenced_dof = dofs[body])) for body in bodies} # froude-krylov force
    F = {body:diff_F[body] + FK_F[body] for body in bodies} # total force
    end_time = time.time()
    if time_data == 1:  # prints time info if switched on - where the bulk of time is spent
        print(f'Hydro terms time:  {end_time-start_time}')
    return A,B,C,F,M
