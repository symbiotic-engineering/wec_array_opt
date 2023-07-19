import optimization_interfaces.heuristic_interface as opt
import numpy as numps
# Define Parameters
N = 3
omega = 0.5
beta = 0
A = 1
p = numps.array([omega,A,beta,N])
# p = [Wave Frequency, Wave Amplitude, density of WEC material, number of WECs]

# Limits on Design variables
limits = {'r':[2,20], 'L':[2,20], 'x':[-1000,1000], 'y':[-1000,1000], 'd':[0,7]}

X,F,H = opt.GA(p,limits)
print(X)
print(F)