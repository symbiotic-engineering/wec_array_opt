import numpy as np
# This module is used to calculate the motion and the power of the WEC

def wec_dyn(bodies,A,B,C,F,m,omega,Amp,reactive,check_condition):    # Calculates WEC motion based on hydro outputs
    #   bodies  ->  list of wec bodies
    #   A       ->  added mass dictionary
    #   B       ->  wave damping dictionary
    #   C       ->  hydrostatic stiffness dictionary
    #   F       ->  wave force dictionary
    #   m       ->  mass/inertia dictionary
    #   omega   ->  wave frequency
    #   Amp     ->  wave amplitude
    if reactive
        k = {body:(omega**2)*(m[body]+A[body][body]) - C[body] for body in bodies}    #   Calculate Optimal PTO stiffness
    else
        k = {body:0 for body in bodies}    #   PTO stiffness is 0 bc no reactive control
    # this section puts everything into vectors and matricies
    F_vec = np.array([F[body][0] for body in bodies])
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

    # calculate Xi, WEC Motion, and the package result as a dictionary
    H = -(omega**2)*(A_mat+m_mat) - 1j*omega*(B_mat+d_mat) + k_mat + C_mat
    #solve it for Xi
    Xi_vec = np.linalg.solve(H,F_vec)*Amp
    Xi = {bodies[ii]:Xi_vec[ii] for ii in range(len(Xi_vec))}
    return Xi

def time_avg_power(bodies,Xi,omega):    # Calculates power
    #   bodies  ->  list of wec bodies
    #   Xi      ->  wec motion dictionary
    #   omega   ->  wave frequency
    P_indv = {body:(1/2)*body.PTOdamp*abs(Xi[body]*omega*1j)**2/1000 for body in bodies} # KW
    P = sum(P_indv.values())            # add up the power from each individual WEC
    return P,P_indv