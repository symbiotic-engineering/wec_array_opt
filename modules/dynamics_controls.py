def wec_dyn(bodies,A,B,C,F,m,omega,Amp):
    k = {body:(omega**2)*(m[body]+A[body]) - C[body] for body in bodies}    #   Calculate Optimal PTO stiffness
    for body in bodies:
        if k[body] > 1e7:                       # if k is too big
            k[body] = k[body]/abs(k[body])*1e7  #   Cap it, but let it keep it's sign
    Xi = {body:F[body]*Amp/(-(A[body]+m[body])*omega**2 + (B[body]+body.PTOdamp)*omega*1j + C[body] + k[body]) for body in bodies}
    return Xi

def time_avg_power(bodies,Xi,omega):
    P_indv = {body:(1/2)*body.PTOdamp*abs(Xi[body]*omega*1j)**2/1000 for body in bodies} # KW
    P = sum(P_indv.values())
    return P,P_indv