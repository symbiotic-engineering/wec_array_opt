import optimization_interfaces.optimization_solvers as opt
import numpy as np
import csv
import time
from parameters.read_params import read_params
from optimization_interfaces.optimization_problems import build_x
# Define Parameters

if __name__ == "__main__":
    N = 4
    p = read_params()
    # p = [Wave Frequency, Wave Amplitude, wave direction, interest, availability, lifetime, array scaling factor,F_max]

    # Limits on Design variables
    limits = {'dr':[4,20], 'L':[0.1,0.2], 'x':[-500,500], 'y':[-500,500], 'd':[0,7]}

    # Opt paramaters
    nWEC = 4
    p_size = 120
    gens = 100
    start_time = time.time()

    X,F = opt.MOCHA(p,limits,nWEC,p_size,gens,space=5,n_proccess=20)
    end_time = time.time()
    print(f'Optimization took {end_time-start_time} s')

    # save design
    F2table = {F[i,0]:F[i,1] for i in range(len(F[:,0]))}
    Xtable = {F[i,0]:build_x(X[i],nWEC) for i in range(len(F[:,0]))}
    F1 = np.sort(F[:,0])
    F2 = [F2table[i] for i in F1]
    #print(F2)
    #print(Xtable)

    X = [Xtable[i] for i in F1]
    with open(f'../data/paretos/obj.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for i in range(len(F)):
            writer.writerow([F1[i],F2[i]]) # LCOE, max spacing

    with open(f'../data/paretos/des.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for i in range(len(X)):
            writer.writerow(X[i])
