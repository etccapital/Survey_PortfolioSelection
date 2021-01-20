import numpy as np
import pandas as pd
import time
import math
from datetime import datetime, date
import matplotlib.pyplot as plt
from OLPSResult import OLPSResult
import scipy.optimize as opt
import helper as hp
import BenchMarkStrategy as bms
from Strategy import Strategy,FollowtheLoser

class CWMR(FollowtheLoser):
    def __init__(self, epsilon = 0.5, phi = 2, type = 'std'):
        self.t_start = time.process_time()
        self.epsilon = epsilon
        self.phi = phi
        self.type = type
        
        
    def name(self):
        name = "Confidence Weighted Mean Reversion-" + str(self.type)
        return name
    def abbr(self): #abbreviation
        abbr = "CWMR-" + str(self.type)
        return abbr
    
    def kernel(self, data:np.array, mu:np.array, sigma:np.array):
        T, N = data.shape
        mu, sigma = self.expert(data, mu, sigma)
        weight = mu / sum(mu)
        return weight,mu,sigma
    
    def expert(self, data:np.array, mu, sigma):
        T, N = data.shape
        mu = np.reshape(mu,(N,1))
        matlab_ones = np.reshape(np.ones(N),(N,1))
        #Calculate the following variables
        top = np.matmul(np.matmul(matlab_ones.T, sigma) , data[T-1, :].T)
        bot = np.matmul(np.matmul(matlab_ones.T, sigma) , matlab_ones)

        x_bar = top / bot

        
        M = np.matmul(data[T-1, :] , mu)
        V = np.matmul(np.matmul(data[T-1, :] , sigma) , data[T-1, :].T)
        W = np.matmul(np.matmul(data[T-1, :] , sigma) , np.ones(N))
        
        #Calculate the quadratic variables (a,b,c) type check
        if self.type == "std":
            a = (V - x_bar * W + (self.phi**2)*V/2)**2 - (self.phi**4)*(V**2)/4
            b = 2 * (self.epsilon - M) * (V - x_bar*W + (self.phi**2)*V/2)
            c = (self.epsilon-M)**2 - (self.phi**2)*V
        else:
            a = 2 * self.phi * (V **2) - 2 * self.phi * x_bar * V * W
            b = 2 * self.phi * self.epsilon *V - 2 * self.phi * V * M + V - x_bar *W
            c = (self.epsilon-M)**2 - (self.phi**2)*V
        #Calculate two roots and get the Lagrangian Multiplier
        a = np.array(a)
        b = np.array(b)
        t1 = b

        t2 = math.sqrt(b**2 - 4*a*c)
        t3 = 2 * a
        
        if (a!=0) and (np.isreal(t2)) and (t2 > 0):
            gamma1 = (-t1 + t2)/(t3)
            gamma2 = (-t1 - t2)/(t3)
            lamb = max(gamma1,gamma2,0)
        elif (a == 0) and (b != 0):
            gamma3 = -c/b
            lamb = max(gamma3, 0)
        else:
            lamb = 0
            
        # Update the distribution element mu and Sigma - type check
        sigma = sigma.astype(float)

        if self.type == "std":            
            mu = mu - lamb * np.matmul(sigma, (data[T-1, :].T - x_bar * np.ones(N) ).T )
            sqrtu = (-lamb * self.phi * V + math.sqrt((lamb ** 2 ) * (V ** 2)* (self.phi ** 2) + 4 * V ))/2
            if sqrtu !=0:
                
                matr = np.linalg.inv(sigma)  + lamb * self.phi / sqrtu * np.power(np.diag(data[T-1, :]),2) 
                matr = matr.astype(float)
                sigma = np.linalg.inv(matr)
        else:
            mu = mu - lamb * np.matmul(sigma, (data[T-1, :].T - x_bar * np.ones(N)).T)
            
            matr = np.linalg.inv(sigma)  + 2 * lamb * self.phi * np.power(np.diag(data[T-1, :]),2) 
            matr = matr.astype(float)
            sigma = np.linalg.inv(matr)
        
        
        # if det(sigma) <= eps:
        #     sigma = sigma + eps * np.diag(np.ones(N))
        mu = np.reshape(mu,(N,))
        mu = self.projection_altenrative(mu,N)
        sigma = sigma / sum(sigma)/N
        
        return mu, sigma
            
    
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
        
        #Init
        alpha = 1
        mu = alpha * hp.uniform_port(m)
        sigma = np.eye(m,m)/(m**m)
        
        for t in np.arange(1,n+1):
            if t >= 2:
                day_weight,mu,sigma = self.kernel(X[:t-1, :], mu, sigma)
                
            #Normalize the constraint, always useless
            day_weight /= sum(day_weight)
            daily_portfolio[t-1, :] = day_weight.T
            
            #Calculate t's return and total return
            daily_ret[t-1] = np.dot(X[t-1,:],day_weight) * (1 - tc/2*sum(abs(day_weight-day_weight_o)))
            cum_ret *= daily_ret[t-1]
            cumprod_ret[t-1] = cum_ret            
            
            #Adjust weight (t, :) for the transaction cost issue
            #day_weight_o = day_weight.*data(t, :)'/daily_ret(t, 1);
            # day_weight_o= np.multiply(day_weight, X[t-1,:].T) / daily_ret[t-1]
            #Since we assume no transaction cost, this step is ignored
            
        
            #print(f"day {t} , daily ret: {daily_ret[t-1]} , cum ret: {cum_ret}")
        # print(f"\n all daily rets: {daily_ret}")
        # print(f"cum rets: {daily_ret.cumprod()}")
        return OLPSResult(pd.Series(daily_ret,index=df.index), elap_time = time.process_time()-self.t_start)
