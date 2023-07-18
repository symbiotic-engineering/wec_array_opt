import numpy as np
import matplotlib.pyplot as plt
import Model.wec_array_model as WAM

# Define Array
space = 100
nx = 2
ny = 1
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

# Parameters
omega = 0.5
A = 1
beta = 0
p = [omega,A,beta]
    
d_val = np.logspace(0,7,100)
P = np.zeros(100)
for ii in range(len(d_val)):
    d = d_val[ii]*np.ones(N)
    x = WAM.pack_x(N,wecx,wecy,r,L,d)
    P[ii] = WAM.run(x,p)
plt.plot(d_val,P)
plt.show()    
