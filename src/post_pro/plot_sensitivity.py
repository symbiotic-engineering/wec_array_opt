import sys, os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.insert(0,parent_folder)
import matplotlib.pyplot as plt
import pandas as pd
import scienceplots
plt.style.use(['science','no-latex','notebook'])



## plotting the sensitivity convergence with samples
df1 = pd.read_csv("~/wec_array_opt/data/sensitivities/sobol_convergence_data.csv")
df1 = df1.rename(columns={'Unnamed: 0': 'parameter'})

df2 = pd.read_csv("~/wec_array_opt/data/sensitivities/sobol_convergence_data_more.csv")
df2 = df2.rename(columns={'Unnamed: 0': 'parameter'})

df = pd.concat([df1,df2],axis = 0)
fig, ax = plt.subplots()

# Color map for coloring the lines by parameter
color_map = plt.cm.get_cmap('tab10', len(df['parameter'].unique()))

for i, (param, group) in enumerate(df.groupby('parameter')):
    ax.plot(group['samples'], group['ST'], label=param, color=color_map(i))

ax.set_yscale('log')
# Add labels and legend
ax.set_xlabel('Samples')
ax.set_ylabel('ST')
ax.legend(title='Parameters',loc='lower left',fontsize='small')

plt.title('Convergence of total sensitivity index of parameters')

plt.show()

plt.savefig("post_pro/plots/sobol_convergence.pdf")

path_total_Si = "../data/sensitivities/total.csv"
path_first_Si = "../data/sensitivities/first.csv"
path_second_Si = "../data/sensitivities/second.csv" 

#for total
total_Si = pd.read_csv(path_total_Si)
total_Si = total_Si.sort_values(by='ST', ascending=True)
plt.figure(figsize=(8, 6))
plt.barh(total_Si['Unnamed: 0'], total_Si['ST'],height = 0.05,alpha = 0.5)
plt.scatter(total_Si['ST'], total_Si['Unnamed: 0'], color='blue', zorder=5,s = 150)
plt.xscale('log')
plt.title('Total sensitivity of parameters to minimized LCOE')
plt.ylabel('parameters')
plt.xlabel('Total Sensitivity Index', fontsize=14)
plt.xticks(rotation=45, ha='right') 
plt.grid(True)
plt.tight_layout() 
plt.savefig("post_pro/plots/SI_total.pdf")
plt.close('all')
