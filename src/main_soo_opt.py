import optimization_interfaces.optimization_solvers as opt
import numpy as np
import csv 
import time
from parameters.read_params import read_params
from optimization_interfaces.optimization_problems import build_x

if __name__ == "__main__":
	nWEC = 4
	# Limits on Design variables
	limits = {'dr':[4,20], 'L':[0.1,0.2], 'x':[-500,500], 'y':[-500,500], 'd':[0,7]}

	# Define Parameters
	N = 4
	p_shape = [1,2,3] #{1:grid, 2:line,3:random}

	# Opt paramaters
	p_size = 120
	gens = 40 #periods
	n_offspring = 50
	p = read_params()

	for _ in p_shape:
		start_time = time.time()
		X,F= opt.GA(p,limits,nWEC,p_size,gens,space=5,shape=_,n_proccess=20)
		end_time = time.time()
		print(f'Optimization took {end_time-start_time} s')

		# save design
		with open(f'../data/experiments/interaction_{_}_reactive', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			writer.writerow([build_x(X,N),F])
