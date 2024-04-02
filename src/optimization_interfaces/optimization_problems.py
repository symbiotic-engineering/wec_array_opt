import numpy as np
from pymoo.core.problem import ElementwiseProblem
import modules.model_nWECs as model
import modules.distances as dis

def limit_def(limits,nWEC):
    n_var=3*(nWEC-1) + 3
    xl = np.zeros(n_var)                #   lower bounds
    xu = np.zeros(n_var)                #   upper bounds
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
    return xl,xu
def constraint(x,p,min_space=5):
    return min_space*x[0] - dis.min_d(x,p)
def calc_LCOE(x,p):
    f = model.run(x,p)                              #   Run the model
    return f[0]

class LCOE_sooProblem(ElementwiseProblem):          #   Sinlge Objective Problem
    def __init__(self,p,limits,nWEC,min_space=5,**kwargs):    #   P is parameters, limits is the bounds on each var type
        xl,xu = limit_def(limits,nWEC)
        super().__init__(n_var=len(xl),
                         n_obj=1,
                         n_ieq_constr=1,
                         xl=xl,
                         xu=xu)
        self.parameters = p
        self.space = min_space
    def _evaluate(self, x, out, *args, **kwargs):
        p = self.parameters
        f1 = calc_LCOE(x,p)                         #   Calculate LCOE
        g1 = constraint(x,p,min_space=self.space)   #   Check constraint on minimum distance
        out["F"] = [f1]
        out["G"] = [g1]

class mooProblem(ElementwiseProblem):               #   same problem as before, except 2 objectives
    def __init__(self,p,limits,nWEC,min_space=5,**kwargs):      #   P is parameters, limits is the bounds on each var type
        xl,xu = limit_def(limits,nWEC)
        super().__init__(n_var=len(xl),
                         n_obj=2,
                         n_ieq_constr=1,
                         xl=xl,
                         xu=xu)
        self.parameters = p
        self.space = min_space
    def _evaluate(self, x, out, *args, **kwargs):
        p = self.parameters
        f1 = calc_LCOE(x,p)                         #   Calculate LCOE
        f2 = dis.max_d(x,p)                         #   2nd objective is minimizing the maximum spacing between wecs
        g1 = constraint(x,p,min_space=self.space)   #   Check constraint on minimum distance
        out["F"] = [f1,f2]
        out["G"] = [g1]