import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import datetime as dt
import yahoo_fin.stock_info as yfs
import scipy.stats as ss

def GetPeriod(ts, start, end):
    return ts[(ts.index> start) & (ts.index <= end)]

def GetMaxLoss(ts):
    ts_min = min(ts)
    ts_max = max(ts)
    loss = (ts_max - ts_min)/ ts_max
    return round((loss*100),1)

def GetCurrLoss(ts):
    ts_max = max(ts)
    ts_curr = ts.tail(1).values[0]
    loss = (ts_max - ts_curr)/ ts_max
    return round((loss*100),1)

def GetReldiff(ts, step=1):
    rd = [round((ts[i+step]-ts[i])*100/ts[i],2) for i in range(len(ts)-step)]
    nans = np.full([step], np.nan)
    return [*nans, *rd]

def GetMaxRelDiffStep(ts, maxStep):
    relDiffs = [GetReldiff(ts=ts, step=step) for step in range(1,maxStep+1)]
    return max([relDiffs[i][len(relDiffs[i])-1] for i in range(0,maxStep)])


#____________________________________________________________________________________________________________________________________________________________________________________________________


if __name__ == '__main__':
    print('StockFcst\n')

   