import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
grandparent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append("/".join((grandparent_folder,'sea-lab-utils')))
import capytaine as cpt
import capytaine as capy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
#import pyplotutilities.colors as colors
from capytaine.bem.airy_waves import airy_waves_potential, airy_waves_velocity, froude_krylov_force
from capytaine.bem.airy_waves import airy_waves_free_surface_elevation
# import meshmagick
# import meshmagick.mesh as mm
# from packaging import version

# import meshmagick.hydrostatics_old as hs
# from scipy.linalg import block_diag
# from capytaine.bem.airy_waves import airy_waves_potential, airy_waves_velocity, froude_krylov_force

import modules.wec_array_initialization as array_init
import modules.model_nWECs as model
omega,beta = 1.047, 0
# optimal parameters and design variables
x_optimal = np.array([9.99992319805342,0.10000141275443655,6.29665416651116,35.2553311085241,-47.23848856922516,
                      6.3156648226237255,35.13284647724411,43.61632163749309,6.353502594175767,70.94483065027279,
                      -0.4074111725847307,6.451506386779879])
wec_radius,wec_length,wecx,wecy,damp,N = model.unpack_x(x_optimal)

# Defining original body
# all sphere

# Duplicate into an array
bodies = array_init.run(wecx,wecy,wec_radius,wec_length,damp)


wec_array = bodies[0]
for ii in range(len(bodies)-1):
	wec_array+=bodies[ii+1]
# Solve radiation problems, and diffraction problem

engine = capy.HierarchicalToeplitzMatrixEngine(ACA_distance = 20,ACA_tol = 1e-1,matrix_cache_size=2) #at least three radius
solver = capy.BEMSolver(engine = engine)
if len(bodies) > 1:
 dofs = {body:f'{body.name}__Heave' for body in bodies}
else:
 dofs = {body:'Heave' for body in bodies} 
rad_prob = [capy.RadiationProblem(body=wec_array,omega=omega,radiating_dof=dofs[body]) for body in bodies]
rad_result = solver.solve_all(rad_prob,keep_details=(True))
diff_prob = capy.DiffractionProblem(body=wec_array, wave_direction=beta, omega=omega)
diff_result = solver.solve(diff_prob,keep_details=(True))

# post-processing
# creating mesh of free surface
x_1 = -200
x_2 = 200
y_1 = -200
y_2 = 200
nx = 100
ny = 100
grid = np.meshgrid(np.linspace(x_1, x_2, nx), np.linspace(y_1, y_2, ny))
diffraction = solver.compute_free_surface_elevation(grid, diff_result)
radiation = sum(solver.compute_free_surface_elevation(grid, rad) for rad in rad_result)
incoming_fse = airy_waves_free_surface_elevation(grid, diff_result)
rad_dif = radiation + diffraction
total = radiation + diffraction + incoming_fse
kd = np.abs(total)/np.abs(incoming_fse)                              # distrubance coeff

# plots
Z = np.real(kd)
X = grid[0]
Y = grid[1]
plt.pcolormesh(X, Y, Z)
plt.xlabel("x")
plt.ylabel("y")
colorbar = plt.colorbar()
colorbar.set_label('Total Wave Field')
plt.scatter(wecx,wecy, marker = 'o', color = 'black', s = 100)  # Add markers
plt.arrow(-125, 100, 20, 0, color='black', width=0.2, head_width=5, head_length=5)
plt.text(-100, 85, 'Incident Waves', color='black', fontsize=12, ha='center', va='center')
plt.tight_layout()
plt.savefig('field.pdf')
plt.show()