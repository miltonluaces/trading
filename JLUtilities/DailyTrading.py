import sys
sys.path.append('D:/source/repos')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import time
import seaborn as sb; sb.set()
import yahoo_fin.stock_info as yfs
import yahoo_finance as yf
import Trading.Funds
from alpha_vantage.timeseries import TimeSeries
from trading.Funds.FundReader import FundReader
from trading.Funds.DBMgr import DBMgr
from trading.Funds.Monitor import *
from trading.Funds.VisualFunds import VisualFunds



# MonitorChart 
#____________________________________________________________________________________________________________________________________________________________________

# Shows daily price (close) of a stock given the ticker and number of days 
def Stock_chart(ticker, ndays=180):
    today = dt.date.today()
    data = yfs.get_data(ticker, start_date=today - dt.timedelta(days=ndays), end_date=today)
    plt.figure(figsize=(20, 10))
    data['close'].plot()
    plt.title(ticker)
    plt.show()


# StockChart
#____________________________________________________________________________________________________________________________________________________________________

def PlotStock(df, ticker):
    plt.figure(figsize=(20, 10))
    df[ticker].plot()
    plt.title(ticker)
    plt.show()
    
def Stock_intchart(ticker, ndays=180):
    today = dt.date.today()
    data = yfs.get_data(ticker, start_date=today - dt.timedelta(days=ndays), end_date=today)
    fig = plt.line(data, y='close', title=ticker)

    fig.update_xaxes(rangeslider_visible=True,rangeselector=dict(
            buttons=list([
                dict(count=15, label="15d", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    fig.show()

def PlotIntStock(df, ticker):
    fig = px.line(df, y=ticker, title=ticker)

    fig.update_xaxes(rangeslider_visible=True,rangeselector=dict(
            buttons=list([
                dict(count=15, label="15d", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    fig.show()

def GenHistory(tickers, ndays, filename):
    today = dt.date.today()
    data = yfs.get_data(tickers[0], start_date=today - dt.timedelta(days=ndays), end_date=today)
    df = data.drop(['open', 'high', 'low', 'adjclose', 'volume', 'ticker'], axis=1)
    df.columns = [tickers[0]]
    for i in range(1,len(tickers)):
        try:
            data = yfs.get_data(tickers[i], start_date=today - dt.timedelta(days=ndays), end_date=today)
            df[tickers[i]]=data['close']
            print(i, ' : ', tickers[i])
        except(Exception) as error:
            print('Error in ', tickers[i])
        
    df.to_csv('D:/Invest/data/stock_hist/'+ filename + '_' + str(ndays) + '.csv')
    print(filename, ' generated.')

# StockTsAnalysis
#____________________________________________________________________________________________________________________________________________________________________



# TESTING
#____________________________________________________________________________________________________________________________________________________________________

if __name__ == '__main__':
    print('DailyTrading\n')

    #vf = VisualFunds()
    #stocks = vf.GetQueryRes("SELECT isin FROM investView() WHERE asset = 'S'")
    #for i in range(stocks.shape[0]):
    #    Stock_chart(stocks.iloc[i]['isin'])

