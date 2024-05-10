import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)
grandparent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append("/".join((grandparent_folder,'sea-lab-utils')))
import matplotlib.pyplot as plt
import csv
import numpy as np
import matplotlib.colors as mcolors
from scipy.interpolate import make_interp_spline
import pyplotutilities.colors as colors
import scienceplots
plt.style.use(['science','no-latex','notebook'])

f1, f2 = [], []
with open('../data/paretos/obj.csv', newline='') as csvfile:
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

# 84 is the recommended design 
plt.scatter(f1[83],f2[83], marker='D', c=colors.red, label='Recommended Design', s=80, edgecolors='k', zorder=4)

#plt.text(utop1, utop2, 'Utopia', color='tab:green', fontsize=16)
#plt.scatter(nadi1, nadi2, marker='x', color=colors.red, label='Nadir Point', s=200, linewidth=2, zorder=3)
#plt.text(nadi1 - 0.015, nadi2 - 4, 'Nadir', color='tab:red', fontsize=16)

# Interpolate a curve between the points

plt.plot(f1, f2, color=colors.blue, label='Interpolated Front', linewidth=2, zorder=1)

plt.legend()
plt.xlabel('LCOE [$/kWh]')
plt.ylabel('Maximum Array Dimension [m]')
plt.title("")

plt.savefig('post_pro/plots/pareto2.pdf')

