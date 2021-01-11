#Contains functions that are used in multiple modules.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from cvxopt import matrix


#check if input is a valid portfolio
def isvalidport(port:np.array):
    #round to four digits to prevent slight numerical error from affecting the final result
    return round(sum(port),4) == 1 and sum([round(w,4) >= 0 for w in port]) == len(port)
def checkvalidport(port:list):
    if not isvalidport(port): raise Exception(f"\n{port} is Not a valid weight combination! Its sum is {sum(port)}")
#returns a uniform portfolio
def uniform_port(n:int):
    return np.array([1/n for i in range(n)])
def numpy_to_cvxopt_matrix(A):
    if not isinstance(A, np.double): 
        A = A.astype(np.double)
    if A is None:
        return A
    if isinstance(A, np.ndarray):
        if A.ndim == 1:
            return matrix(A, (A.shape[0], 1), 'd')
        else:
            return matrix(A, A.shape, 'd')
    else:
        return A
