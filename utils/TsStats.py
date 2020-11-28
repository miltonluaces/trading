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

    def test01_getDataPlot():
        ticker = 'VOO'
        start = '2020-01-06'
        end = '2020-06-26'
        data = yfs.get_data(ticker, start_date=start, end_date=end)
        ts = data['close']
        print(ts)

        plt.plot(ts.index, ts)
        plt.show()

        start = '2020-01-20'
        end = '2020-06-12'
        ts1 = GetPeriod(ts, start, end)
        plt.plot(ts1.index, ts1)
        plt.show()
        print(min(ts1))
        print(max(ts1))
        print(np.mean(ts1))
        print(np.std(ts1))
        print(ss.variation(ts1))
        print(GetMaxLoss(ts1))
        print(GetCurrLoss(ts1))

    def test02_GetReldiff():
        ts = [20.89, 21.26, 21.36, 21.81, 22. ,25.40, 23.45, 23.39, 22.53, 22.34, 24.15, 24.89, 24.79, 24.48, 24.87, 26.54, 26.98, 22.87]    
        rdts = GetReldiff(ts)
        print(rdts)

    def test03_GetReldiffStep():
        ts = [20.89, 21.26, 21.36, 21.81, 22. ,25.40, 23.45, 23.39, 22.53, 22.34, 24.15, 24.89, 24.79, 24.48, 24.87, 26.54, 26.98, 22.87]    
        for step in range(1,4):
            rdts = GetReldiff(ts, step)
            print('Step :', step)
            print(rdts)
    
    def test04_GetMaxRelDiffStep():
        ts = [20.89, 21.26, 21.36, 21.81, 22. ,25.40, 23.45, 23.39, 22.53, 22.34, 24.15, 24.89, 24.79, 24.48, 24.87, 26.54, 26.98, 22.87]    
        for step in range(1,5):
            mrd = GetMaxRelDiffStep(ts, step)
            print('Step ', step, ' Mrd = ', mrd)


    test04_GetMaxRelDiffStep()