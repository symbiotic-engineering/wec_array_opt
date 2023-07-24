import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.termination import get_termination
from pymoo.optimize import minimize

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
    
    def __init__(self,p,limits,**kwargs):
        nwec = int(p[3])
        n_var=3*(nwec-1) + 3
        xl = np.zeros(n_var)                #   bounds
        xu = np.zeros(n_var)
        xl[0] = limits['r'][0]
        xu[0] = limits['r'][1]
        xl[1] = limits['L'][0]
        xu[1] = limits['L'][1]
        xl[2] = limits['d'][0]
        xu[2] = limits['d'][1]
        for i in range(nwec-1):
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
        fs = model.run(x,p)
        f1 = fs[0]
        f2 = dis.max_d(x,p)                #   2nd objective is minimizing the maximum spacing between wecs
        g1 = 10*x[0] - dis.min_d(x,p)     #   Check constraint on minimum distance
        out["F"] = [f1,f2]
        out["G"] = [g1]

def MOCHA(p,limits,p_size,gens,n_offspring):
           #   Multi Objective Constrained Heuristic Algorithim

#    client = Client()
#    client.restart()
#    print("DASK STARTED")
#         # initialize the thread pool and create the runner
#    runner = DaskParallelization(client)

# define the problem by passing the starmap interface of the thread pool
    # initialize the thread pool and create the runner
   n_proccess = 10
   pool = multiprocessing.Pool(n_proccess)
   runner = StarmapParallelization(pool.starmap)
   problem = mooProblem(p,limits,elementwise_runner=runner)
   algorithm = NSGA2(
        pop_size=p_size,
        n_offsprings=n_offspring,
        sampling=FloatRandomSampling(),
        crossover=SBX(prob=0.9, eta=15),
        mutation=PM(eta=20),
        eliminate_duplicates=True
    )

   termination = get_termination("n_gen", gens)
   res = minimize(problem,
               algorithm,
               termination,
               seed=1,
               save_history=True,
               verbose=True)
    
   X = res.X
   F = res.F
   H = res.history
   return X,F,H
