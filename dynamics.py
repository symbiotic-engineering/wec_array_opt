import numpy as np

def solve(initial_hydro,a,omega,bodies):
    A ={body:initial_hydro[body]['A'] for body in bodies}
    B ={body:initial_hydro[body]['B'] for body in bodies}
    C ={body:initial_hydro[body]['C'] for body in bodies}
    F ={body:initial_hydro[body]['F'] for body in bodies}
    M ={body:initial_hydro[body]['M'] for body in bodies}

    tf = {body:(-(omega**2)*(A[body]+M[body]) + 1j*omega*B[body] + C[body])**-1 for body in bodies}

    forces = {body1:{body2: a[body1][body2]*F[body1][body2] for body2 in bodies}for body1 in bodies}
    force_sum = {body:sum(forces[body].values()) for body in bodies}

    Xi = {body:force_sum[body]*tf[body] for body in bodies}
    return Xi