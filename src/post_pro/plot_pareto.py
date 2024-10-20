import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0,parent_folder)

import modules.model_nWECs as model

import matplotlib.pyplot as plt
import csv
import numpy as np
import matplotlib.colors as mcolors
from scipy.interpolate import make_interp_spline
import pyplotutilities.colors as colors
import scienceplots
plt.style.use(['science','no-latex','notebook'])

f1, f2 = [], []
with open('../data/paretos/objectives_filtered.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        f1.append(float(row[0]))
        f2.append(float(row[1]))
#del(f1[-1])
#del(f2[-1])
utop1 = min(f1)
utop2 = min(f2)
nadi1 = max(f1)
nadi2 = max(f2)

plt.rcParams.update({'font.size': 15})  # Increase font size
colors.get_colors()
fig = plt.figure(1, facecolor='none')
ax = plt.axes()
plt.subplots_adjust(bottom=0.16)
ax.set_facecolor('none')
# Increase marker size and linewidth for better visibility
plt.scatter(f1, f2, marker='o', c=colors.blue, label='Pareto Front', s=75, edgecolors='k', zorder=2)
plt.scatter(utop1, utop2, marker='*', color=colors.green, label='Utopia Point', s=150, edgecolors='k', zorder=3)

#suggested point --84 index 0.2198151431189803,57.5921023195911
plt.scatter(f1[84-1],f2[84-1], marker='D', c=colors.red, label='Recommended Design', s=80, edgecolors='k', zorder=4)

#domintated designs : Reviewer question: Intutitive layout on the pareto front.
#line layout with 30m spacing
line_layout = [0.23,90]
plt.scatter(line_layout[0],line_layout[1],marker = "_",s = 75, label = "Line layout (dominated)", c=colors.red)

## Grid layout with 50m spacing -- compact distance (hyypotenuse)= 70
grid_layout = [0.2262,70]
plt.scatter(grid_layout[0],grid_layout[1],marker = "s",s = 75,label = "Grid layout (dominated)", c=colors.red)

#plt.text(utop1, utop2, 'Utopia', color='tab:green', fontsize=16)
#plt.scatter(nadi1, nadi2, marker='x', color=colors.red, label='Nadir Point', s=200, linewidth=2, zorder=3)
#plt.text(nadi1 - 0.015, nadi2 - 4, 'Nadir', color='tab:red', fontsize=16)

# Interpolate a curve between the points

plt.plot(f1, f2, color=colors.blue, label='Interpolated Front', linewidth=2, zorder=1)

plt.legend(fontsize='small',fancybox=True, frameon=True, edgecolor='black')
plt.xlabel('LCOE [$/kWh]')
plt.ylabel('Maximum Array Dimension [m]')
plt.title("")

plt.savefig('post_pro/plots/pareto.pdf')

