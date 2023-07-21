import optimization_interfaces.single_objective_opt as opt
import numpy as np
import csv 
import time
# Define Parameters
N = 1
omega = 1
beta = 0
A = 1
p = np.array([omega,A,beta,N,0])
# p = [Wave Frequency, Wave Amplitude, wave direction, number of WECs, display time stamps?]

# Limits on Design variables
limits = {'r':[2,20], 'L':[2,20], 'x':[-1000,1000], 'y':[-1000,1000], 'd':[0,7]}

# Opt paramaters
p_size = 10
gens = 5
n_offspring = 5
start_time = time.time()
X,F,H = opt.LCOE_GA(p,limits,p_size,gens,n_offspring)
end_time = time.time()
print(f'Optimization took {end_time-start_time} s')

# save design
with open(f'optimal_designs/XF_{omega}_{A}_{beta}_{N}__{p_size}_{gens}_{n_offspring}.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow([X,F])