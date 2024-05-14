import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
import scienceplots
warnings.filterwarnings("ignore")
plt.style.use(['science','no-latex','notebook'])

import math

df = pd.read_csv("../data/paretos/combined_design_and_vars.csv",index_col=0,usecols=lambda x: x not in ['LCOE'])
df['D2'] = df['x2']**2 + df['y2']**2
df['D3'] = df['x3']**2 + df['y3']**2
df['D4'] = df['x4']**2 + df['y4']**2

df['L'] = df['L/r'] * df['r']

print(df.head())

df['Mean Damping'] = np.exp(df[['log_d1', 'log_d2', 'log_d3', 'log_d4']].mean(axis=1))
df = df[['r','Mean Damping','D2','D3','D4']]
melted_df = df.melt(var_name='variable', value_name='value')

plt.figure(figsize=(10, 8))
grouped = melted_df.groupby('variable')
for variable, data in grouped:
    print('x')
    plt.plot(data.reset_index().index, data['value']/data['value'].iloc[0], label=variable)
    

plt.xlabel('Pareto designs')
plt.text(5, 0.1, "Min LCOE design", fontsize=9, ha='right')
plt.text(123, 0.1, "Min Distance design", fontsize=9, ha='right')

plt.ylabel('Normalized (with min LCOE) optimal design value')
plt.grid()
plt.title('Variation across the pareto front')
plt.xticks(range(10, 120, 30))
plt.legend(title='Objectives', loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')  
plt.savefig('post_pro/plots/changeAcrossPareto.pdf')
plt.close()

# ========only plotting both objectives change============== 
df = 0
plt.xlabel('Pareto Designs')
plt.ylabel('Normalized(with min LCOE) score')
plt.grid()
plt.title('Variation across the pareto front')
plt.xticks(range(10, 120, 30))
plt.legend(title='Objectives', loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')  
df = pd.read_csv("../data/paretos/combined_design_and_vars.csv",usecols=lambda x: x in ['LCOE','distance'])
print(df.columns)
melted_df = df.melt(var_name='variable', value_name='value')

grouped = melted_df.groupby('variable')

for variable, data in grouped:
    plt.plot(data.reset_index().index, data['value']/data['value'].iloc[0], label=variable)
plt.legend(title='Objectives', loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')  
plt.savefig('post_pro/plots/changeObjective_AcrossPareto.pdf')