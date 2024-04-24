import sys, os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.insert(0,parent_folder)
import matplotlib.pyplot as plt
import pandas as pd
import capytaine as capy
from plotnine import ggplot, aes, facet_wrap, labs, geom_line,scale_color_discrete
import plotnine as pn

df = pd.read_csv('../data/mesh_convergence/convergence.csv')
grouped = df.groupby('design').ngroup()
df['design_id'] = 'design' + grouped.astype(str)
df['moving_average'] = df['A'].rolling(window=4, min_periods=4).mean()
plt.figure(figsize=(14,10))
x = ( ggplot(df)
    + facet_wrap(facets="design_id",scales='free')
    + aes(x="panels", y="A")
    #+ geom_line(show_legend=True)+ pn.theme(panel_background=pn.element_blank()) 
    + aes(y='moving_average') +  geom_line(color='red', linetype='dashed')
 + pn.theme()
  + labs(
        x="panels",
        y="A(w)",
        title="",
    )
 + pn.theme(axis_ticks_major_y=pn.element_blank())
 + pn.theme(figure_size=(12, 8))
             ).draw()
x.savefig("post_pro/plots/mesh_convergence.pdf")