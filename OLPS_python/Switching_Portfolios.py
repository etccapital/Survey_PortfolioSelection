from OLPSResult import OLPSResult
import numpy as np
import pandas as pd
import math
import helper as hp
from Strategy import Strategy
import random

def update_weight(df_to_day: np.array, gamma: float, port: np.array):
    
    num_cols = df_to_day.shape[1]
    weight = np.ones(num_cols)
    
    for i in range(len(port)):
        weight[i] = port[i] * (1 - gamma - gamma/(num_cols - 1)) + gamma/(num_cols - 1)
    
    return weight

class SP(Strategy):
    def __init__(self, gamma: float):
        self.gamma = gamma
    
    def run(self, df:pd.DataFrame):
        
        # Initialization
        num_days = df.shape[0]
        num_cols = df.shape[1]
        
        update_port = np.array([1/num_cols for i in range(num_cols)])
        
        cum_ret = 1
        cumprod_ret = np.ones(num_days)
        daily_rets = np.ones(num_days)
        
        # update daily weight of portfolios by SP strategy
        for i in range(num_days):
            if i >= 1:
                update_port = update_weight(df.to_numpy()[:i], self.gamma, 
                                            update_port)
            # normalize the constraint
            sums = sum(update_port)
            for j in range(num_cols):
                update_port[j] = update_port[j]/sums
            if not hp.isvalidport(update_port): raise Exception("Not a valid portfolio!")
            
            day_i_ret = np.matmul(df.to_numpy()[i], update_port)
            daily_rets[i] = day_i_ret
            cum_ret = cum_ret * day_i_ret
            cumprod_ret[i] = cum_ret
        
        ts_daily_rets = pd.Series(index=df.index, data=daily_rets.transpose())
        return OLPSResult(ts_daily_rets)        
    
    def name(self):
        return "Switching Portfolios"