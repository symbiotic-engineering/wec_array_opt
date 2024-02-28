import optimization_interfaces.multi_objective_opt as opt
import numpy as np
import csv
import time
# Define Parameters

if __name__ == "__main__":
    N = 4
    omega = 1.047
    beta = 0
    A = 1
    p = np.array([omega,A,beta,N,0])
    # p = [Wave Frequency, Wave Amplitude, wave direction, number of WECs, display time stamps?]

    # Limits on Design variables
    limits = {'r':[2,10], 'L':[0.1,0.2], 'x':[-500,500], 'y':[-500,500], 'd':[0,7]}

    # Opt paramaters
    p_size = 250
    gens = 100
    n_offspring = 50
    start_time = time.time()
    X,F = opt.MOCHA(p,limits,p_size,gens,n_offspring)
    end_time = time.time()
    print(f'Optimization took {end_time-start_time} s')

    # save design
    F2table = {F[i,0]:F[i,1] for i in range(len(F[:,0]))}
    Xtable = {F[i,0]:X[i,:] for i in range(len(F[:,0]))}
    F1 = np.sort(F[:,0])
    F2 = [F2table[i] for i in F1]
    print(F2)
    print(Xtable)

    X = [Xtable[i] for i in F1]
    with open(f'../data/paretos/domObjective.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for i in range(len(F)):
            writer.writerow([F1[i],F2[i]]) # LCOE, max spacing

    with open(f'../data/paretos/domDesign.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for i in range(len(X)):
            writer.writerow(X[i])
