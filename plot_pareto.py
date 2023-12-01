import matplotlib.pyplot as plt



import csv
import numpy as np
import matplotlib.colors as mcolors
from scipy.interpolate import make_interp_spline



f1, f2 = [], []
with open('./paretos/domF_1.047_1_0_4__500_100_100.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        f1.append(float(row[0]))
        f2.append(float(row[1]))

utop1 = min(f1)
utop2 = min(f2)
nadi1 = max(f1)
nadi2 = max(f2)

# Create a colormap using colorblind-friendly colors
cmap = plt.get_cmap('tab20', len(f1))

plt.rcParams.update({'font.size': 16})  # Increase font size

fig = plt.figure(1, facecolor='none')
ax = plt.axes()
ax.set_facecolor('none')
# Increase marker size and linewidth for better visibility
plt.scatter(f1, f2, marker='o', c='tab:blue', label='Pareto Front', s=100, edgecolors='k', zorder=2)
plt.scatter(utop1, utop2, marker='*', color='tab:green', label='Utopia Point', s=200, edgecolors='k', zorder=3)
#plt.text(utop1, utop2, 'Utopia', color='tab:green', fontsize=16)
plt.scatter(nadi1, nadi2, marker='x', color='tab:red', label='Nadir Point', s=200, linewidth=2, zorder=3)
#plt.text(nadi1 - 0.015, nadi2 - 4, 'Nadir', color='tab:red', fontsize=16)

# Interpolate a curve between the points

plt.plot(f1, f2, color='tab:blue', label='Interpolated Curve', linewidth=2, zorder=1)

plt.legend()
plt.xlabel('LCOE [$/kWh]')
plt.ylabel('Maximum Array Dimension [m]')
plt.title("")

plt.show()

