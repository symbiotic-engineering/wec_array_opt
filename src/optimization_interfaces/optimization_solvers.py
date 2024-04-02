import numpy as np
import csv
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.termination import get_termination
from pymoo.termination.robust import RobustTermination
from pymoo.termination.ftol import MultiObjectiveSpaceTermination
from pymoo.optimize import minimize
from pymoo.core.evaluator import Evaluator
from pymoo.core.population import Population

import multiprocessing
from multiprocessing.pool import ThreadPool
from pymoo.core.problem import StarmapParallelization

import optimization_interfaces.optimization_problems as opt_probs

def read_intial_pop(pop_file):
    pops = []
    with open(pop_file, 'r') as file:
        for line in file:
            row = [float(x) for x in line.strip().split(',')]
            pops.append(np.array(row))
    return pops
def create_intial_pop(p_size,problem,nWEC,pop_file):
    initial_pop = np.zeros((p_size,nWEC*3))
    for ii in range(len(problem.xl)):
        initial_pop[:,ii] = problem.xl[ii] + (problem.xu[ii] - problem.xl[ii])*np.random.random(p_size)
    selected_pop = read_intial_pop(pop_file)
    for ii in range(len(selected_pop)):
        initial_pop[ii] = selected_pop[ii]
    return initial_pop

def create_pat(opt_problem,p,limits,nWEC,p_size,gens,n_offspring,n_proccess,xo_prob,xo_eta,mutant_eta,pop_file=None):
    # builds the problem, algoritm, and termination criteria  
    pool = multiprocessing.Pool(n_proccess) 
    runner = StarmapParallelization(pool.starmap) 
    problem = opt_problem(p,limits,nWEC,elementwise_runner=runner)
    
    if pop_file==None: sampling = FloatRandomSampling()
    else: sampling = create_intial_pop(p_size,problem,nWEC,pop_file)

    algorithm = NSGA2(
        pop_size=p_size,
        n_offsprings=n_offspring,
        sampling=sampling,
        crossover=SBX(prob=xo_prob, eta=xo_eta),
        mutation=PM(eta=mutant_eta),
        eliminate_duplicates=True
    )
    termination = RobustTermination(MultiObjectiveSpaceTermination(tol=0.05, n_skip=5), period=gens)
    return problem,algorithm,termination
    
def GA(p,limits,nWEC,p_size,gens,n_offspring,n_proccess=4,xo_prob=0.9,xo_eta=15,mutant_eta=20):  
    #   Single Objective GA method search algorithm
    
    problem,algorithm,termination = create_pat(opt_probs.LCOE_sooProblem,p,limits,nWEC,p_size,gens,n_offspring,n_proccess,xo_prob,xo_eta,mutant_eta)

    res = minimize(problem,algorithm,termination,seed=2,verbose=True)
    X = res.X
    F = res.F
    return X,F

def MOCHA(p,limits,nWEC,p_size,gens,n_offspring,n_proccess=1,xo_prob=0.9,xo_eta=15,mutant_eta=20):
    # Multi Objective Constrained Heuristic Algorithim

    problem,algorithm,termination = create_pat(opt_probs.mooProblem,p,limits,nWEC,p_size,gens,n_offspring,n_proccess,xo_prob,xo_eta,mutant_eta,pop_file='optimization_interfaces/initial_pop_resistive.csv')

    res = minimize(problem,algorithm,termination,seed=2,save_history=False,verbose=True)
    X = res.X
    F = res.F
    return X,F