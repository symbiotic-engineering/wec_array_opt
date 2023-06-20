# PWA - NDG's attempt
import capytaine as capy
import numpy as np
from capytaine.bem.airy_waves import airy_waves_potential
# Define Array and Waves
wecx = [0, 50]
wecy = [0, 0]
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
    body.x = x
    body.y = y
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

# BEM time - looking at each wec individually
def indv_phi(bodies):
    solver = capy.BEMSolver()
    diff_problems = {body:capy.DiffractionProblem(body=body,omega=omega,wave_direction=beta) for body in bodies}
    rad_problems = {body:capy.RadiationProblem(body=body,omega=omega) for body in bodies}
    diff_results = {body:solver.solve(problem) for body,problem in diff_problems.items()}
    rad_results = {body:solver.solve(problem) for body,problem in rad_problems.items()}
    phis = {body:airy_waves_potential(np.array([body.x,body.y,0]),problem) for body,problem in diff_problems.items()}
    return phis
phis = indv_phi(bodies)

# Step 1: interactions
