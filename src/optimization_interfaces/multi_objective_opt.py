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
   #pops[0,:] = np.array([ 2.0001, 0.10001, 5.5563025, 14.3213562, 0., 5.5563025, 7.07106781, 7.37106781, 5.5563025,  7.07106781, -7.37106781, 5.5563025 ])
   pops[0,:] = np.array([2.0001, 0.10001, 5.12, 14.3213562, 0., 5.12, 7.07106781, 7.37106781, 5.12,  7.07106781, -7.37106781, 5.12])
   pops[1,:] = np.array([9.999970313502526,0.10041574838156794,6.304674613578433,33.17864093475277,-39.45106931057746,6.410550357610941,33.437154284954964,43.06414705949915,6.377470448472719,66.19658764436237,1.2584238507427503,6.3748014264588155])
   pops[2,:] = np.array([9.987321515722519,0.10662388649473951,6.151532834804084,35.23856516368701,-35.44087061257184,6.28082801004714,35.367559968366166,36.13620134648769,6.119626152397323,71.28139056514007,-0.2693019826155214,6.47108928431184])
   pops[3,:] = np.array([7.028905698659637,0.10036489699511598,6.0140744603322025,34.83712887909791,-21.901471656596037,6.187448885908339,21.101731701366205,28.989075170225938,5.84098555086319,51.294038953101364,10.682911657141867,5.984509918099064])
   pops[4,:] = np.array([5.063285242751879,0.10022333983904058,5.730567616296603,19.318917196290382,-17.99687173008511,5.747318475762741,16.548443321232973,19.437985985264593,5.855070171258899,36.5450372453937,1.1814704072914373,5.733947219723865])
   pops[5,:] = np.array([3.9995811408551596,0.10004010713258184,5.393198874036043,18.54934326914679,-16.919058858740573,5.471369182408946,16.546588502119825,12.555340588707864,5.34042573824425,32.09458499532183,-0.12281648604136548,5.3673251824730634])
   print(pops)
   print('=======================================================================')
   problem = mooProblem(p,limits,nWEC,elementwise_runner=runner,sampling = pops)
   algorithm = NSGA2(
        pop_size=p_size,
        n_offsprings=n_offspring,
        sampling=pops,
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
