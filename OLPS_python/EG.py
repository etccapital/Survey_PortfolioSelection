import numpy as np
import pandas as pd
from OLPSResult import OLPSResult
import helper as hp
from Strategy import Strategy


def eg_kernel(data: np.array, weight_o: np.array, eta: float):
    
    T = data.shape[0]
    N = data.shape[1]
    weight = np.zeros(N)
    denominator = np.matmul(data[T-1], weight_o)
    for i in range(N):
        M = np.exp(eta * data[T-1][i] / denominator)
        weight[i] = weight_o[i] * M
    
    sums = sum(weight)
    for i in range(N):
        weight[i] = weight[i]/sums
    return weight
        



class EG(Strategy):

    def __init__(self, eta):
        self.eta = eta

    def run(self, df:pd.DataFrame):
        n = df.shape[0]
        m = df.shape[1]
        cum_ret = 1
        cumprod_ret = np.ones(n)
        daily_ret = np.ones(n)
        day_weight = np.array([1/m for i in range(m)])
        day_weight_o = np.zeros(m)
        daily_portfolio = np.zeros( (n, m) )
    
        for i in range(n):
            if i >= 1:
                day_weight = eg_kernel(df.to_numpy()[:i], day_weight, self.eta)
            sums = sum(day_weight)
            for j in range(m):
                day_weight[j] = day_weight[j]/sums
            #for k in range(m):
            #    daily_i_ret = 
            daily_i_ret = np.matmul(df.to_numpy()[i], day_weight)
            daily_ret[i] = daily_i_ret
            cum_ret = cum_ret * daily_i_ret
            cumprod_ret[i] = cum_ret
        
        ts_daily_rets = pd.Series(index=df.index, data=daily_ret.transpose())
        return OLPSResult(ts_daily_rets)
             
    
    
    def name(self):
        return "Exponential Gradient"