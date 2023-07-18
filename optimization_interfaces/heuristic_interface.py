import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
import modules.model_nWECs as LCOE_calc
import modules.distances as dis

class sooProblem(ElementwiseProblem):        #   Sinlge Objective Problem
    def __init__(self,p,limits):            #   P is parameters, limits is the bounds on each var type
        nwec = p[3]
        n_var=3*(nwec-1) + 3
        xl = np.zeros(n_var)                #   Lower bounds
        xu = np.zeros(n_var)
        xl[0] = 0
        for i in range(nwec):
            xl[0+i*5] = limits['r'][0]
            xu[0+i*5] = limits['r'][1]
            xl[1+i*5] = limits['L'][0]
            xu[1+i*5] = limits['L'][1]
            xl[2+i*5] = limits['x'][0]
            xu[2+i*5] = limits['x'][1]
            xl[3+i*5] = limits['y'][0]
            xu[3+i*3] = limits['y'][1]
            xl[4+i*3] = limits['d'][0]
            xu[4+i*3] = limits['d'][1]
        super().__init__(n_var=n_var,
                         n_obj=1,
                         n_ieq_constr=1,
                         xl=xl,
                         xu=xu)
        self.parameters = p

    def _evaluate(self, x, out, *args, **kwargs):
        p = self.parameters
        f1 = LCOE_calc.run(x,p)                         #   Run the model
        g1 = 10*x[0] - dis.min_d.run(x,p)     #   Check constraint on minimum distance
        out["F"] = [f1]
        out["G"] = [g1]