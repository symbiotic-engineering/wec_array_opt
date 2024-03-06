import numpy as np
import pandas as pd
from smt.sampling_methods import LHS
from concurrent.futures import ProcessPoolExecutor
import random, os , sys
import capytaine as capy
random.seed(0)
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.insert(0,parent_folder)

import modules.hydro_terms as hydro
import modules.distances as dis

def body_resolution(r,L,nr,ntheta,nx):
    #generate cylinder for 0,0
    mesh = capy.meshes.predefined.mesh_vertical_cylinder(radius=r,center=(0,0,0), length=L,resolution = (nr,ntheta,nx))
    body = capy.FloatingBody(mesh,dofs = capy.rigid_body_dofs(rotation_center=[0,0,0]))
    body.add_translation_dof(name='Heave')
    body.keep_immersed_part()
    body = body.immersed_part()
    body.center_of_mass = (0, 0, 0)
    body.radius = r
    return body


def get_hydro(body):
   
    C = body.compute_hydrostatics()              # solves hydrostatics problem (no waves)
    # hydrostatic stiffness
    M = np.array(C["inertia_matrix"])     # mass
    engine = capy.BasicMatrixEngine() 
    solver = capy.BEMSolver(engine = engine)    # creates the solver using the defined engine
          
    # create problems and solve
    rad_prob = [capy.RadiationProblem(body=body,omega=1.02,radiating_dof='Heave') for body in [body]]  # radiation
    rad_result = solver.solve_all(rad_prob,keep_details=(True))
    diff_prob = capy.DiffractionProblem(body=body, omega=1.02)                       # diffraction
    diff_result = solver.solve(diff_prob,keep_details=(True))
    
    # Get the important stuff
    dataset = capy.assemble_dataset(rad_result + [diff_result])
   
    A = dataset['added_mass'].sel(radiating_dof = 'Heave', influenced_dof = 'Heave') 
   
    B = dataset['radiation_damping'].sel(radiating_dof = 'Heave',influenced_dof = 'Heave')
    return A[0],B[0]


#Latin hypercube sampling to get representative design in the design space.
radius,length_ratio = [1,10], [1,3]
designs = np.array([radius, length_ratio])
sampling = LHS(xlimits=designs)
num = 100
inputs_dim = sampling(num)

df = pd.DataFrame(inputs_dim)

nr = [8,20] #(nr) number of panels along a radius on the extremities of the cylinder
ntheta = [10,30] #(ntheta) number of panels along a circular slice of the cylinder
nx = [5,25] #number of circular slices(nx) ,

#Latin hypercube sampling to get all representative panels in the design space.
panels = np.array([nr,nx,ntheta])
sampling = LHS(xlimits=panels)
num = 50
inputs_panels= sampling(num)

print(inputs_panels)

# model.run after pack, unpack stuff...
omega = 1.02

def by_design(inputs,panels):
    name = f"design_{panels[0]}_{panels[1]}_{panels[2]}_{inputs[0]},{inputs[1]}"
    body = body_resolution(inputs[0],inputs[1],int(panels[0]),int(panels[1]),int(panels[2]))
    body.name = name
    nb_faces = body.mesh.nb_faces 
    Amass , Bamping = get_hydro(body)
    data = {'design':name,'panels':nb_faces,'A': float(Amass), 'B':float(Bamping)} 
    return data

data = [by_design(inputs,panels) for inputs in inputs_dim for panels in inputs_panels]
df = pd.DataFrame.from_dict(data)
df.to_csv(f"../../data/mesh_convergence/convergence.csv")



