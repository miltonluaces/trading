import numpy as np
import requests
import yahoo_fin.stock_info as si
#import zipline as zl

#price = si.get_live_price('AAPL')
#print('{0:.2f}'.format(price))

hist = si.get_data('AAPL', start_date='01-01-2018', end_date='09-01-2018')
#print(hist)
prices = hist['high'].values
print(prices)

#from alpha_vantage.timeseries import TimeSeries
#import matplotlib.pyplot as plt
#import sys

#def stockchart(symbol):
#    ts = TimeSeries(key='your_key', output_format='pandas')
#    data, meta_data = ts.get_intraday(symbol=symbol,interval='60min', outputsize='full')
#    data['4. close'].plot()
#    plt.title(symbol)
#    plt.show()

#stockchart('AAPL')