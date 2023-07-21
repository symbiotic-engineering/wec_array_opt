import optimization_interfaces.single_objective_opt as opt
import numpy as numps
# Define Parameters
N = 3
omega = 0.5
beta = 0
A = 1
p = numps.array([omega,A,beta,N,0])
# p = [Wave Frequency, Wave Amplitude, wave direction, number of WECs, free surface reach, grid point rates in free surface]

# Limits on Design variables
limits = {'r':[2,20], 'L':[2,20], 'x':[-1000,1000], 'y':[-1000,1000], 'd':[0,7]}

# Opt paramaters
p_size = 100
gens = 50
n_offspring = 50

X,F,H = opt.P_GA(p,limits,p_size,gens,n_offspring)
print(X)
print(F)