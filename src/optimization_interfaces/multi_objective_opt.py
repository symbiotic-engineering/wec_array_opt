import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.termination import get_termination
from pymoo.termination.robust import RobustTermination
from pymoo.termination.ftol import MultiObjectiveSpaceTermination
from pymoo.optimize import minimize
from pymoo.core.evaluator import Evaluator
from pymoo.core.population import Population

# from dask.distributed import Client
# from pymoo.core.problem import DaskParallelization

import multiprocessing
from multiprocessing.pool import ThreadPool
from pymoo.core.problem import StarmapParallelization

import modules.model_nWECs as model
import modules.distances as dis

####################################################################
#                                                                  #
#           Multi Objective Problems and Solvers                   #
#                                                                  #
####################################################################

class mooProblem(ElementwiseProblem):    # same problem as before, except 2 objectives
    
    def __init__(self,p,limits,nWEC,**kwargs):
        n_var=3*(nWEC-1) + 3
        xl = np.zeros(n_var)                #   bounds
        xu = np.zeros(n_var)
        xl[0] = limits['r'][0]
        xu[0] = limits['r'][1]
        xl[1] = limits['L'][0]
        xu[1] = limits['L'][1]
        xl[2] = limits['d'][0]
        xu[2] = limits['d'][1]
        for i in range(nWEC-1):
            xl[3+i*3] = limits['x'][0]
            xu[3+i*3] = limits['x'][1]
            xl[4+i*3] = limits['y'][0]
            xu[4+i*3] = limits['y'][1]
            xl[5+i*3] = limits['d'][0]
            xu[5+i*3] = limits['d'][1]
        super().__init__(n_var=n_var,
                         n_obj=2,
                         n_ieq_constr=1,
                         xl=xl,
                         xu=xu)
        self.parameters = p

    def _evaluate(self, x, out, *args, **kwargs):
        p = self.parameters
        #print(f'x is {x}')
        fs = model.run(x,p)
        f1 = fs[0]
        f2 = dis.max_d(x,p)                #   2nd objective is minimizing the maximum spacing between wecs
        g1 = 5*x[0] - dis.min_d(x,p)     #   Check constraint on minimum distance
        out["F"] = [f1,f2]
        out["G"] = [g1]

def MOCHA(p,limits,nWEC,p_size,gens,n_offspring):
           #   Multi Objective Constrained Heuristic Algorithim

#    client = Client()
#    client.restart()
#    print("DASK STARTED")
#         # initialize the thread pool and create the runner
#    runner = DaskParallelization(client)

# define the problem by passing the starmap interface of the thread pool
    # initialize the thread pool and create the runner
   n_proccess = 24
   pool = multiprocessing.Pool(n_proccess)
   runner = StarmapParallelization(pool.starmap)
   pops = np.zeros((p_size,nWEC*3))
   limit_problem = mooProblem(p,limits,nWEC)
   for ii in range(len(limit_problem.xl)):
    pops[:,ii] = limit_problem.xl[ii] + (limit_problem.xu[ii] - limit_problem.xl[ii])*np.random.random(p_size)
   pops[0,:] =np.array([ 2.0001, 0.10001, 5.5563025, 14.3213562, 0., 5.5563025, 7.07106781, 7.37106781, 5.5563025,  7.07106781, -7.37106781, 5.5563025 ])
   print(pops)
   print('=======================================================================')
   problem = mooProblem(p,limits,nWEC,elementwise_runner=runner,sampling = pops)
   algorithm = NSGA2(
        pop_size=p_size,
        n_offsprings=n_offspring,
        sampling=FloatRandomSampling(),
        crossover=SBX(prob=0.9, eta=15),
        mutation=PM(eta=20),
        eliminate_duplicates=True
    )

   termination = RobustTermination(
                                    MultiObjectiveSpaceTermination(tol=0.005, n_skip=5), period=gens)

   
   
   #termination = get_termination("n_gen", gens)
   res = minimize(problem,
               algorithm,
               termination,
               seed=2,
               save_history=False, # might be a good idea to remove
               verbose=True)
    
   X = res.X
   F = res.F
   return X,F
