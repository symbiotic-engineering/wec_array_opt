import capytaine as capy
import numpy as np

def get_body(r,x,y):
    mesh = capy.meshes.predefined.mesh_sphere(radius=r,center=(x,y,0))
    body = capy.FloatingBody(mesh)
    body.add_translation_dof(name='Heave')
    body = body.immersed_part()
    body.name = f'{x}_{y}'
    body.home = np.array([x,y,0])
    body.radius = r
    return body

def get_neighbors(bodies):
    neighbors = {body:[] for body in bodies}
    for body in bodies:
        for neighbor in bodies:
            if not body == neighbor:
                neighbors[body].append(neighbor)
    return neighbors

def run(wecx,wecy,r):
    bodies = [get_body(r,x,y) for x,y in zip(wecx,wecy)]
    neighbors = get_neighbors(bodies)
    return bodies,neighbors
