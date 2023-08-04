import capytaine as cpt
import capytaine as capy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
# import meshmagick
# import meshmagick.mesh as mm
# from packaging import version

# import meshmagick.hydrostatics_old as hs
# from scipy.linalg import block_diag
# from capytaine.bem.airy_waves import airy_waves_potential, airy_waves_velocity, froude_krylov_force

import modules.wec_array_initialization as array_init
import modules.model_nWECs as model
omega,beta = 1.047,0
# optimal parameters and design variables
x_optimal = [6.767664116492389,0.4243817925685805,4.962817393662435,
     4383.557774446713,3262.042695725369,5.849118310687371,
     2091.3675973652084,1414.4902698961453,5.581359744648973,
     2630.7904280993725,3179.2915385711467,5.121721884659403,
     3775.6529704577347,-1196.9202158721198,5.462649133124424,
     3172.1144504953268,2199.662816700332,5.965260673173294,
     2314.2339229104405,3250.631815744075,6.381085936367207,
     1966.9174630851205,4196.5570376803325,6.635042324919791,
     717.7310259942562,3123.575922711865,5.479512515985848,
     3129.6216120449008,2870.869403460795,4.671790513634331]
wec_radius,wec_length,wecx,wecy,damp = model.unpack_x(x_optimal,10)

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
rad_result = solver.solve_all(rad_prob,keep_details=(True),n_jobs=10)
diff_prob = capy.DiffractionProblem(body=wec_array, wave_direction=beta, omega=omega)
diff_result = solver.solve(diff_prob,keep_details=(True))

ngridx = 250
ngridy = 250

free_surface = cpt.FreeSurface(x_range=(-5000, 5000), y_range=(-5000, 5000), nx=ngridx, ny=ngridy)
diffraction_elevation_at_faces = solver.get_free_surface_elevation(diff_result, free_surface)
radiation_elevation_at_faces = np.array(sum([solver.get_free_surface_elevation(rad_res, free_surface) for rad_res in rad_result])) #-1j*omega *

# radiation_elevations_per_dof = {res.radiating_dof: (-1j*omega)*solver.get_free_surface_elevation(res, fs) for res in radiation_results} 
# radiation_elevation = sum(rao.sel(omega=omega, radiating_dof=dof).data * radiation_elevations_per_dof[dof] for dof in body.dofs) 


# add incoming waves
h_i = free_surface.incoming_waves(diff_result)
h_t = (diffraction_elevation_at_faces + h_i + radiation_elevation_at_faces)



kd = h_t/h_i



# plots
x = np.linspace(-5000,5000,ngridx)
y = np.linspace(-5000,5000,ngridy)
X, Y = np.meshgrid(x, y)
Z = kd.reshape(ngridx,ngridy)
fig, ax = plt.subplots()
top = cm.get_cmap('Blues_r', 128)
bottom = cm.get_cmap('Reds', 128)
newcolors = np.vstack((top(np.linspace(0, 1, 128)),
                       bottom(np.linspace(0, 1, 128))))
cmap = ListedColormap(newcolors, name='OrangeBlue')
CS = ax.contourf(X,Y,Z,cmap=cmap,vmin=0.5,vmax=1.5)

plt.plot(wecx,wecy, linestyle = 'none', marker = 'o', color = (0/256,158/256,115/256), markersize = 10)
cbar = fig.colorbar(CS)
cbar.set_label(label='$K_{D}$',fontsize=17)
cbar.ax.tick_params(labelsize=12)
# ax.set_title('Ratio of Perturbed Free Surface to Incident Wave Elevation')
ax.set_xlabel('x [m]',fontsize=17)
ax.set_ylabel('y [m]',fontsize=17)
ax.annotate(r'$\beta$ = $\pi$/2',xy=(-100,-150),xytext=(-185,-150),fontsize=15)
plt.arrow(-175,-175,50,0,length_includes_head=True,head_width=10,head_length=10)

plt.savefig("field.pdf")
plt.show()

# plt.savefig('SSSSS.pdf')