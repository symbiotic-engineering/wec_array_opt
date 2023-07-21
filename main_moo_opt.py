import optimization_interfaces.multi_objective_opt as opt
import numpy as np
# Define Parameters
N = 3
omega = 0.5
beta = 0
A = 1
p = np.array([omega,A,beta,N,0])
# p = [Wave Frequency, Wave Amplitude, wave direction, number of WECs, display time stamps?]

# Limits on Design variables
limits = {'r':[2,20], 'L':[2,20], 'x':[-1000,1000], 'y':[-1000,1000], 'd':[0,7]}

# Opt paramaters
p_size = 100
gens = 50
n_offspring = 50

X,F,H = opt.MOCHA(p,limits,p_size,gens,n_offspring)
print(X)
print(F)