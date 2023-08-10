import capytaine as capy
import numpy as np

def get_body(r,L,x,y,d):
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
    return body

def calc_theta(body,neighbor):
    x_1 = body.home[0]
    y_1 = body.home[1]
    x_2 = neighbor.home[0]
    y_2 = neighbor.home[1]
    theta = np.arctan2((y_1-y_2),(x_1-x_2))  # just some trig
    return theta


def get_neighbors(bodies):
    neighbors = {body:[] for body in bodies}
    for body in bodies:
        for neighbor in bodies:
            if not body == neighbor:
                neighbor.theta = calc_theta(body,neighbor) # angle from neighbor to body, used in pwa
                neighbors[body].append(neighbor)
    return neighbors




def run(wecx,wecy,r,L,ds):
    bodies = [get_body(r,L,x,y,d) for x,y,d in zip(wecx,wecy,ds)]
    return bodies


def grid(r,L,ds): #generate a grid layout and passes bodies for optimization
    wecX, wecY = np.meshgrid(np.linspace(0,50,2),np.linspace(0,50,2))
    wecx = wecX.flatten()
    wecy = wecY.flatten()
    bodies = run(wecx,wecy,r,L,ds)
    return bodies

def line(r,L,ds): #generate line and pass bodies for optimization 
    wecx = np.zeros(4)
    wecy = np.linspace(0,200,4)
    bodies = run(wecx,wecy,r,L,ds)
    return bodies

def random(r,L,ds): #pass optimal random WEC
    wecx = np.array([0,30,10,-30])
    wecy = np.array([0,30,-40,20])
    bodies = run(wecx,wecy,r,L,ds)
    return bodies