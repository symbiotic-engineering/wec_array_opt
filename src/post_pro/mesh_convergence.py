import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from smt.sampling_methods import LHS
import itertools
from concurrent.futures import ProcessPoolExecutor
import random, os , sys
import capytaine as capy
from plotnine import ggplot, aes, facet_wrap, labs, geom_line,scale_color_discrete
import plotnine as pn
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
radius,length_ratio = [3,10], [0.5,2] # r':[2,10], 'L':[0.1,0.2] but L is diferrent here
designs = np.array([radius, length_ratio])
sampling = LHS(xlimits=designs)
num = 6
inputs_dim = sampling(num)

df = pd.DataFrame(inputs_dim)

nr = list(range(2,21,5))#(nr) number of panels along a radius on the extremities of the cylinder
ntheta = list(range(20,40+1,5)) #(ntheta) number of panels along a circular slice of the cylinder
nx = list(range(10,30+1,5)) #number of circular slices(nx) ,
# # default for unit radius and length 10---> nx=10, ntheta=10, nr=2

# Generate all possible combinations
inputs_panels = list(itertools.product(nr, ntheta, nx))
print(inputs_panels)
# model.run after pack, unpack stuff...
omega = 1.02

def by_design(inputs,panels):
    name = f"design_{inputs[0]},{inputs[1]}"
    body = body_resolution(inputs[0],inputs[1],int(panels[0]),int(panels[1]),int(panels[2]))
    body.name = name
    body.resolution = (panels[0],panels[1],panels[2])
    nb_faces = body.mesh.nb_faces 
    Amass , Bamping = get_hydro(body)
    data = {'design':name,'nr':panels[0],'ntheta':panels[1],'nx':panels[2],'panels':nb_faces,'A': float(Amass), 'B':float(Bamping)} 
    return data

data = [by_design(inputs,panels) for inputs in inputs_dim for panels in inputs_panels]
df = pd.DataFrame.from_dict(data)

df.to_csv(f"../../data/mesh_convergence/convergence.csv")
grouped = df.groupby('design').ngroup()
df['design_id'] = 'design' + grouped.astype(str)
df['moving_average'] = df['A'].rolling(window=4, min_periods=4).mean()
plt.figure(figsize=(14,10))
x = ( ggplot(df)
    + facet_wrap(facets="design_id",scales='free')
    + aes(x="panels", y="A")
    + labs(
        x="panels",
        y="A",
        title="",
    )
    #+ geom_line(show_legend=True)+ pn.theme(panel_background=pn.element_blank()) 
    + aes(y='moving_average') +  geom_line(color='red', linetype='dashed')
 + pn.theme(axis_title_y=pn.element_blank())
 + pn.theme(axis_ticks_major_y=pn.element_blank())
 + pn.theme(figure_size=(12, 8))
             ).draw()
x.savefig("plots/mesh_convergence.pdf")