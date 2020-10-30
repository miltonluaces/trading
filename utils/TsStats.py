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


if __name__ == '__main__':
    print('StockFcst\n')

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
    