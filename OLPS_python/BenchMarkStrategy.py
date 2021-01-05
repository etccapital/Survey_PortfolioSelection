import numpy as np
import pandas as pd
import math
from datetime import datetime, date
import matplotlib.pyplot as plt
from OLPSResult import OLPSResult
import scipy.optimize as opt
import helper as hp
from Strategy import Strategy

#Buy and Hold
class BAH(Strategy):
    def __init__(self, stock:str):
        self.stock = stock
    def run(self, df:pd.DataFrame):
        return OLPSResult(df[self.stock])
    def name(self):
        return "Buy and Hold"

#Best Stock - HindSight Strategy
class BS(Strategy):
    def run(self, df:pd.DataFrame):
        ret_to_col = dict()
        for col in df.columns:
            cumret = np.prod(df[col].values)
            ret_to_col[cumret] = col
        best_stock = ret_to_col[max(ret_to_col)]
        return OLPSResult(df[best_stock])
    def name(self):
        return "Best Stock"

#Constant Rebalanced Portfolio
class CRP(Strategy):
    def __init__(self, port):
        if not hp.isvalidport(port): raise Exception("Not a valid portfolio!")
        self.port = np.array(port)
    def run(self, df:pd.DataFrame):
        #note that directly multiplying np arrays with "*" will produce incorrect results
        rel_rets = np.matmul(df.to_numpy(), self.port).transpose()
        ts_daily_rets = pd.Series(index=df.index, data=rel_rets)
        return OLPSResult(ts_daily_rets)
    def name(self):
        return "Constant Rebalanced Portfolio"

#Uniform Constant Rebalanced Portfolio
class UCRP(Strategy):
    def __init__(self):
        pass
    def run(self, df:pd.DataFrame):
        num_cols = df.shape[1]
        uni_port = np.array([1/num_cols for i in range(num_cols)])
        return CRP(uni_port).run(df)
    def name(self):
        return "Uniform Constant Rebalanced Portfolio"
#Best Constant Rebalanced Portfolio - Hindsight Strategy
#In constrast to expectation, direct constrained optimization didn't take a long time.
#Scipy Nb!
class BCRP(Strategy):
    def __init__(self):
        pass
    def run(self, df:pd.DataFrame):
    #Set up constrained optimization
        func = lambda w:-np.prod(np.matmul(df.to_numpy(), w))
        cons = [{'type': 'eq',
                 'fun': lambda w: np.array([sum(w)-1])},
                {'type': 'ineq',
                 'fun': lambda w: np.array([w[i] for i in range(len(w))])}]
        num_cols = df.shape[1]
        init = np.array([1/num_cols for i in range(num_cols)])
        result = opt.minimize(func, x0=init, constraints=cons)
        if not result.success: print("Optimization for BCRP not successful :(")
        return CRP(result.x).run(df)
    def name(self):
        return "Best Constant Rebalanced Portfolio"
