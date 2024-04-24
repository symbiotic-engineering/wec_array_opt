import numpy as np
import modules.force_saturation_interface as force_sat
# This module is used to calculate the motion and the power of the WEC

def system_response(F,omega,A,B,C):
    H = -(omega**2)*A + -1j*omega*B + C
    return np.linalg.solve(H,F).ravel()

def wec_dyn(bodies,A,B,C,F,m,omega,Amp,reactive,F_max=np.inf,check_condition=True):    # Calculates WEC motion based on hydro outputs
    #   bodies  ->  list of wec bodies
    #   A       ->  added mass dictionary
    #   B       ->  wave damping dictionary
    #   C       ->  hydrostatic stiffness dictionary
    #   F       ->  wave force dictionary
    #   m       ->  mass/inertia dictionary
    #   omega   ->  wave frequency
    #   Amp     ->  wave amplitude
    if reactive: k = {body:(omega**2)*(m[body]+A[body][body]) - C[body] for body in bodies} #   Calculate Optimal PTO stiffness
    else: k = {body:[[0]] for body in bodies}   #   PTO stiffness is 0 bc no reactive control
    # this section puts everything into vectors and matricies
    F_vec = np.array([F[body][0] for body in bodies])*Amp
    m_vec = np.array([m[body][0][0] for body in bodies])
    k_vec = np.array([k[body][0][0] for body in bodies])
    d_vec = np.array([body.PTOdamp for body in bodies])
    C_vec = np.array([C[body][0][0] for body in bodies])
    m_mat = np.diag(m_vec.transpose())
    k_mat = np.diag(k_vec.transpose())
    d_mat = np.diag(d_vec.transpose())
    C_mat = np.diag(C_vec.transpose())
    A_mat = np.array([[A[effected][effecting][0] for effecting in bodies] for effected in bodies])
    B_mat = np.array([[B[effected][effecting][0] for effecting in bodies] for effected in bodies])
    
    # https://www.sciencedirect.com/science/article/pii/S0889974620305995 why we picked 500
    if (np.linalg.cond(A_mat) > 500 or np.linalg.cond(B_mat) > 500) and check_condition:
        print(f'ill conditioned {np.linalg.cond(A_mat)} {np.linalg.cond(B_mat)}')
        Xi = {body:1e-5/np.linalg.cond(A_mat) for body in bodies}
        return Xi

    # calculate system inertia, resistance, and reactance
    inertia = m_mat+A_mat       # inertia is sum of mass and added mass
    resistance = B_mat+d_mat    # resistance is sum of wave induced damping and PTO damping
    reactance = C_mat+k_mat     # reactance is sum of hydrostatic stiffness and PTO stiffness (if reactive control is used)

    # calculate Xi, WEC Motion
    Xi_vec = system_response(F_vec,omega,inertia,resistance,reactance)
    
    # check force saturation
    if reactive:
        resistance_sat,reactance_sat,d_sat = force_sat.saturate(F_max,omega,Xi_vec,inertia,resistance,reactance,F_vec,d_vec,k_vec)
        Xi_vec = system_response(F_vec,omega,inertia,resistance_sat,reactance_sat)
        # update the pto damping in the body
        for ii in range(len(bodies)): bodies[ii].PTOdamp = d_sat[ii]
        
        ''' Test stuff
        test = True
        F_max = 1e5
        if test:
            saturated = np.full_like(Xi_vec, False, dtype=bool)
            for ii in range(len(saturated)):
                resistance,reactance,d_vec,saturated = force_sat.saturate2(F_max,omega,Xi_vec,inertia,resistance,reactance,F_vec,d_vec,k_vec,saturated)
                Xi_vec = system_response(F_vec,omega,inertia,resistance,reactance)
            for ii in range(len(bodies)): bodies[ii].PTOdamp = d_vec[ii]
        else:
            resistance_sat,reactance_sat,d_sat = force_sat.saturate(F_max,omega,Xi_vec,inertia,resistance,reactance,F_vec,d_vec,k_vec)
            Xi_vec = system_response(F_vec,omega,inertia,resistance_sat,reactance_sat)
            # update the pto damping in the body
            for ii in range(len(bodies)): bodies[ii].PTOdamp = d_sat[ii]'''
        
    Xi = {bodies[ii]:Xi_vec[ii] for ii in range(len(Xi_vec))}
    return Xi

def time_avg_power(bodies,Xi,omega):    # Calculates power
    #   bodies  ->  list of wec bodies
    #   Xi      ->  wec motion dictionary
    #   omega   ->  wave frequency
    P_indv = {body:(1/2)*body.PTOdamp*abs(Xi[body]*omega*1j)**2/1000 for body in bodies} # KW
    P = sum(P_indv.values())            # add up the power from each individual WEC
    return P,P_indv