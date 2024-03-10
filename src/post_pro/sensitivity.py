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
    "bounds": [[0.1, 3], [-np.pi, np.pi],[0.2,3],[0.05,0.2],[0.79,0.99],[5,35],[0.5,0.99]],
    "groups": None #maybe group wave and econ separately.
}


# #array of wecx and wecy neeeded
# # generate the input sample
print(os.getcwd())

 #update this with optimal locations
csv_file_path = os.path.join( '~/wec_array_opt/data/paretos', 'domDesignNewMesh.csv')
df = pd.read_csv(csv_file_path, delimiter=',',header=None)

# setting an index such that we get a few points along the Pareto front
end = len(df.iloc[:,0])
#index_range = np.arange(0, end, int(0.1 * end), dtype=int)
index_range = np.arange(0, end, 1, dtype=int)
# for loop to calculate q-factor for Pareto optimal points
some_pareto_designs = []

for index in index_range:
    some_pareto_designs.append(df.iloc[index,:] )

#run theh 'nominal' values picked by sampler 
def run_sensitivity_sampler(optimal_dv,N_samples,write_out = False):
    param_values = saltelli.sample(parameter_problem, N_samples)
    Y = np.empty([16*N_samples])
    for i, X in enumerate(param_values):
        p = [*X]
        print(f'{p} | set number {i}')
        Y[i] = model.run(optimal_dv,p)[0] #one objective at a time
    
        Si = sobol.analyze(parameter_problem, Y,calc_second_order=True, num_resamples=100, conf_level=0.95, print_to_console=False)
        total_Si, first_Si, second_Si = Si.to_df()
        if write_out:
            total_Si.to_csv(f"../data/sensitivities/total_{i}.csv")
            first_Si.to_csv(f"../data/sensitivities/first_{i}.csv")
            second_Si.to_csv(f"../data/sensitivities/second_{i}.csv")
            print(f"wrote out the sensiitivity for design {i}..use plot_sensitivity.py to plot")
        return np.mean(Y)

#running sensitivity for one design to get idea number of samples to run.
N = [2**i for i in np.range(0,10)] #,4000,5000,10000]
#mean_Y = [run_sensitivity_sampler(some_pareto_designs[1],samples) for samples in N]

# maybe run in parallel
def run_parallel_sensitivity(N_values):
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        mean_Y = list(executor.map(lambda samples: run_sensitivity_sampler(some_pareto_designs[1], samples), N_values))
    return mean_Y

mean_Y = run_parallel_sensitivity(N)

np.savetxt("mean_Y_txt", mean_Y)