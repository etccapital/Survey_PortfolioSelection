import numpy as np
import pandas as pd
import math
import time
from datetime import datetime, date
import matplotlib.pyplot as plt
from OLPSResult import OLPSResult
import scipy.optimize as opt
import helper as hp
import BenchMarkStrategy as bms
from Strategy import Strategy,FollowtheLoser

class PAMR(FollowtheLoser):
    def __init__(self, epsilon = 0.5, C = 500, type = 1):
        self.t_start = time.process_time()
        self.epsilon = epsilon
        self.C = C
        self.type = type
        
        
    def name(self):
        name = "Passive Aggressive Mean Reversion"
        if self.type == 0:
            return name
        else:
            name = name + "-" + str(self.type)
            return name
    def abbr(self): #abbreviation
        abbr = "PAMR"
        if self.type == 0:
            return abbr
        else:
            abbr = abbr + "-" + str(self.type)
            return abbr
    
    def kernel(self, data:np.array, weight_o:np.array, eta):
        T, N = data.shape
        weight = weight_o - eta * (data[T-1,:].T - sum(data[T-1,:]) / N )
        weight = self.expert(weight,N)
        return weight
    
    def expert(self, weight:np.array,N):
        return self.projection_altenrative(weight,N)
    
    def lagrange_multiplier(self, data:np.array, t, m, daily_ret:np.array, eta):
        vec = data[t-1,:] -1/m*sum(data[t-1,:])
        if self.type == 2:
            denominator = np.dot(vec,vec.T) + 0.5/self.C
        else:
            denominator = np.dot(vec,vec.T)
        if denominator != 0:
            eta = (daily_ret[t-1] - self.epsilon) / denominator
            
        return max(0, eta)
            
    
    def run(self, df:pd.DataFrame, tc = 0):
        X = df.to_numpy()
        n, m = X.shape
        # Variables for return, start with uniform weight
        cum_ret = 1
        cumprod_ret = np.ones(n)
        daily_ret = np.ones(n)
        day_weight = hp.uniform_port(m)
        day_weight_o = np.zeros(m)
        daily_portfolio = np.zeros((n, m))
        eta = 0 
        
        for t in np.arange(1,n+1):
            if t >= 2:
                day_weight = self.kernel(X[:t-1, :], day_weight, eta)
                
            #Normalize the constraint, always useless
            day_weight /= sum(day_weight)
            daily_portfolio[t-1, :] = day_weight.T
            
            #Calculate t's return and total return
            # print("Day {0}, Dayweight {1}".format(t,day_weight))
            # print("Day {0}, X {1}".format(t,X[t-1,:]))
            # print("Day {0}, day_weight_o {1}".format(t,day_weight_o))
            # print("Day {0}, daily_ret {1}".format(t,daily_ret))
            # print("Day {0}, cumprod_ret {1}".format(t,cumprod_ret))
            daily_ret[t-1] = np.dot(X[t-1,:],day_weight) * (1 - tc/2*sum(abs(day_weight-day_weight_o)))
            cum_ret *= daily_ret[t-1]
            cumprod_ret[t-1] = cum_ret            
            
            #Adjust weight (t, :) for the transaction cost issue
            #day_weight_o = day_weight.*data(t, :)'/daily_ret(t, 1);
            # day_weight_o= np.multiply(day_weight, X[t-1,:].T) / daily_ret[t-1]
            #Since we assume no transaction cost, this step is ignored
            
            #Calculate the Lagarange Multiplier
            eta = self.lagrange_multiplier(X, t, m, daily_ret, eta)
            #print(f"day {t} , daily ret: {daily_ret[t-1]} , cum ret: {cum_ret}")
        # print(f"\n all daily rets: {daily_ret}")
        # print(f"cum rets: {daily_ret.cumprod()}")
        return OLPSResult(pd.Series(daily_ret,index=df.index), elap_time = time.process_time()-self.t_start)
