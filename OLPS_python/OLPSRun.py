#This is the main interface
from CWMR import CWMR
import numpy as np
import pandas as pd
from pandas.tseries.offsets import *
from datetime import datetime, date
import matplotlib.pyplot as plt
import BenchMarkStrategy as bms
import OLPSResult as olps
from varname import nameof
import copy
from xone import calendar
from PAMR import PAMR
from RMR import RMR
work_dir = "D:/OLPS/Survey_PortfolioSelection/OLPS_python/"

#create a DatetimeIndex with all trading days from start_date to end_date
def business_dates(start_date:str, end_date:str):
    us_cal = calendar.USTradingCalendar()
    kw = dict(start=start_date, end=end_date)
    return pd.bdate_range(**kw).drop(us_cal.holidays(**kw))

#modify the index column of the given dataframes to be a time series(DatetimeIndex object)
def add_time(df:pd.DataFrame, start_date, end_date):
    num_rows = df.shape[0]
    time_col = business_dates(start_date, end_date)
    df.index = time_col[:num_rows]
#all-in-one function, compare multiple strategies on the same dataset
def compare_strats(strats:list, df:pd.DataFrame, df_name = "", print_option=True, plot_option=True):
    results = []
    for s in strats:
        s_result = s.run(df)
        results.append(copy.copy(s_result))
        if print_option:
            print("{} Strategy on {} dataset{}{}".format(s.name(),df_name, "\n", s_result.__str__()))
    if plot_option:
        labels = [type(s).__name__ for s in strats]
        olps.olps_plot(results, labels=labels, title = df_name)

if __name__ == "__main__":
    # load data
    # df_nyseo = pd.read_excel("Datasets/nyse-o.xlsx", engine='openpyxl')
    # df_nysen = pd.read_excel("Datasets/nyse-n.xlsx", engine='openpyxl')
    # df_tse = pd.read_excel("Datasets/tse.xlsx", engine='openpyxl')
    df_sp500 = pd.read_excel(work_dir+"Datasets\\sp500.xlsx", engine='openpyxl')
    # df_msci = pd.read_excel("Datasets/msci.xlsx", engine='openpyxl')
    # df_djia = pd.read_excel("Datasets/djia.xlsx", engine='openpyxl')

    # #add time column as index
    # add_time(df_nyseo, "1962-07-03", "1984-12-31")
    # add_time(df_nysen, "1985-01-01", "2010-06-30")
    # add_time(df_tse, "1994-01-04", "1998-12-31")
    add_time(df_sp500, "1998-01-02", "2003-01-31")
    # add_time(df_msci, "2006-04-01", "2010-03-31")
    # add_time(df_djia, "2001-01-14", "2003-01-17")


    df_name = "SP500"
    #uniformly distribute wealth on all stocks
    num_stocks = df_nyseo.shape[1]
    portfolio = [1/df_nyseo.shape[1] for i in range(num_stocks)]
    #a list of all strategies to be tested
    #strats = [bms.CRP(portfolio), bms.BS(), bms.BCRP()]
    strats = []
    strats.append(PAMR())
    strats.append(RMR())
    strats.append(CWMR(type='var'))
    #compare them on S&P500
    compare_strats(strats, df_nyseo, df_name=df_name, print_option=True,plot_option=True )
