import sys, os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.insert(0,parent_folder)
import matplotlib.pyplot as plt
import pandas as pd



# ## plotting the sensitivity convergence with samples
# df = pd.read_csv("~/wec_array_opt/data/sensitivities/omega_convergence.csv")
# df = df.rename(columns={'Unnamed: 0': 'parameter'})
# df = df[df.parameter == 'omega']
# print(df.head())
# fig, ax = plt.subplots()

# # Color map for coloring the lines by parameter
# color_map = plt.cm.get_cmap('tab10', len(df['parameter'].unique()))

# for i, (param, group) in enumerate(df.groupby('parameter')):
#     ax.plot(group['samples'], group['ST'], label=param, color=color_map(i))

# # Add labels and legend
# ax.set_xlabel('Samples')
# ax.set_ylabel('ST')
# ax.legend(title='Parameter')

# plt.title('Convergence of total sensitivity for omega')

# plt.show()

# plt.savefig("plots/sobol_convergence.pdf")


path_total_Si = "../data/sensitivities/total_sens_calcs.csv"
path_first_Si = "../data/sensitivities/first_sens_calcs.csv"
path_second_Si = "../data/sensitivities/second_sens_cals.csv" 

#for total
total_Si = pd.read_csv(path_total_Si)
plt.figure(figsize=(8, 6))
plt.errorbar(total_Si['Unnamed: 0'], total_Si['ST'], yerr=total_Si['ST_conf'], fmt='o', color='blue', capsize=5)
#plt.yscale('log')
plt.title('Scatter Plot of total sensitivity with Confidence Bars')
plt.xlabel('parameters')
plt.ylabel('ST')
plt.xticks(rotation=45, ha='right') 
plt.grid(True)
plt.tight_layout() 
plt.show()
plt.savefig("post_pro/plots/SI_total.pdf")
plt.close('all')

#similarly for first order 
first_Si = pd.read_csv(path_first_Si)
plt.figure(figsize=(8, 6))

#plt.errorbar(first_Si['Unnamed: 0'], first_Si['S1'], yerr=first_Si['S1_conf'], fmt='o', color='blue')

plt.title('Scatter Plot of first order sensitivity with Confidence Bars')
#plt.yscale('log')
plt.xlabel('parameters')
plt.ylabel('ST')
plt.xticks(rotation=45, ha='right') 
plt.grid(True)
plt.tight_layout() 
plt.show()
plt.savefig("post_pro/plots/SI_first.pdf")
plt.close('all')


#similarly for second order interactin 
second_Si = pd.read_csv(path_second_Si)
plt.figure(figsize=(8, 6))
second_Si_sorted = second_Si.sort_values(by='S2', ascending=False)
plt.bar(second_Si_sorted['Unnamed: 0'], second_Si_sorted['S2'], color='blue')
#plt.errorbar(second_Si['Unnamed: 0'], second_Si['S2'], fmt='o', color='blue', capsize=5)
plt.title('Scatter Plot of second order sensitivity')
plt.xlabel('parameters')
#plt.yscale('log')
plt.ylabel('ST')
plt.xticks(rotation=45, ha='right') 
plt.grid(True)
plt.tight_layout() 
plt.show()
plt.savefig("post_pro/plots/SI_second.pdf")
plt.close('all')

