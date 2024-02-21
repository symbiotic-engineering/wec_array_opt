import capytaine as capy
import numpy as np
# This module is used to create the array of bodies, also can be used to get neighbor lists and angles if PWAing

def get_cylinder(r,L,x,y,d):    # creates one WEC body
    # r ->  wec radius
    # L ->  wec length
    # x ->  x location
    # y ->  y location
    # d ->  pto damping
    mesh = capy.meshes.predefined.mesh_vertical_cylinder(radius=r,center=(x,y,0), length=L)
    body = capy.FloatingBody(mesh)
    body.add_translation_dof(name='Heave')
    body.keep_immersed_part()
    body = body.immersed_part()
    body.name = f'{x}_{y}'
    body.home = np.array([x,y,0])
    body.radius = r
    body.center_of_mass=(x, y, 0)
    body.keep_only_dofs(['Heave'])
    body.rotation_center=(x,y,0)
    body.PTOdamp = d
    body.compute_rigid_body_inertia()
    body.compute_hydrostatic_stiffness()
    return body

def get_sphere(r,L,x,y,d): #creates one spherical WEC body
    # r ->  wec radius
    # L ->  wec length (not really needed here but left as a placeholder for consistency)
    # x ->  x location
    # y ->  y location
    # d ->  pto damping
    mesh = capy.meshes.predefined.mesh_sphere(radius = r, center = (x,y,0))
    body = capy.FloatingBody(mesh)
    body.add_translation_dof(name='Heave')
    body.keep_immersed_part()
    body = body.immersed_part()
    body.name = f'{x}_{y}'
    body.home = np.array([x,y,0])
    body.radius = r
    body.center_of_mass=(x, y, 0)
    body.keep_only_dofs(['Heave'])
    body.rotation_center=(x,y,0)
    body.PTOdamp = d
    print("Volume:", body.volume)
    print("Center of buoyancy:", body.center_of_buoyancy)
    print("Wet surface area:", body.wet_surface_area)
    print("Displaced mass:", body.disp_mass(rho=1025))
    print("Waterplane center:", body.waterplane_center)
    print("Waterplane area:", body.waterplane_area)
    print("Metacentric parameters:",
        body.transversal_metacentric_radius,
        body.longitudinal_metacentric_radius,
        body.transversal_metacentric_height,
        body.longitudinal_metacentric_height)
    return body

def calc_theta(body,neighbor):  # old function, useful for PWA
    # bodies    ->  list of wec bodies 
    # neighbors ->  dictionary of other bodies for each body
    x_1 = body.home[0]
    y_1 = body.home[1]
    x_2 = neighbor.home[0]
    y_2 = neighbor.home[1]
    theta = np.arctan2((y_1-y_2),(x_1-x_2))  # just some trig
    return theta


def get_neighbors(bodies):  # old function, useful for PWA
    # bodies->  list of wec bodies 
    neighbors = {body:[] for body in bodies}
    for body in bodies:
        for neighbor in bodies:
            if not body == neighbor:
                neighbor.theta = calc_theta(body,neighbor) # angle from neighbor to body, used in pwa
                neighbors[body].append(neighbor)
    return neighbors



def run(wecx,wecy,r,L,ds): # Initializes the WEC Array, creates the bodies
    # wecx  ->  list of wec x locations
    # wecy  ->  list of wec y locations
    # r     ->  radius of wec
    # L     ->  wec length
    # ds    ->  list of pto dampings
    bodies = [get_cylinder(r,L,x,y,d) for x,y,d in zip(wecx,wecy,ds)]
    return bodies



# Predefined Layouts
def grid(r,L,ds): #generate a grid layout and passes bodies for optimization
    # r     ->  radius of wec
    # L     ->  wec length
    # ds    ->  list of pto dampings
    wecX, wecY = np.meshgrid(np.linspace(0,50,2),np.linspace(0,50,2))
    wecx = wecX.flatten()
    wecy = wecY.flatten()
    bodies = run(wecx,wecy,r,L,ds)
    return bodies

def line(r,L,ds): #generate line and pass bodies for optimization 
    # r     ->  radius of wec
    # L     ->  wec length
    # ds    ->  list of pto dampings
    wecx = np.zeros(4)
    wecy = np.linspace(0,200,4)
    bodies = run(wecx,wecy,r,L,ds)
    return bodies

def random(r,L,ds): #pass optimal random WEC
    # r     ->  radius of wec
    # L     ->  wec length
    # ds    ->  list of pto dampings
    wecx = np.array([0,30,10,-30])
    wecy = np.array([0,30,-40,20])
    bodies = run(wecx,wecy,r,L,ds)
    return bodies