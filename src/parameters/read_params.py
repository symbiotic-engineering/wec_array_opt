import numpy as np
import csv
def read_params(pfile='parameters/parameters.csv'):
    parameters = {}
    with open(pfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            parameters[row['Parameter']] = float(row['Value'])

    # Convert the parameters to a numpy array
    p = np.array([parameters['omega'], parameters['A'], parameters['beta'], parameters['i'], parameters['n_avail'],    parameters['life_time'], parameters['array_scaling_factor'], parameters['F_max']])
    return p