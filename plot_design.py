import matplotlib.pyplot as plt
import modules.model_nWECs as model

# Design to plot
N = 1
x = [ 10,10,4 ]

# get x and y
r, L, x, y, d  = model.unpack_x(x,N)

# plot
plt.plot(x,y, linestyle = 'none', marker = 'o', color = 'm', markersize = 20)
plt.show()