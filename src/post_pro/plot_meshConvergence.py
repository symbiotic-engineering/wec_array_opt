import sys, os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.insert(0,parent_folder)
import matplotlib.pyplot as plt
import scienceplots
plt.style.use(['science','no-latex','notebook'])
import pandas as pd
import capytaine as capy
from plotnine import ggplot, aes, facet_wrap, labs, geom_line,scale_color_discrete
import plotnine as pn

df = pd.read_csv('../data/mesh_convergence/convergence.csv')
grouped = df.groupby('design').ngroups

fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(18, 12))
# Plot lines on each subplot
for i, (design_id, group) in enumerate(df.groupby('design')):
    #group['moving_average'] = df['A'].rolling(window=10, min_periods=8).mean()
    group = group.sort_values(by='panels')
    row = i // 3 
    col = i % 3   
    ax = axs[row, col] 
    ax.plot(group['panels'], group['A'], label='A',color = 'black')
    #ax.plot(group['panels'], group['moving_average'], color='red', linestyle='dashed', label='Moving Average')
    ax.set_title(f'Design{i}')
    ax.set_xlabel('panels')
    ax.set_ylabel('A(w)')
    ax.set_yscale('log')
plt.legend()
plt.tight_layout()
plt.savefig("post_pro/plots/mesh_convergence.pdf")
    