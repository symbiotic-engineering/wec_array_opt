import numpy as np
import pandas as pd
from smt.sampling_methods import LHS
from concurrent.futures import ProcessPoolExecutor
import random, os , sys
import capytaine as capy
random.seed(0)
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.insert(0,parent_folder)

import modules.model_nWECs as model
import modules.distances as dis

def body_resolution(r,L,nr,ntheta,nx):
    #generate cylinder for 0,0
    mesh = capy.meshes.predefined.mesh_vertical_cylinder(radius=r,center=(0,0,0), length=L,resolution = (nr,ntheta,nx))
    body = capy.FloatingBody(mesh)
    body.add_translation_dof(name='Heave')
    body.keep_immersed_part()
    body = body.immersed_part()
    body.name = f"{radius}_{length_ratio}"
    return body

nr = [8,10,15,20] #(nr) number of panels along a radius on the extremities of the cylinder
ntheta = [10,20,24,30] #(ntheta) number of panels along a circular slice of the cylinder
nx = [5,10,15,25] #number of circular slices(nx) ,


#Latin hypercube sampling to get representative design in the design space.
radius,length_ratio = [1,10], [1,3]
designs = np.array([radius, length_ratio])
sampling = LHS(xlimits=designs)
num = 10
inputs_dim = sampling(num)
print(f"inputs_designs are {inputs_dim}")
df = pd.DataFrame(inputs_dim)

panels = np.array([nr,nx,ntheta])
#Latin hypercube sampling to get representative design in the design space.
sampling = LHS(xlimits=panels)
num = 10
inputs_panels= sampling(num)
print("panels")
print(inputs_panels)

df = pd.DataFrame(inputs_dim)

# model.run after pack, unpack stuff...

#@NATE add this
omega = 1.02
iteration = 0
print(inputs_dim)
design_Mass = {}
def by_design(inputs,panels):
	name = f"design_{panels[0]}_{panels[1]}_{panels[2]}_{inputs[0]},{inputs[1]}"
	bodies = [body_resolution(inputs[0],inputs[1],int(panels[0]),int(panels[1]),int(panels[2]))]
	nb_faces = {body.name:body.mesh.nb_faces for body in bodies}
	#ds1 = [solve_hydrodynamics(body,0.3) for body in bodies]
	LCOE = []
	omega_range = [omega]
	body_name = []
	df_list= []
	iteration = 0
	with ProcessPoolExecutor(20) as exe:
	# perform calculations
		print("inside ProcessPoolExecutor")
		for lcoe,distance in exe.map(model.run, bodies):
			LCOE.append(lcoe)
			body_name.append(bodies.name)
			pairs = [(face,lcoe) for face,lcoe,bn in zip(nb_faces.values(),lcoe,body_name)]
			pairs = sorted(
			   pairs, 
			    key=lambda x: x[0]
			)

			data = [{'design':bn,'panels':nb_faces,'lcoe':lcoe} for nb_faces,lcoe,bn in pairs ]
			data = pd.DataFrame.from_dict(data)
			df_list.append(data)
			print("appendng dataframe")
			df = pd.concat(df_list)
			df.to_csv(f"data/{name}_{2}.csv")
			iteration+=1
	return iteration


x= [by_design(inputs,panels) for inputs in inputs_dim for panels in inputs_panels]
#fixed..deterministic


