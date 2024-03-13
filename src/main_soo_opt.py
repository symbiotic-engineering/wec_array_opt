import optimization_interfaces.single_objective_opt as opt
import numpy as np
import csv 
import time
nWEC = 4
# Limits on Design variables
limits = {'r':[2,10], 'L':[0.1,0.2], 'x':[-500,500], 'y':[-500,500], 'd':[0,7]}

# Define Parameters
N = 4
omega = 1.047
beta = 0
A = 1
i = 0.07                # interest rate
n_avail = 0.95          # availability coefficient (from global avg estimates) **conservative**
life_time = 25          # lifetime of WEC
array_scaling_factor = 0.65     # account for fact that OPEX does not scale linearly (very simplified)
p_shape = [1,2,3] #{1:grid, 2:line,3:random}

# Opt paramaters
p_size = 250
gens = 40 #periods
n_offspring = 50

for _ in p_shape:
	p = np.array([omega,A,beta,i,n_avail,life_time,array_scaling_factor,0,_])

	start_time = time.time()
	X,F= opt.LCOE_GA(p,limits,nWEC,p_size,gens,n_offspring)
	end_time = time.time()
	print(f'Optimization took {end_time-start_time} s')

	# save design
	with open(f'../data/experiments/interaction_{_}', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		writer.writerow([X,F])