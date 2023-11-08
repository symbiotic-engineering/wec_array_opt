import modules.model_nWECs as model
import modules.distances as dis
import numpy as np

p = np.array([1.047,1,0,1,1])
            #  r  L d  x  y d
x = np.array([10,0.52,5])

LCOE,AEP,P = model.run(x,p)
print(f'The LCOE is {LCOE} $/kWh')
print(f'The AEP is {AEP} kWh')
print(f'The Power is {P} kW')
mind = dis.min_d(x,p)
print(f'The mind is {mind} m')