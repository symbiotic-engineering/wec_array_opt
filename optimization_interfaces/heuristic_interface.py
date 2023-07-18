import numpy as np
import Model.wec_array_model as WAM
from pymoo.algorithms.moo.nsga2 import NSGA2
# x = [r_1, L_1, x_1, y_1, d_1, r_2, L_2, x_2, y_2, d_2, ..., r_n, L_n, x_n, y_n, d_n]
# p = [omega, A, beta, N]
class sooProblem(ElementwiseProblem):        #   Sinlge Objective Problem

    def __init__(self,p,limits):            #   P is parameters, limits is the bounds on each var type
        nwec = p[3]
        n_var=5*nwec
        xl = np.zeros(n_var)                #   Lower bounds
        xu = np.zeros(n_var)
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
        f1 = WAM.run(x,p)                         #   Run the model
        g1 = 3*x[0] - minimum_distance.run(x,p)     #   Check constraint on minimum distance
        out["F"] = [f1]
        out["G"] = [g1]
