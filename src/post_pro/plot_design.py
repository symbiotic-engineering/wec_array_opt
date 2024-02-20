import matplotlib.pyplot as plt
import modules.model_nWECs as model
import numpy as np

# Design to plot
N = 4
x = [2.0016200525777434,0.10000249298379714,2.867765962701866,-8.958046230230694,-5.754094162055907,3.2342380447161108,-8.67560571496843,9.809968695344995,3.3069956247436254,-15.558692996975106,1.8526743275462612,2.57270056436542]
# get x and y
r, L, x, y, d  = model.unpack_x(x,N)
print(d)
wecX, wecY = np.meshgrid(np.linspace(0,50,2),np.linspace(0,50,2))
x = wecX.flatten()
y = wecY.flatten()
r = 9.86
r = 2.2

x = np.zeros(4)
y = np.linspace(0,200,4)
r = 2.2
r = 9.86

#x = np.array([0,30,10,-30])
#y = np.array([0,30,-40,20])
#r = 4.958

# plot
plt.rcParams.update({'font.size': 12})  # Increase font size
fig,ax = plt.subplots(1,figsize=(7,7))
ax.plot(x,y, linestyle = 'none', marker = 'o', color = 'r', markersize = 6*r)
for ii in range(len(x)):
    ax.text(x[ii],y[ii],f'{ii+1}',horizontalalignment = 'center', verticalalignment = 'center',color = 'w')
ax.set_xlabel('X location [m]')
ax.set_ylabel('Y location [m]')
ax.set_xlim([-125,175])
ax.set_ylim([-75,225])
#ax.axis('equal')
#plt.show()
plt.savefig('experiments_interaction_2/line_layout.png')
