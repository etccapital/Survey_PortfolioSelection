import numpy as np
import pandas as pd
import time
from datetime import datetime, date
import matplotlib.pyplot as plt
from OLPSResult import OLPSResult
import scipy.optimize as opt
import helper as hp
import BenchMarkStrategy as bms
from Strategy import FollowtheLoser

class RMR(FollowtheLoser):
    def __init__(self, epsilon = 5, W = 5):
        self.t_start = time.process_time()
        self.epsilon = epsilon
        self.W = W
        
        
    def name(self):

        return "Robust Median Reversion"
    def abbr(self): #abbreviation
        return "RMR"
    
    def l1median_VaZh_z(self, X: np.array, medIn = 0, zerotol = 1e-15, tol = 1e-9, maxiter = 200):
        n, m = X.shape
        if medIn == 0:
            medIn = np.median(X)
        iterdis = 1
        iter = 0 
        y = np.array([medIn])
        
        while (iterdis > 0) and (iter < maxiter):
            Tnum = np.zeros([1,m])
            R = np.zeros([1,m])
            Tden = 0 
            yita = 0
            for i in np.arange(n):
                dist = np.linalg.norm(X[i,:] - y)
                if dist >= zerotol:
                    Tnum += X[i,:]/dist
                    Tden += 1/dist
                    R += (X[i, :] - y)/dist
                else:
                    yita = 1 
            
            if Tden == 0:
                T = 0
            else:
                T = Tnum/Tden

            if np.linalg.norm(R) == 0:
                r = 0
            else:
                r = min(1, yita/np.linalg.norm(R))
                
            Ty = (1-r) * T + r * y
            iterdis = np.linalg.norm(Ty-y, ord = 1) - tol*np.linalg.norm(y, ord = 1)
            iter += 1
            y = Ty 
        return y
    
    def day_weight(self, data_close:np.array, X: np.array, t1:int, day_weight:np.array):
        T, N = X.shape
        if t1 < self.W + 2:
            x_t1 = X[t1-1,:]
        else:

            x_t1 = np.divide(self.l1median_VaZh_z(data_close[t1-self.W:t1-1,:]), data_close[t1-1,:])
        
        if (np.linalg.norm(x_t1 - np.mean(x_t1))) ** 2 == 0:
            tao = 0
        else:
            tao = min(0, (np.matmul(x_t1, day_weight)-self.epsilon)/((np.linalg.norm(x_t1 - np.mean(x_t1))) ** 2))
        day_weight = day_weight - tao * (x_t1 - np.mean(x_t1) * np.ones(x_t1.shape))
        day_weight = day_weight.reshape(N,)

       
        
        day_weight = self.projection_altenrative(day_weight,N)
        
        return day_weight
        
    def run(self, df:pd.DataFrame, tc = 0):
        X = df.to_numpy()
        n, m = X.shape
        # Variables for return, start with uniform weight
        run_ret = 1
        total_ret = np.ones(n)
        daily_ret = np.ones(n)
        day_weight = hp.uniform_port(m)
        day_weight_o = np.zeros(m)
        day_weight_n = np.zeros(m)
        turno = 0

        #Init
        data_close = np.ones([n,m])
        
        for t in np.arange(1,n+1):
            if t >= 2:
                data_close[t-1,:] = np.multiply(data_close[t-2,:], X[t-1,:])
                
        for t in np.arange(0,n):
            #Step 1 Receive stock price relatives
            
            #Step 2 Calculate t's return and total return
            daily_ret[t] = np.dot(X[t,:],day_weight) * (1 - tc/2*sum(abs(day_weight-day_weight_o)))
            run_ret *= daily_ret[t]
            total_ret[t] = run_ret
            
            #Adjust weight[t, :] for the transaction cost issue
            day_weight_o = np.multiply(day_weight, X[t,:].T) / daily_ret[t]
            
            #Step 3 Update Portfolio 
            if t < n+1 :
                
                day_weight_n = self.day_weight(data_close,X, t+1, day_weight)
                
                
                turno = turno + sum(abs(day_weight-day_weight_o))
                day_weight = day_weight_n

        return OLPSResult(pd.Series(daily_ret,index=df.index), elap_time = time.process_time()-self.t_start)
