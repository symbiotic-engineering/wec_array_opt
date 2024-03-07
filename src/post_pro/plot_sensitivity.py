import sys, os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.insert(0,parent_folder)
import matplotlib.pyplot as plt
import pandas as pd
path_total_Si = "../data/sensitivities/total.csv"
path_first_Si = "../data/sensitivities/first.csv"
path_second_Si = "../data/sensitivities/second.csv"

#for total
total_Si = pd.read_csv(path_total_Si)
plt.figure(figsize=(8, 6))
plt.errorbar(total_Si['Unnamed: 0'], total_Si['ST'], yerr=total_Si['ST_conf'], fmt='o', color='blue', capsize=5)
plt.title('Scatter Plot of total sensitivity with Confidence Bars')
plt.xlabel('parameters')
plt.ylabel('ST')
plt.xticks(rotation=45, ha='right') 
plt.grid(True)
plt.tight_layout() 
plt.show()
plt.savefig("SI_total.pdf")
plt.close('all')

#similarly for first order 
first_Si = pd.read_csv(path_first_Si)
plt.figure(figsize=(8, 6))
plt.errorbar(first_Si['Unnamed: 0'], first_Si['S1'], yerr=first_Si['S1_conf'], fmt='o', color='blue', capsize=5)
plt.title('Scatter Plot of first order sensitivity with Confidence Bars')
plt.xlabel('parameters')
plt.ylabel('ST')
plt.xticks(rotation=45, ha='right') 
plt.grid(True)
plt.tight_layout() 
plt.show()
plt.savefig("SI_first.pdf")
plt.close('all')


#similarly for second order interactin 
second_Si = pd.read_csv(path_second_Si)
plt.figure(figsize=(8, 6))
plt.errorbar(second_Si['Unnamed: 0'], second_Si['S2'], yerr=second_Si['S2_conf'], fmt='o', color='blue', capsize=5)
plt.title('Scatter Plot of second order sensitivity with Confidence Bars')
plt.xlabel('parameters')
plt.ylabel('ST')
plt.xticks(rotation=45, ha='right') 
plt.grid(True)
plt.tight_layout() 
plt.show()
plt.savefig("SI_second.pdf")
plt.close('all')