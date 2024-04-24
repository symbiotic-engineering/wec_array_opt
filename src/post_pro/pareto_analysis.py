import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols

#combining optimal design with their optimal objectives for analysis and interpretation.
df1 = pd.read_csv("../data/paretos/FINALdomObjective.csv",names = ['LCOE','distance'],header= None)   
df2 = pd.read_csv("../data/paretos/FINALdomDesign.csv",names = ['r', 'L/r', 'log_d1', 'x2', 'y2', 'log_d2','x3', 'y3', 'log_d3','x4', 'y4', 'log_d4'],header = None)

df1.reset_index(drop=True, inplace=True)
df2.reset_index(drop=True, inplace=True)
df = pd.concat([df2,df1],axis = 1)
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


#plot design variable for designs in pareto set





#Minimal LCOE and average damping plot

df_final = df[['mean_damp','r','L','area','LCOE','distance']]
# correlation_matrix = df_final.corr().abs()
# print(correlation_matrix)
# # Create a mask for removing highly correlated features
# mask = correlation_matrix.mask(correlation_matrix <= 0.95, 1)
# print(mask.columns.tolist())
# # Drop the columns with high correlation
# df_final = df_final.drop(columns=mask.columns.tolist(), axis=1)
# print(df_final.columns)
#interpret relationship between two objectives.#
model = ols('LCOE ~ distance',data = df).fit(intercept = False) #+ np.power(distance, 2)
coefficients = model.params
print(model.summary())

latex_output = model.summary().as_latex()

with open('post_pro/plots/regression_output.tex', 'w') as f:
    f.write(latex_output)

regression_equation = f"y = {coefficients['Intercept']:.4f}"
for i, coef in enumerate(coefficients[1:], start=1):
    regression_equation += f" + ({coef:.4f}) * X_{i}"

# Convert the equation to LaTeX format
latex_equation = "$" + regression_equation + "$"

sns.regplot(x="LCOE", y="distance", data=df_final)
# plt.savefig('post_pro/plots/regplot.pdf')
sns.pairplot(df_final,kind="reg", plot_kws={'line_kws':{'color':'red'}})
plt.xlabel('X Label', fontsize=20, fontweight='bold',rotation=45)
plt.ylabel('Y Label', fontsize=20, fontweight='bold',rotation=45)
#OR add correlation plot?
plt.savefig('post_pro/plots/Interactions.pdf')

# corr_matrix = df.corr()

# mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

# f, ax = plt.subplots(figsize=(11, 9))

# cmap = sns.diverging_palette(230, 20, as_cmap=True)

# sns.heatmap(corr_matrix, mask=mask, cmap=cmap, vmax=.3, center=0,
#             square=True, linewidths=.5, cbar_kws={"shrink": .5})
#plt.savefig('post_pro/plots/regplot.pdf')