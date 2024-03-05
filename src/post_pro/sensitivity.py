## make a function/use nominal run function for sampler to run. 
#
# use sample to generate inputs - uniform distribution
# evaluate the model for each input sample..the model meaning nominal run function we created
# non-uniform probability distribution for the omega cause they have non-uniform , non-normal distributions?
# statistical distribution of wave parameters - omega, waveheadings  only for now

## NOTE FOR KAPIL: invetigating sensitivity of FCR (fixed charge rate), potentially
# include efficiency terms from econ mod (n_avail and n_trans)

import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.insert(0,parent_folder)

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

#similarly for design variable 
dv_problem = {
    "num_vars": 3, #variables or parameters
    "names": ['radius','separation_length'], 
    "bounds": [[0.5, 30], [5, 50]]
}

#array of wecx and wecy neeeded
# generate the input sample
N_samples = 100
Y = np.empty([16*N_samples])

#run sampler
param_values = saltelli.sample(parameter_problem, N_samples)
print(param_values)

#optimal locations
N = 4
r = 5
L = 2*2
basex = np.array([0,0,0,0,0,-30,-30,-30,-30]) # used to make wecx easier
wecx = np.concatenate((basex,basex + 500))
wecy = np.array([0,30,60,-30,-60,15,45,-15,-45,0,30,60,-30,-60,15,45,-15,-45])
damp = 3.6e5*np.ones(wecx.shape)
 #update this with optimal locations
#x = model.pack_x(wecx,wecy,r,L,damp)
x = np.array([6.299197279076497,0.10007673575582875,5.939685563058021,49.182921347145985,7.320310446259552,5.885220747485372,35.81817865532949,-21.72754886674548,5.972333841463968,19.11948545539301,25.042376603446414,5.880815678820527])
#run theh 'nominal' values picked by sampler 
for i, X in enumerate(param_values):
    p = [*X]
    print(f'{p} | set number {i}')
    Q = model.run(x,p)[0] #one objective at a time
    print('=================================')
    print(Q)
    Y[i] = Q 


Si = sobol.analyze(parameter_problem, Y,calc_second_order=True, num_resamples=100, conf_level=0.95, print_to_console=False)

#first order sobol indices
#
total_Si, first_Si, second_Si = Si.to_df()

total_Si.to_csv("../data/sensitivities/total.csv")
first_Si.to_csv("../data/sensitivities/first.csv")
second_Si.to_csv("../data/sensitivities/second.csv")

Si.plot()
plt.savefig("SI.pdf")
