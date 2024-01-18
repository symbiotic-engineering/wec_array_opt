import numpy as np
# This module is used to calculate the motion and the power of the WEC

def wec_dyn(bodies,A,B,C,F,m,omega,Amp):    # Calculates WEC motion based on hydro outputs
    k = {body:(omega**2)*(m[body]+A[body][body]) - C[body] for body in bodies}    #   Calculate Optimal PTO stiffness
    for body in bodies:
        if k[body] > 1e7:                       # if k is too big
            k[body] = k[body]/abs(k[body])*1e7  #   Cap it, but let it keep it's sign
    #k = {body:0 for body in bodies}
    #Xi = {body:F[body]*Amp/(-(A[body]+m[body])*omega**2 - (B[body]+body.PTOdamp)*omega*1j + C[body] + k[body]) for body in bodies}
    
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
    
    # calculate Xi, WEC Motion, and the package result as a dictionary
    Xi_vec = np.matmul(np.linalg.inv(-(omega**2)*(A_mat+m_mat) - 1j*omega*(B_mat+d_mat) + k_mat + C_mat),F_vec)
    Xi = {bodies[ii]:Xi_vec[ii] for ii in range(len(Xi_vec))}
    return Xi

def time_avg_power(bodies,Xi,omega):    # Calculates power
    P_indv = {body:(1/2)*body.PTOdamp*abs(Xi[body]*omega*1j)**2/1000 for body in bodies} # KW
    P = sum(P_indv.values())            # add up the power from each individual WEC
    return P,P_indv