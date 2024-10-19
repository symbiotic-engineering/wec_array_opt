import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
import scienceplots
plt.style.use(['science','no-latex','notebook'])
#combining optimal design with their optimal objectives for analysis and interpretation.
def pareto_dataset():
    df1 = pd.read_csv("../data/paretos/objectives_filtered.csv",names = ['LCOE','distance'],header= None)   
    df2 = pd.read_csv("../data/paretos/designs_filtered.csv",names = ['r', 'L/r', 'log_d1', 'x2', 'y2', 'log_d2','x3', 'y3', 'log_d3','x4', 'y4', 'log_d4'],header = None)

    df1.reset_index(drop=True, inplace=True)
    df2.reset_index(drop=True, inplace=True)
    df = pd.concat([df2,df1],axis = 1)
    return df


df = pareto_dataset()
df.to_csv("../data/paretos/combined_design_and_vars.csv")



df['mean_damp'] = df[['log_d1', 'log_d2', 'log_d3', 'log_d4']].mean(axis=1)
df['L'] = df['L/r'] * df['r']

#creating the variable for the 4 locations to gauge some heuristics
df['centroid_x'] = df[['x2', 'x3', 'x4']].mean(axis=1)
df['centroid_y'] = df[['y2', 'y3','y4']].mean(axis=1)

# Calculate the radius as the distance from the centroid to any point
df['radius1'] = np.sqrt((df['x2'] - df['centroid_x'])**2 + (df['y2'] - df['centroid_y'])**2)
df['radius2'] = np.sqrt((df['x3'] - df['centroid_x'])**2 + (df['y3'] - df['centroid_y'])**2)
df['radius3'] = np.sqrt((df['x3'] - df['centroid_x'])**2 + (df['y3'] - df['centroid_y'])**2)

df['radius'] = np.maximum.reduce([df['radius1'], df['radius2'], df['radius3']])


# Calculate the area of the circle inscribing the points
df['area'] = np.pi * df['radius']**2
#Minimal LCOE and average damping plot
df_final = df[['mean_damp','r','L','area','LCOE','distance']]

#do it twice for two discrete decision space in the pareto front.
cluster_after = 83 #also the recommended design.84th
#interpret relationship between two objectives.#
model1 = ols('LCOE ~ distance',data = df.iloc[:83]).fit(intercept = False) #+ np.power(distance, 2)
model2 = ols('LCOE ~ distance',data = df.iloc[84:]).fit(intercept = False)
print(model1.rsquared)
print(model2.rsquared)
print()
coefficients1 = model1.params
coefficients2 = model2.params
# latex_output = model.summary().as_latex()
# with open('post_pro/plots/regression_output.tex', 'w') as f:
#     f.write(latex_output)

regression_equation1 = f"y = {coefficients1['Intercept']:.4f}"
for i, coef in enumerate(coefficients1[1:], start=1):
    regression_equation1 += f" + ({coef:.4f}) * X_{i}"

regression_equation2 = f"y = {coefficients2['Intercept']:.4f}"
for i, coef in enumerate(coefficients2[1:], start=1):
    regression_equation2 += f" + ({coef:.4f}) * X_{i}"


# Convert the equation to LaTeX format
latex_equation1 = "$" + regression_equation1 + "$"
latex_equation2 = "$" + regression_equation2 + "$"
print(latex_equation1)
print(latex_equation2)

# Plot regression for the first subset
sns.regplot(y="LCOE", x="distance", data=df.iloc[:83], label='Cluster 1',line_kws={"color": "orange"}, scatter_kws={"color": "blue"})
plt.text(0.15, 0.8, r'$LCOE_{2} = 0.3035 - 0.0012 \times distance_{2}$', fontsize=14,  fontweight='bold',transform=plt.gca().transAxes)

# Plot regression for the second subset
sns.regplot(y="LCOE", x="distance", data=df.iloc[84:], label='Cluster 2',line_kws={"color": "green"}, scatter_kws={"color": "magenta"})
plt.text(0.2, 0.1, r'$LCOE_{1} = 0.2475 - 0.0003 \times distance_{1}$', fontsize=14,  fontweight='bold',transform=plt.gca().transAxes)
# Add equations for each line 

plt.xticks(fontsize=12, fontweight='bold') 
plt.yticks(fontsize=12, fontweight='bold')
plt.ylabel('LCOE [$/kWh]', fontweight='bold',fontsize=14)
plt.xlabel('Distance [m]', fontweight='bold',fontsize=14)
#plt.title('Models for tradeoff analysis for different decision space',fontweight='bold')
plt.legend()
plt.grid(True)
plt.savefig('post_pro/plots/regplot.pdf')


