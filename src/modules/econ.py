# LCOE model for heaving point absorber WEC array
# this model calculates the CAPEX by a mass scaling technique
# the OPEX is modeled as a percentage (about 5%) of the CAPEX
# O. Vitale 02/27/2024

import numpy as np

def run(M,P,bodies):
    # is this rated P just a random value? where did we get this?
    # rated P should just be equal to P. 
    rated_P = P                     # (r - 2)*100/8 + 900 

    # parameters
    i = 0.05                # interest rate
    n_trans = 0.945         # transmission line efficiency (from OWT estimates) **conservative**
    n_avail = 0.95          # availability coefficient (from global avg estimates) **conservative**  
    L = 25                  # lifetime of WEC
    m_wec = M               # mass of each WEC in array [kg]
    m_f2hb = 5704000        # mass of wavebob WEC [kg] for scaling
    MR = {body:m_wec[body]/m_f2hb for body in bodies}   # mass ratio for scaling

    # finding annual energy production (AEP)
    TAEP = {body:P[body]*8760 for body in bodies}   # theoretical annual energy production [kWh/yr] (per WEC)
    TAEP_total = sum(TAEP.values())
    AEP = n_avail*n_trans*TAEP_total                # annual energy production [kwh/yr]

    # let's assume CAPEX is not annualized and annualize it
    CAPEX_oesmed = 9000     # median CAPEX reported by OES for WECs [$/kW] (not annualized i believe)
    CAPEX_ind = {body:(CAPEX_oesmed + (CAPEX_oesmed*MR[body]))*rated_P for body in bodies}  # scaled CAPEX [$] (individual WEC)
    CAPEX = sum(CAPEX_ind.values())                                                         # array CAPEX [$]
    ann_CAPEX = CAPEX * ((i*(1+i)**L)/((1+i)**L - 1))                          # annualized CAPEX based on interest rate [$/yr]

    # think this OPEX method is bad for arrays. the OPEX will not increase linearly
    # with number of WECs
    OPEX_oesmed = CAPEX_oesmed*0.05                 # OPEX represented as percentage of CAPEX [$/kW-yr]
    OPEX_ind = {body:(OPEX_oesmed + (OPEX_oesmed*MR[body]))*rated_P for body in bodies} # scaled OPEX [$/yr] (individual WEC)

    # ideally what i would do is for each WEC after the first WEC i multiply them each by 0.5
    # and then sum them, but this has essentially the same effect
    array_scaling_factor = 0.65     # account for fact that OPEX does not scale linearly (very simplified)
    OPEX = sum(OPEX_ind.values())*array_scaling_factor   # array OPEX [$/yr]

    # calculating LCOE
    LCOE = (ann_CAPEX + OPEX)/AEP     # levelized cost of energy [$/kWh]
    return LCOE,AEP
