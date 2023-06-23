# PWA - NDG's attempt
import capytaine as capy
import numpy as np
from capytaine.bem.airy_waves import airy_waves_potential
# Define Array and Waves
wecx = [0, 50, 100]
wecy = [0, 0, 0]
r = 1
omega = 1
beta = 0

# Get the Bodies
def get_body(r,x,y):
    mesh = capy.meshes.predefined.mesh_sphere(radius=r,center=(x,y,0))
    body = capy.FloatingBody(mesh)
    body.add_translation_dof(name='Heave')
    body = body.immersed_part()
    body.name = f'{x}_{y}_{r}'
    body.home = np.array([x,y,0])
    return body 

N = len(wecx)
bodies = [get_body(r,x,y) for x,y in zip(wecx,wecy)]

# Potentially usefull function
def get_neighbors(bodies):
    neighbors = {body:[] for body in bodies}
    for body in bodies:
        for neighbor in bodies:
            if not body == neighbor:
                neighbors[body].append(neighbor)
    return neighbors
neighbors = get_neighbors(bodies)

# BEM Potentials
def bem_potentials(bodies,neighbors):
    solver = solver = capy.BEMSolver()
    diff_problem = {body:capy.DiffractionProblem(body=body,omega=omega,wave_direction=beta) for body in bodies}
    diff_result = {body:solver.solve(diff_problem[body]) for body in bodies}
    phi = {effector:
           {effected:solver.compute_potential(effected.home,diff_result[effector])for effected in bodies} 
          for effector in bodies}
    return phi

phi = bem_potentials(bodies,neighbors)
print(phi)

# Step 1: interactions
