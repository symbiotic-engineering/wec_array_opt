def run(bodies,Xi,omega):
    P_indv = {body:(1/2)*body.PTOdamp*abs(Xi[body]*omega*1j)**2/1000 for body in bodies} # KW
    P = sum(P_indv.values())
    return P,P_indv