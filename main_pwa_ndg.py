# PWA - NDG's attempt
import capytaine as capy
import numpy as np
# Define Array and Waves
wecx = [0, 50, 100]
wecy = [0, 0, 0]
r = 1
omega = 1
beta = 0
g = 9.81

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
print("Initialization completed. On to BEM...")

# Step 1: BEM Potentials
def bem_potentials(bodies,neighbors):
    solver = solver = capy.BEMSolver()
    diff_problem = {body:capy.DiffractionProblem(body=body,omega=omega,wave_direction=beta) for body in bodies}
    diff_result = {body:solver.solve(diff_problem[body]) for body in bodies}
    phi = {effector:
           {effected:solver.compute_potential(effected.home,diff_result[effector])for effected in bodies} 
          for effector in bodies}
    return phi

phi = bem_potentials(bodies,neighbors)
print("BEM completed. On to PWA...")

# Step 2: PWA
def calc_phi_star(bodies,neighbors,phi):
    def pwa_interaction(body_i,body_j,phi_ij):
        k = omega**2/g
        x_i = body_i.home[0]
        y_i = body_i.home[0]
        x_j = body_j.home[0]
        y_j = body_j.home[1]
        theta = np.arctan((y_j-y_i)/(x_j-x_i))
        phi_multiplier = np.exp(1j*k*((x_i-x_j)*np.cos(theta) + (y_i-y_j)*np.sin(theta))) 
        phi_term = phi_ij*phi_multiplier
        return phi_term

    phi_star = {body:sum(pwa_interaction(neighbor,body,phi[neighbor][body]) for neighbor in neighbors[body]) for body in bodies}
    return phi_star

phi_star = calc_phi_star(bodies,neighbors,phi)
print(phi_star)

