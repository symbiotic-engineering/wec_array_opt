import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.core.variable import Real, Integer
import modules.model_nWECs as model
import modules.distances as dis

def create_vars(limits,nWEC):
    vars = {
        "dr": Integer(bounds=(limits['dr'][0],limits['dr'][1])),
        "l": Real(bounds=(limits['L'][0],limits['L'][1])),
        "d": Real(bounds=(limits['d'][0],limits['d'][1]))
    }
    for i in range(nWEC-1):
        vars[f'x{i+1}'] = Real(bounds=(limits['x'][0],limits['x'][1]))
        vars[f'y{i+1}'] = Real(bounds=(limits['y'][0],limits['y'][1]))
        vars[f'd{i+1}'] = Real(bounds=(limits['d'][0],limits['d'][1]))
    return vars
def build_x(X,nWEC):
    x=np.zeros(nWEC*3)
    x[0] = X['dr']
    x[1] = X['l']
    x[2] = X['d']
    for i in range(nWEC-1):
        x[3+i*3] = X[f'x{i+1}']
        x[4+i*3] = X[f'y{i+1}']
        x[5+i*3] = X[f'd{i+1}']
    return x
def constraint(x,p,min_space=5):
    return min_space*x[0] - dis.min_d(x,p)
def calc_LCOE(x,p,shape=None,spacing=50):
    f = model.run(x,p,shape=shape,spacing=spacing)                              #   Run the model
    return f[0]

class LCOE_sooProblem(ElementwiseProblem):          #   Sinlge Objective Problem
    def __init__(self,p,limits,nWEC,min_space=5,shape=None,spacing=50,**kwargs):    #   P is parameters, limits is the bounds on each var type
        vars =create_vars(limits,nWEC)
        super().__init__(n_obj=1,n_ieq_constr=1,vars=vars,**kwargs)
        self.parameters = p
        self.nWEC = nWEC
        self.space = min_space
        self.shape = shape
        self.spacing = spacing
    def _evaluate(self, X, out, *args, **kwargs):
        p = self.parameters
        x = build_x(X,self.nWEC)
        f1 = calc_LCOE(x,p,self.shape,spacing=self.spacing) #   Calculate LCOE
        g1 = constraint(x,p,min_space=self.space)           #   Check constraint on minimum distance
        out["F"] = [f1]
        out["G"] = [g1]

class mooProblem(ElementwiseProblem):               #   same problem as before, except 2 objectives
    def __init__(self,p,limits,nWEC,min_space=5,shape=None,**kwargs):      #   P is parameters, limits is the bounds on each var type
        vars =create_vars(limits,nWEC)
        super().__init__(n_obj=2,n_ieq_constr=1,vars=vars,**kwargs)
        self.parameters = p
        self.nWEC = nWEC
        self.space = min_space
    def _evaluate(self, X, out, *args, **kwargs):
        p = self.parameters
        x = build_x(X,self.nWEC)
        f1 = calc_LCOE(x,p)                         #   Calculate LCOE
        f2 = dis.max_d(x,p)                         #   2nd objective is minimizing the maximum spacing between wecs
        g1 = constraint(x,p,min_space=self.space)   #   Check constraint on minimum distance
        out["F"] = [f1,f2]
        out["G"] = [g1]