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
# SAlib library for sampling and variance calculation
from SALib.analyze import sobol
from SALib.sample import saltelli
# Specify the model inputs and their bounds. The default probability
# distribution is a uniform distribution between lower and upper bounds.
# should we do sensitivity on locations? or just wave parameters.
parameter_problem = {
    "num_vars": 3, #variables or parameters
    "names": ['omega','wave_heading','wave_amplitude'], 
    "bounds": [[0.1, 3], [0, 180],[1,5]]
}

#similarly for design variable 
dv_problem = {
    "num_vars": 3, #variables or parameters
    "names": ['radius','separation_length'], 
    "bounds": [[0.5, 30], [5, 50]]
}

#array of wecx and wecy neeeded
# generate the input sample
N_samples = 1000
Y = np.empty([N_samples])

#run sampler
param_values = saltelli.sample(parameter_problem, N_samples)

#optimal locations
N = 18
r = 5
L = 2*2
basex = np.array([0,0,0,0,0,-30,-30,-30,-30]) # used to make wecx easier
wecx = np.concatenate((basex,basex + 500))
wecy = np.array([0,30,60,-30,-60,15,45,-15,-45,0,30,60,-30,-60,15,45,-15,-45])
damp = 3.6e5*np.ones(wecx.shape)
 #update this with optimal locations
x = model.pack_x(N,wecx,wecy,r,L,damp)
#run theh 'nominal' values picked by sampler 
for i, X in enumerate(param_values):
    p = [*X,N,0]
    print(p)
    Y[i] = model.run(x,p)[0] #one objective at a time


Si = sobol.analyze(parameter_problem, Y)

#first order sobol indices
total_Si, first_Si, second_Si = Si.to_df()

Si.to_df().to_csv("data/sensitivities.csv")


