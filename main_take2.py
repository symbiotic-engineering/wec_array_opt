import wec_array_initialization as array_init
import bem_interface as bem

# Define Array
wecx = [0,100]
wecy = [0,0]
r = 10

# Waves
Amp = 1
omega = 1
beta = 0


# Array Initialization
N = len(wecx)
bodies,neighbors = array_init.run(wecx,wecy,r)

# Babarit Step 1: BEM stuff
ii = 1
initial_hydro = bem.initial_hydrodynamics(bodies,omega,omega)
for body in bodies:
    #print(f"Rad Source: {initial_hydro[body]['sigma_r']}")
    #print(f"Diff Source: {initial_hydro[body]['sigma_d']}")
    print(f"Force: {initial_hydro[body]['F']}")
    
