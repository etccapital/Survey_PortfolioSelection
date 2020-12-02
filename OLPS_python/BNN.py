#All the pattern matching based strategies
import numpy as np
import pandas as pd
import math
from datetime import datetime, date
import matplotlib.pyplot as plt
from OLPSResult import OLPSResult
import scipy.optimize as opt
import helper as hp
from Strategy import Strategy

#Nonparametric kernel-based sample selection
def isSimilarKernel(x:np.array, y:np.array, c:float, l:float):
    if x.shape != y.shape: raise ArithmeticError("Dimensions of inputs should match!")
    #F-norm
    return np.linalg.norm(x-y) <= c/l

x = np.array([[1.5,2],[2,3]])
y = np.array([[1,2],[2,3]])
c = 0.5
l = 1
print(isSimilarKernel(x,y,c,l))

#Non-parametric nearest neighbour log-optimal starategy
class BNN(Strategy):
    def run(self, df):
        pass

