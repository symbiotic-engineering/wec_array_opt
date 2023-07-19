# this mod gives you the disturbance coefficient throughout the wave field
import capytaine as cpt
import numpy as np
from capytaine.bem.airy_waves import froude_krylov_force
import scipy.interpolate as scipy_interp

def disturbance(bodies,diff_result,rad_result,max_loc,gps):
    # position data from array
    xmin = -max_loc
    xmax = max_loc
    ymin = -max_loc
    ymax = max_loc
    
    # creating mesh of free surface

    solver = cpt.BEMSolver()
    free_surface = cpt.FreeSurface(x_range=(xmin, xmax), y_range=(ymin, ymax), nx=gps, ny=gps)
    diffraction_elevation_at_faces = np.array(solver.get_free_surface_elevation(diff_result, free_surface))
    radiation_elevation_at_faces = np.array(sum(solver.get_free_surface_elevation(rad_res, free_surface) for rad_res in rad_result))

    # add incoming waves
    h_i = free_surface.incoming_waves(diff_result)
    h_t = (diffraction_elevation_at_faces + h_i + radiation_elevation_at_faces)
    kd = np.array(h_t/h_i)
    x = np.linspace(xmin,xmax,gps)
    y = np.linspace(ymin,ymax,gps)
    Kd = kd.reshape(gps,gps)
    X, Y = np.meshgrid(x, y)
    return Kd, X, Y

def kd_at_loc(bodies,Kd, X, Y):
    homes = {body:(body.home[0],body.home[1]) for body in bodies}
    kd = {body:scipy_interp.griddata((X.flatten(),Y.flatten()),Kd.flatten(),homes[body]) for body in bodies}
    return kd
