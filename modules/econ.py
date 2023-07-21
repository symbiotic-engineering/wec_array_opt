# LCOE model for heaving point absorber WEC array
# this model calculates the CAPEX by a mass scaling technique
# the OPEX is modeled as a percentage (about 5%) of the CAPEX
# O. Vitale 07/13/2023

import numpy as np

def run(N,M,P,bodies,r):
    rated_P = (r - 2)*100/8 + 900
    # inputs from model
    # P is the power out for each individual WEC
    nWEC = N                # number of WECs in array
    m_wec = M               # mass of each WEC in array [kg]
    TAEP = {body:P[body]*8760 for body in bodies}   # theoretical annual energy production [kWh] (per WEC)

    # fixed parameters
    FCR = 0.108             # fixed charge rate reported by DOE for WECs
    n_trans = 0.945         # transmission line efficiency (from OWT estimates) **conservative**
    n_avail = 0.95          # availability coefficient (from global avg estimates) **conservative**

    # mass scaling method
    m_f2hb = 5704000            # mass of wavebob WEC [kg]
    MR = {body:m_wec[body]/m_f2hb for body in bodies}   # mass ratio for scaling

    CAPEX_oesmed = 9000     # median CAPEX reported by OES for WECs [$/kW]
    CAPEX_ind = {body:(CAPEX_oesmed + (CAPEX_oesmed*MR[body]))*rated_P for body in bodies}  # scaled CAPEX [$] (individual WEC)
    # ******** ATTN NATE *********
    # so here, all the CAPEX_ind need to be summed. not sure how u wanna do that
    # but this is the spot to do that
    CAPEX = sum(CAPEX_ind.values())                 # array CAPEX [$]

    OPEX_oesmed = CAPEX_oesmed*0.05                 # OPEX represented as percentage of CAPEX [$/kW]
    OPEX_ind = {body:(OPEX_oesmed + (OPEX_oesmed*MR[body]))*rated_P for body in bodies} # scaled OPEX [$] (individual WEC)
    # ******* ATTN NATE ***********
    # same note as before for OPEX
    OPEX = sum(OPEX_ind.values())   # array OPEX [$]

    # calculating AEP
    TAEP_total = sum(TAEP.values())
    AEC = n_avail*TAEP_total        # annual energy capture [kWh]
    AEP = n_trans*AEC               # annual energy production [kWh]

    # calculating LCOE
    LCOE = ((FCR*CAPEX) + OPEX)/AEP     # levelized cost of energy [$/kWh]
    return LCOE,AEP