import modules.model_nWECs as model
import modules.distances as dis
import numpy as np

p = np.array([0.5,1,0,2])
            #  r  L d  x  y d
x = np.array([10,10,4,100,0,4])

LCOE = model.run(x,p)
print(f'The LCOE is {LCOE} $/kWh')
mind = dis.min_d(x,p)
print(f'The mind is {mind} m')