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
    y_1 = -70
    y_2 = 130
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
    cmap = LinearSegmentedColormap.from_list('CustomMap', [colors.blue, colors.green, colors.yellow])
    plt.pcolormesh(X, Y, Z,cmap=cmap) #, cmap=cmap,vmin=0,vmax=2.5)
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
    plt.pcolormesh(X, Y, Zk,cmap=cmap) #, cmap=cmap,vmin=0,vmax=2.5)
    plt.xlabel("x")
    plt.ylabel("y")
    colorbar = plt.colorbar()
    colorbar.set_label(r'Disturbace Coefficient, $k_d$')
    plt.scatter(wecx,wecy, marker = 'o', color = 'black', s = 100)  # Add markers
    plt.arrow(-50, 50, 20, 0, color='black', width=0.2, head_width=5, head_length=5)
    plt.text(-60, 40, 'Incident Waves', color='black', fontsize=12, ha='center', va='center')
    plt.tight_layout()
    plt.savefig('post_pro/plots/kd_minLCOE.pdf')
    plt.show()
    return

import numpy as np
# optimal parameters and design variables
x_optimal = np.array([8.0,0.10000342644859998,5.547542754651831,24.266210287828336,64.50412981468327,5.5488186147585585,47.37176881575031,-0.5568212532930796,5.560543492258006,-22.87242901300752,65.98209563108522,5.5581438747010585])
waveField(x_optimal)
