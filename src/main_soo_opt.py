import optimization_interfaces.single_objective_opt as opt
import numpy as np
import csv 
import time

# Define Parameters
N = 4
omega = 1.047
beta = 0
A = 1
p_shape = [1,2,3]
for _ in p_shape:
	p = np.array([omega,A,beta,N,0,_]) #{1:grid, 2:line,3:random}
	# p = [Wave Frequency, Wave Amplitude, wave direction, number of WECs, display time stamps?]

	# Limits on Design variables
	limits = {'r':[2,10], 'L':[0.1,0.5], 'x':[-2500,2500], 'y':[-2500,2500], 'd':[0,7]}

	# Opt paramaters
	p_size = 500
	gens = 40 #periods
	n_offspring = 100
	start_time = time.time()
	X,F,H = opt.LCOE_GA(p,limits,p_size,gens,n_offspring)
	end_time = time.time()
	print(f'Optimization took {end_time-start_time} s')

	# save design
	with open(f'experiments_interaction_{int(p[5])}/XF_{omega}_{A}_{beta}_{N}__{p_size}_{gens}_{n_offspring}.csv', 'w', newline='') as csvfile:
	    writer = csv.writer(csvfile, delimiter=',')
	    writer.writerow([X,F])