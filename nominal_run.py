import numpy as np
import matplotlib.pyplot as plt
import Model.wec_array_model as WAM
# Define Array
space = 100
nx = 3
ny = 3
N = nx*ny
xrange = space*(nx-1)
yrange = space*(ny-1)
xs = np.linspace(0,xrange,nx)
ys = np.linspace(0,yrange,ny)
X, Y = np.meshgrid(xs, ys)
wecx = X.flatten()
wecy = Y.flatten()
#plt.plot(wecx,wecy,linestyle = 'none',marker = 'o')
#plt.show()
r = 10*np.ones(N)
L = 10*np.ones(N)
d = 1000*np.ones(N)

# Design vector
x = WAM.pack_x(N,wecx,wecy,r,L,d)

# Parameters
omega = 0.5
A = 1
beta = 0
p = [omega,A,beta]
    
P = WAM.run(x,p)