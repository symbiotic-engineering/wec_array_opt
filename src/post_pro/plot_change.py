import pandas as pd
import warnings
import matplotlib.pyplot as plt
import scienceplots
warnings.filterwarnings("ignore")
plt.style.use(['science','no-latex','notebook'])

import math
def alignment_score(points):
   
    min_x_point = [0,0] #first one is zero,zero

    angles = []
    for point in points:
        if point != min_x_point:
            dx = point[0] - min_x_point[0]
            dy = point[1] - min_x_point[1]
            angle = math.atan2(dy, dx)  # Calculate angle in radians
            angles.append(angle)

    angles_deg = [math.degrees(angle) % 360 for angle in angles]
    # Calculate alignment score as the std dev of angles
    alignment_score = math.sqrt(sum(angle ** 2 for angle in angles_deg) / len(angles_deg))

    return alignment_score


df = pd.read_csv("../data/paretos/combined_design_and_vars.csv",index_col=0,usecols=lambda x: x not in ['LCOE'])
df['D2'] = df['x2']**2 + df['y2']**2
df['D3'] = df['x3']**2 + df['y3']**2
df['D4'] = df['x4']**2 + df['y4']**2

df['Alignment metric'] = df.apply(lambda row: alignment_score([(row[f'x{i}'], row[f'y{i}']) for i in range(2, 5)]), axis=1)

df['L'] = df['L/r'] * df['r']


df['Mean Damping'] = df[['log_d1', 'log_d2', 'log_d3', 'log_d4']].mean(axis=1)
df = df[['r','Mean Damping','D2','D3','D4','Alignment metric']]
melted_df = df.melt(var_name='variable', value_name='value')

# # Plot using seaborn
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
plt.legend(title='Variables', loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')  
plt.savefig('post_pro/plots/changeAcrossPareto.pdf')
plt.close()

# ========only plotting both objectives change============== 
df = 0
plt.xlabel('Pareto Designs')
plt.ylabel('Normalized (with min LCOE) optimal design value')
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
plt.legend(title='Variables', loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')  
plt.savefig('post_pro/plots/changeObjective_AcrossPareto.pdf')