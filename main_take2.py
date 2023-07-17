import wec_array_initialization as array_init
import bem_interface as bem
import dynamics as dyn
import step4_interface as step4
import numpy as np
import matplotlib.pyplot as plt
'''Please note that I changed how I index my 2d dictionaries for ease of coding in some parts.
In my first attempt I did variable[effecting body][effected body] for all my interaction terms.
Now I do variable[effected body][effecting body] because it lets me easily sum by doing
sum(variable[body].value) and it returns the total of what is effecting it instead of the total
of how it is effecting others. The variables this impacts are only "phi" and "a".'''

# Define Array
space = 100
nx = 10
ny = 10
xrange = space*(nx-1)
yrange = space*(ny-1)
xs = np.linspace(0,xrange,nx)
ys = np.linspace(0,yrange,ny)
X, Y = np.meshgrid(xs, ys)
wecx = X.flatten()
wecy = Y.flatten()
plt.plot(wecx,wecy,linestyle = 'none',marker = 'o')
plt.show()
r = 10
T = 5

# Waves
Amp = 1
omega = 0.5
beta = 0

# Array Initialization
N = len(wecx)
bodies,neighbors = array_init.run(wecx,wecy,r,T)

# Babarit Step 1: BEM stuff
ii = 1
initial_hydro = bem.initial_hydrodynamics(bodies,neighbors,omega,beta)

# Step 2: Initialize amplitude matrix
a = {body1:{body2:0 for body2 in bodies} for body1 in bodies}
for body in bodies:
    a[body][body] = Amp

# Step 3: Solve for Motion
Xi = dyn.solve(initial_hydro,a,omega,bodies)

# Step 4: Wierd PWA equations
phi = step4.calc_phi(bodies,neighbors,Xi,initial_hydro,a,omega)
a = step4.new_a_matrix(bodies,neighbors,phi,omega,a)

# Step 5: Loop
converged = False
while not converged:
    a_old = a
    Xi = dyn.solve(initial_hydro,a,omega,bodies)
    phi = step4.calc_phi(bodies,neighbors,Xi,initial_hydro,a,omega)
    a = step4.new_a_matrix(bodies,neighbors,phi,omega,a)
    a_diff =[]
    for body1 in bodies:
        for body2 in bodies:
            a_diff.append(np.abs(a[body1][body2] - a_old[body1][body2]))
    if max(a_diff) <= 0.003:
        converged = True
    
print(Xi)