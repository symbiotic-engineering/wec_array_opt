import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append("/".join((parent_folder,'src')))
import modules.model_nWECs as model
import numpy as np
from parameters.read_params import read_params
import optimization_interfaces.optimization_solvers as opt
from optimization_interfaces.optimization_problems import build_x

F_max = np.array([1e3,1e4,2e4,3e4,5e4,1e5,2.6e5,5e5,1e6,1e7,5e7])
p = read_params(pfile = 'src/parameters/parameters.csv')
nWEC = 1
X = []
X[0] = {'dr': 4, 'l': 0.1000000540887625, 'd': 5.899076018032584}
X[1] = {'dr': 4, 'l': 0.1000000540887625, 'd': 5.899076018032584}
X[2] = {'dr': 4, 'l': 0.10000657012190317, 'd': 5.596105657497667}
X[3] = {'dr': 5, 'l': 0.10000227419138716, 'd': 5.78730264758039}
X[4] = {'dr': 6, 'l': 0.10000963320096552, 'd': 5.868392657927661}
X[5] = {'dr': 6, 'l': 0.10000125750582964, 'd': 5.554460399293205}
X[6] = {'dr': 6, 'l': 0.10000289686420798, 'd': 5.138937648806523}
X[7] = {'dr': 6, 'l': 0.10001273315406213, 'd': 4.835135710989342}
X[8] = {'dr': 6, 'l': 0.1000023709585898, 'd': 4.548831096843891}
X[9] = {'dr': 5, 'l': 0.10000024963576025, 'd': 3.533122077314086}
X[10] = {'dr': 5, 'l': 0.10000822484108503, 'd': 3.5293994697295177}

for x,fmax in X,F_max:
    print(x)