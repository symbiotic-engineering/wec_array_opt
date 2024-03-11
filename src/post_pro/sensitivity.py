## make a function/use nominal run function for sampler to run. 
#
# use sample to generate inputs - uniform distribution
# evaluate the model for each input sample..the model meaning nominal run function we created
# non-uniform probability distribution for the omega cause they have non-uniform , non-normal distributions?
# statistical distribution of wave parameters - omega, waveheadings  only for now

## NOTE FOR KAPIL: invetigating sensitivity of FCR (fixed charge rate), potentially
# include efficiency terms from econ mod (n_avail and n_trans)

import sys
import pandas as pd
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.insert(0,parent_folder)
import concurrent.futures
import modules.model_nWECs as model
import modules.distances as dis
import numpy as np
import matplotlib.pyplot as plt
# SAlib library for sampling and variance calculation
from SALib.analyze import sobol
from SALib.sample import saltelli
# Specify the model inputs and their bounds. The default probability
# distribution is a uniform distribution between lower and upper bounds.
# should we do sensitivity on locations? or just wave parameters.
parameter_problem = {
    "num_vars": 7, #variables or parameters
    "names": ['omega','wave_heading','wave_amplitude','interest','n_avail','L','array_scaling_factor'], 
    "bounds": [[0.1, 3.1], [-np.pi, np.pi],[0.2,3],[0.05,0.2],[0.79,0.99],[5,35],[0.5,0.99]],
    "groups": None #maybe group wave and econ separately.
}


# #array of wecx and wecy neeeded
# # generate the input sample
print(os.getcwd())

 #update this with optimal locations
csv_file_path = os.path.join( '~/wec_array_opt/data/paretos', 'FINALdomDesign.csv')
df = pd.read_csv(csv_file_path, delimiter=',',header=None)
print(df)
#index_range = np.arange(0, end, int(0.1 * end), dtype=int)
index_range = [15,203,232,241,248]
#np.arange(0, df.shape[0], 20, dtype=int)
# for loop to calculate q-factor for Pareto optimal points
some_pareto_designs = []

for index in index_range:
    some_pareto_designs.append(df.iloc[index,:] )
print("sampled pareto design equidistant")
print(len(some_pareto_designs))
#run theh 'nominal' values picked by sampler 
def run_sensitivity_sampler(optimal_dv,N_samples,write_out = False):
    param_values = saltelli.sample(parameter_problem, N_samples)
    print(param_values.shape)
    Y = np.empty([16*N_samples]) #for each combination.
    for i, X in enumerate(param_values):
        p = [*X]
        Y[i] = model.run(optimal_dv,p,check_condition=False)[0] #one objective at a time
    
    Si = sobol.analyze(parameter_problem, Y,calc_second_order=True, num_resamples=10, conf_level=0.95, print_to_console=False)
    
    total_Si,first_Si,second_Si = Si.to_df()
   
    if write_out:
        total_Si.to_csv(f"~/wec_array_opt/data/sensitivities/{optimal_dv}_total.csv")
        first_Si.to_csv(f"~/wec_array_opt/data/sensitivities/{optimal_dv}_first.csv")
        second_Si.to_csv(f"~/wec_array_opt/data/sensitivities/{optimal_dv}_second.csv")
        print(f"wrote out the sensiitivity for design {i}..use plot_sensitivity.py to plot")
    return total_Si
#========================SOBOL SENSITIVITY===================
#running sensitivity for one design to get idea number of samples to run.
#N = [2**i for i in np.arange(2,8)] #,4000,5000,10000]
#mean_Y = [run_sensitivity_sampler(some_pareto_designs[1],samples) for samples in N]
#print(N)
# maybe run in parallel..also for sensitivity convergence.
def run_parallel_convergence_sensitivity(N_values):
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        # Use list comprehension to run run_sensitivity_sampler for each N value in parallel
        total_SI = list(executor.map(lambda samples: run_sensitivity_sampler(some_pareto_designs[1], samples), N_values))
        
  #  total_SI = [run_sensitivity_sampler(some_pareto_designs[1], samples,write_out=False) for samples in N_values]
        for i, df in enumerate(total_SI):
            df['samples'] = [N_values[i]] * len(df)
        total_df = pd.concat(total_SI)
    return total_df
#run_sensitivity_sampler(some_pareto_designs[0],2,write_out = True)
#after sobol convergence, N = 1000 is picked --
#====================SENSITIVITY STUDY ======================
for pareto_design in some_pareto_designs:
    total_df = run_sensitivity_sampler(pareto_design, 1024,write_out = True)
    total_df.to_csv(f"~/wec_array_opt/data/sensitivities/{pareto_design}_total_SI_convergece.csv")