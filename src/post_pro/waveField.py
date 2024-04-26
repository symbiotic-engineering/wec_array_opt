def waveField(x_optimal):
    import sys
    import os
    parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.append(parent_folder)
    grandparent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    sys.path.append("/".join((grandparent_folder,'sea-lab-utils')))
    import capytaine as capy
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from matplotlib.colors import ListedColormap, LinearSegmentedColormap
    from capytaine.bem.airy_waves import airy_waves_potential, airy_waves_velocity, froude_krylov_force
    from capytaine.bem.airy_waves import airy_waves_free_surface_elevation
    import pyplotutilities.colors as colors
    import modules.wec_array_initialization as array_init
    import modules.model_nWECs as model
    from parameters.read_params import read_params
    import modules.hydro_terms as hydro
    from modules.dynamics_controls import wec_dyn 

    p = read_params()
    wec_radius,wec_length,wecx,wecy,damp,N = model.unpack_x(x_optimal)
    bodies = array_init.run(wecx,wecy,wec_radius,wec_length,damp) # use design vector
    A,B,C,F,M,rad_result,diff_result = hydro.run(bodies,beta=p[2],omega=p[0],time_data=False,wave_field=True)
    Xi = wec_dyn(bodies,A,B,C,F,M,omega=p[0],Amp=1,reactive=True,F_max=p[7])   # WEC motion
    
    engine = capy.HierarchicalToeplitzMatrixEngine(ACA_distance = 7*bodies[0].radius,ACA_tol = 1e-2,matrix_cache_size=2)
    solver = capy.BEMSolver(engine = engine)

    # post-processing
    # creating mesh of free surface
    x_1 = -100
    x_2 = 100
    y_1 = -100
    y_2 = 100
    nx = 100
    ny = 100
    grid = np.meshgrid(np.linspace(x_1, x_2, nx), np.linspace(y_1, y_2, ny))
    diffraction = solver.compute_free_surface_elevation(grid, diff_result)

    multiplications = []
    for i in range(len(bodies)):
        mult_result = solver.compute_free_surface_elevation(grid, rad_result[i]) * Xi[bodies[i]]
        multiplications.append(mult_result)
    radiation = sum(multiplications)

    # radiation = sum(solver.compute_free_surface_elevation(grid, rad) for rad in rad_result)
    incoming_fse = airy_waves_free_surface_elevation(grid, diff_result)
    total = radiation + diffraction + incoming_fse
    kd = np.abs(total)/np.abs(incoming_fse)                              # distrubance coeff

    # plots
    Z = np.real(total)
    X = grid[0]
    Y = grid[1]
    colors.get_colors()
    plt.pcolormesh(X, Y, Z) #, cmap=cmap,vmin=0,vmax=2.5)
    plt.xlabel("x")
    plt.ylabel("y")
    colorbar = plt.colorbar()
    colorbar.set_label(r"Total Wave Elevation, $\xi$")
    plt.scatter(wecx,wecy, marker = 'o', color = 'black', s = 100)  # Add markers
    plt.arrow(-50, 50, 20, 0, color='black', width=0.2, head_width=5, head_length=5)
    plt.text(-60, 40, 'Incident Waves', color='black', fontsize=12, ha='center', va='center')
    plt.tight_layout()
    plt.show()

    Zk = np.real(kd)
    colors.get_colors()
    plt.pcolormesh(X, Y, Zk) #, cmap=cmap,vmin=0,vmax=2.5)
    plt.xlabel("x")
    plt.ylabel("y")
    colorbar = plt.colorbar()
    colorbar.set_label(r'Disturbace Coefficient, $k_d$')
    plt.scatter(wecx,wecy, marker = 'o', color = 'black', s = 100)  # Add markers
    plt.arrow(-50, 50, 20, 0, color='black', width=0.2, head_width=5, head_length=5)
    plt.text(-60, 40, 'Incident Waves', color='black', fontsize=12, ha='center', va='center')
    plt.tight_layout()
    plt.show()
    #plt.savefig('post_pro/plots/field.pdf')
    return

import numpy as np
# optimal parameters and design variables
x_optimal = np.array([9.99992319805342,0.10000141275443655,6.29665416651116,35.2553311085241,
                    -47.23848856922516,6.3156648226237255,35.13284647724411,43.61632163749309,6.353502594175767,
                    70.94483065027279,-0.4074111725847307,6.451506386779879])
waveField(x_optimal)
