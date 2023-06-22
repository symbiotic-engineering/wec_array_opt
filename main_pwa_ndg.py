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
                neighbors[body].append(neighbor.home)
    return neighbors
neighbors = get_neighbors(bodies)
print(neighbors)

# BEM time - looking at each wec individually
def indv_phi(bodies):
    solver = capy.BEMSolver()
    diff_problems = {body:capy.DiffractionProblem(body=body,omega=omega,wave_direction=beta) for body in bodies}
    rad_problems  = {body:capy.RadiationProblem(body=body,omega=omega) for body in bodies}
    diff_results  = {body:solver.solve(diff_problems[body]) for body in bodies}
    rad_results   = {body:solver.solve(rad_problems[body]) for body in bodies}
    phis = {body:airy_waves_potential(body.home,diff_problems[body]) for body in bodies}
    return phis
phis = indv_phi(bodies)
print("================Indvidual Phis===================")
print(phis)

# BEM - off diagonals, not helpful
def neighbor_phi(bodies,neighbors):
    solver = capy.BEMSolver()
    diff_problems = {body:capy.DiffractionProblem(body=body,omega=omega,wave_direction=beta) for body in bodies}
    rad_problems  = {body:capy.RadiationProblem(body=body,omega=omega) for body in bodies}
    diff_results  = {body:solver.solve(diff_problems[body]) for body in bodies}
    rad_results   = {body:solver.solve(rad_problems[body]) for body in bodies}
    phis = {body:airy_waves_potential(np.array(neighbors[body]),diff_problems[body]) for body in bodies}
    return phis
phis = neighbor_phi(bodies,neighbors)
print("================Neighbor Phis===================")
print(phis)

def phi_incident(body):
    g = 9.81
    k = omega**2/g
    phi = g/omega*np.exp(k*(body.home[0]*np.cos(beta) + body.home[1]*np.sin(beta))*1j)
    return phi
phis = {body:phi_incident(body) for body in bodies}
print("================Nate's Phis===================")
print(phis)
print("My phis are just incident, but if you multiply them by -j, you get the BEM results... hmmm")

# Step 1: interactions
