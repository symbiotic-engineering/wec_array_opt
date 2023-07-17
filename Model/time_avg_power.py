def run(bodies,Xi,omega):
    P_indv = {body:(1/2)*body.PTOdamp*abs(Xi[body]*omega*1j)**2 for body in bodies}
    P = sum(P_indv.values())
    return P