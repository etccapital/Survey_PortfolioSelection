from OLPSResult import OLPSResult
import numpy as np
import pandas as pd
import math
import helper as hp
from Strategy import Strategy
import random

def findQ(b: np.array, df_to_day: np.array, de10: float, delta: float):
    
    num_cols = df_to_day.shape[1]
    P = np.prod(np.matmul(df_to_day, b))
    Q = P * min(1, np.exp((b[num_cols-1] - 2*de10)/(num_cols*delta)))
    
    return Q


def getUniversalWeight(df_to_day: np.array):
    
    de10 = 4e-3 # minimum coordinate
    delta = 5e-3 # spacing of grid
    M = 10 # number of samples
    S = 5 # number of steps in the random walk

    num_cols = df_to_day.shape[1] # number of stocks
    
    r = np.array([1/num_cols for i in range(num_cols)])
    b = np.ones(num_cols)
    
    allM = []
    
    new_port = np.zeros(num_cols)
    
    # generate M=10 universal portfolio starting from uniform portfolio
    for m in range(M):
        b = r.copy()
        for s in range(S):
            bnew = b.copy()
            j = random.randint(0, num_cols-2)
            
            a = random.randint(1, 2)
            if(a == 2):
                a = -1
            
            bnew[j] = b[j] + (a*delta)
            bnew[num_cols-1] = b[num_cols-1] - (a*delta)
            if(bnew[j] >= de10 and bnew[num_cols-1] >= de10):
                x = findQ(b, df_to_day, de10, delta)
                y = findQ(bnew, df_to_day, de10, delta)
                
                pr = min(y/x, 1)
                temp = random.random()
                
                if temp < pr:
                    b = bnew.copy()
        
        allM.append(b)
        
    for row in range(num_cols):
        s = 0
        for port in allM:
            s = s + port[row]
        new_port[row] = s/M
    
    return new_port
    
class UP(Strategy):
    def __init__(self):
        pass
    def run(self, df:pd.DataFrame):
        # get number of days and number of stocks
        num_days = df.shape[0]
        num_cols = df.shape[1]
        
        # get initial portfolio
        # prev_port = np.zeros(25)
        update_port = np.array([1/num_cols for i in range(num_cols)])
        
        # some initialization
        daily_rets = np.ones(num_days)
        cum_ret = 1
        cumprod_ret = np.ones(num_days)

        
        # update daily return day by day since weight changes
        for i in range(num_days):
            if i >= 1:
                update_port = getUniversalWeight(df.to_numpy()[:i])
            for j in range(num_cols):
                update_port[j] = update_port[j]/sum(update_port)
            if not hp.isvalidport(update_port): raise Exception("Not a valid portfolio!")
            day_i_ret = np.matmul(df.to_numpy()[i], update_port)
            daily_rets[i] = day_i_ret
            cum_ret = cum_ret * day_i_ret
            cumprod_ret[i] = cum_ret
            # prev_port = 
        
        # convert list into ndarray
        # daily_rets = np.array(daily_rets)
        ts_daily_rets = pd.Series(index=df.index, data=daily_rets.transpose())
        return OLPSResult(ts_daily_rets)
    
    
    def name(self):
        return "Universal Portfolio"