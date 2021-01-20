import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import helper as hp
from cvxopt import solvers, matrix

#Abstract Interface for all Strategy subclasses
#may become more useful in the future
class Strategy():
    #returns an OLPS result object
    def run(self, df:pd.DataFrame):
        pass
    def name(self):
        pass
class FollowtheLoser(Strategy):
    
    def kernel(self):
        pass
    def expert(self):
        pass

    def projection_altenrative(self, weight:np.array, N):
        #Initialize 
        C = hp.numpy_to_cvxopt_matrix(np.eye(N,N))
        d = hp.numpy_to_cvxopt_matrix(weight)
        
        lb = np.zeros(N)
        ub = np.ones(N)
        
        #Fill A & b with lb and ub since cvxopt does not take lb and ub
        A = np.vstack([-np.eye(N), np.eye(N)])
        b = np.concatenate([-lb,ub])
        
        Aeq = hp.numpy_to_cvxopt_matrix(np.ones(N))
        beq = hp.numpy_to_cvxopt_matrix(np.ones(1))
        A = hp.numpy_to_cvxopt_matrix(A)
        b = hp.numpy_to_cvxopt_matrix(b)

        Q = C.T * C
        q = - d.T * C
        Aeq = matrix(Aeq,(1,Aeq.size[0]),'d')
        solvers.options['show_progress'] = False
        soln = solvers.qp(Q, q.T, A, b, Aeq, beq, None, None)
        
        x = np.array(soln['x']).reshape(N,)

        return x
        
