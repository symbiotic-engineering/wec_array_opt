import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append("/".join((parent_folder,'src')))
import modules.model_nWECs as model
import modules.distances as dis
import numpy as np
from parameters.read_params import read_params
import optimization_interfaces.optimization_solvers as opt

p = read_params(pfile = 'src/parameters/parameters.csv')
p[7] = 3e4
nWEC = 1
limits = {'dr':[4,20], 'L':[0.1,0.2], 'x':[-500,500], 'y':[-500,500], 'd':[0,7]}
p_size = 50
gens = 20
X,F= opt.GA(p,limits,nWEC,p_size,gens,space=5,shape=None,n_proccess=4)
print(f'X: {X}')
print(f'F: {F}')