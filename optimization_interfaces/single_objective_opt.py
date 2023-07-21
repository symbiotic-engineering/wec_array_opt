import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.termination import get_termination
from pymoo.optimize import minimize
import modules.model_nWECs as model
import modules.distances as dis

####################################################################
#                                                                  #
#           Single Objective Problems and Solvers                  #
#                                                                  #
####################################################################

class LCOE_sooProblem(ElementwiseProblem):       #   Sinlge Objective Problem
    def __init__(self,p,limits):            #   P is parameters, limits is the bounds on each var type
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
                         n_obj=1,
                         n_ieq_constr=1,
                         xl=xl,
                         xu=xu)
        self.parameters = p

    def _evaluate(self, x, out, *args, **kwargs):
        p = self.parameters
        fs = model.run(x,p)                         #   Run the model
        f1 = fs[0]
        g1 = 10*x[0] - dis.min_d(x,p)     #   Check constraint on minimum distance
        out["F"] = [f1]
        out["G"] = [g1]

def LCOE_GA(p,limits,p_size,gens,n_offspring):       #   GA method search algorithm
    problem = P_sooProblem(p,limits)
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

class AEP_sooProblem(ElementwiseProblem):       #   Sinlge Objective Problem
    def __init__(self,p,limits):            #   P is parameters, limits is the bounds on each var type
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
                         n_obj=1,
                         n_ieq_constr=1,
                         xl=xl,
                         xu=xu)
        self.parameters = p

    def _evaluate(self, x, out, *args, **kwargs):
        p = self.parameters
        fs = model.run(x,p)                         #   Run the model
        f1 = -fs[1]
        g1 = 10*x[0] - dis.min_d(x,p)     #   Check constraint on minimum distance
        out["F"] = [f1]
        out["G"] = [g1]

def AEP_GA(p,limits,p_size,gens,n_offspring):       #   GA method search algorithm
    problem = P_sooProblem(p,limits)
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

class P_sooProblem(ElementwiseProblem):       #   Sinlge Objective Problem
    def __init__(self,p,limits):            #   P is parameters, limits is the bounds on each var type
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
                         n_obj=1,
                         n_ieq_constr=1,
                         xl=xl,
                         xu=xu)
        self.parameters = p

    def _evaluate(self, x, out, *args, **kwargs):
        p = self.parameters
        fs = model.run(x,p)                         #   Run the model
        f1 = -fs[2]
        g1 = 10*x[0] - dis.min_d(x,p)     #   Check constraint on minimum distance
        out["F"] = [f1]
        out["G"] = [g1]

def P_GA(p,limits,p_size,gens,n_offspring):       #   GA method search algorithm
    problem = P_sooProblem(p,limits)
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