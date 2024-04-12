import numpy as np
import warnings
####################################################################
#                                                                  #
#               This all comes directly from MDOcean               #
#                                                                  #
####################################################################
def get_abc_symbolic(f, m, b, k, w, r_b, r_k): 
    t2 = b**2
    t3 = k**2
    t4 = m**2
    t5 = r_b**2
    t6 = r_k**2
    t7 = w**2
    t8 = t7**2
    t9 = t3 * t5
    t12 = t2 * t6 * t7
    t13 = k * m * r_k * t5 * t7 * 2.0
    t10 = r_k * t9 * 2.0
    t11 = -t9
    t14 = r_b * t12 * 2.0
    t15 = -t12
    a_q = t11 + t15 + 1.0 / f**2 * t5 * t6 * (t3 + t2 * t7 + t4 * t8 - k * m * t7 * 2.0)
    b_q = t9 * 2.0 - t10 + t12 * 2.0 + t13 - t14
    c_q = t10 + t11 - t13 + t14 + t15 + t6 * t11 + t5 * t15 - t4 * t5 * t6 * t8 + k * m * t5 * t6 * t7 * 2.0
    return a_q, b_q, c_q

def get_relevant_soln(which_soln, roots):
    filtered_values = roots[which_soln] # filters for true index values
    result = filtered_values.sum() if np.any(which_soln) else 0 # if no true, then 0
    return result

def handle_two_solns(which_soln, roots):
    # this fcn seems to just say the second is not "ok"...
    which_soln[1] = False
    mult_1 = get_relevant_soln(which_soln, roots)
    return mult_1

def pick_which_root(roots, a_quad, b_quad, c_quad):
    # check on what solutions are "ok"
    which_soln = np.logical_and(np.logical_and(np.isreal(roots), roots > 0), roots <= 1)
    both_ok = np.sum(which_soln, axis=0) == 2   # are they both "ok"?

    if both_ok: # if they are both "ok"... why don't we check for no soln for the others?
        print('Both are ok, so just pick the first one...')
        mult = handle_two_solns(which_soln, roots)
    else:
        num_solns = np.sum(which_soln, axis=0)
        if num_solns != 1:
            which_soln = np.logical_and(roots > 0, roots <= 1.001) # why no check real
            num_solns = np.sum(which_soln)
            if num_solns != 1:
                print('****!!!')
        mult = get_relevant_soln(which_soln, roots)
    
    return mult


def get_multiplier(f_sat, m, b, k, w, r_b, r_k):
    if f_sat == 1: return 1 # if not saturated, we don't want to do anything

    # get a b and c quadratic formula variables, generated by matlab symbolic toolbox
    a_quad, b_quad, c_quad = get_abc_symbolic(f_sat, m, b, k, w, r_b, r_k)
    
    # Solve the quadratic formula
    determinant = np.sqrt(b_quad ** 2 - 4 * a_quad * c_quad)
    num1 = -b_quad + determinant
    num2 = -b_quad - determinant
    den = 2 * a_quad
    roots = np.array([num1/den, num2/den])

    # Choose which of the two roots to use
    mult = pick_which_root(roots, a_quad, b_quad, c_quad)
    assert np.all(np.isnan(mult) == False)

    return mult

####################################################################
#                                                                  #
#               This is based on MDOcean, but changed              #
#                                                                  #
####################################################################
def saturate(F_max,omega,X,A,B,C,F_app,d,k):
    F_ptos = np.sqrt((d*omega)**2 + k**2)*X     # PTO force
    r = np.array([min([F_max/abs(F_pto), 1]) for F_pto in F_ptos])   # r
    alpha = 2/np.pi * (1/r * np.arcsin(r) + np.sqrt(1 - r**2))  # alpha multiplier
    f_sat = alpha*r # not sure what this is
    mult =  np.ones(d.shape)
    for ii in range(len(f_sat)):
        mult[ii] = get_multiplier(f_sat[ii],m=A[ii,ii],b=B[ii,ii],k=C[ii,ii],w=omega,r_b=B[ii,ii]/d[ii],r_k=C[ii,ii]/k[ii])
    d_sat = d*mult
    B_sat = B - np.diag(d*(1-mult))     # reduce PTO damping by multiplier*original PTO damping
    C_sat = C - np.diag(k*(1-mult))     # reduce PTO stiffnes by multiplier*original PTO stiffness
    return B_sat,C_sat,d_sat

# this one saturates one at a time - not really needed, see saturation folder of experiments
def saturate2(F_max,omega,X,A,B,C,F_app,d,k,saturated):
    F_ptos = np.sqrt((d*omega)**2 + k**2)*X     # PTO force
    r = np.array([min([F_max/abs(F_pto), 1]) for F_pto in F_ptos])   # r
    alpha = 2/np.pi * (1/r * np.arcsin(r) + np.sqrt(1 - r**2))  # alpha multiplier
    f_sat = alpha*r # not sure what this is
    mult =  np.ones(d.shape)
    go = True
    while go:
        idx = np.argmax(abs(F_ptos))
        if saturated[idx]: F_ptos[idx] = 0
        else: 
            mult[idx] = get_multiplier(f_sat[idx],m=A[idx,idx],b=B[idx,idx],k=C[idx,idx],w=omega,r_b=B[idx,idx]/d[idx],r_k=C[idx,idx]/k[idx])
            saturated[idx] = True
            go =  False
    d_sat = d*mult
    B_sat = B - np.diag(d*(1-mult))     # reduce PTO damping by multiplier*original PTO damping
    C_sat = C - np.diag(k*(1-mult))     # reduce PTO stiffnes by multiplier*original PTO stiffness
    return B_sat,C_sat,d_sat,saturated