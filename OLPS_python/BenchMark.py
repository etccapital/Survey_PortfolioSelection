import numpy as np
import pandas as pd
from datetime import datetime, date
import matplotlib.pyplot as plt
from varname import nameof

#After running a strategy, an OLPSResult object will be returned
#can be used for plotting or printing important information
class OLPSResult:
    #daily_ret is the relative return of each day
    def __init__(self, daily_ret: pd.Series):
        self.time_range = daily_ret.index
        self.daily_ret = daily_ret
        self.cum_rets = self.getCumReturn()
    #returns the time series of daily relative return
    def getRelReturn(self):
        return self.daily_ret
    # returns a DatetimeIndex object, representing the time range
    def getTimeRange(self):
        return self.time_range
    # returns the time series of cumulative return
    def getCumReturn(self):
        values = []
        cum_ret = 1
        for rel_ret in self.daily_ret.values:
            cum_ret *= rel_ret
            values.append(cum_ret)
        return pd.Series(data=values, index=self.time_range)

#Abstract Interface for all strategy classes
class Strategy:
    # def __init__(self, df_rel_price: pd.DataFrame):
    #     self.df_rel_price = df_rel_price
    def summary(self):
        pass
    def run(self,df:pd.DataFrame,*args,**kwargs):
        pass
    def name(self):
        pass
#superclass for all benchmark strategy classes
class BenchMarkStrategy(Strategy):
    pass

#Buy and Hold strategy
class BAH(BenchMarkStrategy):
    def __init__(self,stock: str):
        BenchMarkStrategy.__init__(self)
        self.stock = stock
        self.name = "Buy and Hold"
    def name(self):
        return "Buy and Hold"
    def run(self, df: pd.DataFrame):
        return OLPSResult(self.df_rel_price[self.stock])

# def BestStock(BenchMarkStrategy):
#     def run(self):
#

#plot a series of daily returns for comparison purpose
#can pass in arbitrary number of OLPSResult objects
# def olps_plot(*olps_results: OLPSResult,ax):
#     # Check that the time range of all inputs are equal
#     result1 = olps_results[0]
#     for result in olps_results:
#         if sum(result.getTimeRange() != result1.getTimeRange()) > 0:
#             raise IndexError('Time range of all OLPS results need to match!')
#     #concatenate all time series
#     df_concat = pd.concat([result.getCumReturn() for result in olps_results],axis = 1)
#     df_concat.plot(colormap="Dark2", kind="line", figsize = (14,7),ax=ax)
#     plt.show()
#     print([nameof(result) for result in olps_results])

