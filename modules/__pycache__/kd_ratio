# this mod gives you the disturbance coefficient throughout the wave field
import capytaine as cpt
import numpy as np
from capytaine.bem.airy_waves import froude_krylov_force

def disturbance(wecx,wecy,diff_result,rad_result):
    # position data from array
    xmin = min(wecx)
    xmax = max(wecx)
    ymin = min(wecy)
    ymax = max(wecy)

    # creating mesh of free surface
    solver = cpt.BEMSolver()
    free_surface = cpt.FreeSurface(x_range=(xmin, xmax), y_range=(ymin, ymax), nx=300, ny=300)
    diffraction_elevation_at_faces = solver.get_free_surface_elevation(diff_result, free_surface)
    radiation_elevation_at_faces = solver.get_free_surface_elevation(rad_result, free_surface)

    # add incoming waves
    h_i = free_surface.incoming_waves(diff_result)
    h_t = (diffraction_elevation_at_faces + h_i + radiation_elevation_at_faces)
    kd = h_t/h_i
    return kd
