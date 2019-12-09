import numpy as np
import pandas as pd


# Price volatility
def Volatility(stockTS, mw):
     dailyPercChange = stockTS.pct_change()
     volatility = dailyPercChange.rolling(mw).std() * np.sqrt(mw) 
     return(volatility)

# MA crossing signals
def MACrossSignals(date, price, shortW, longW):
     signals = pd.DataFrame(index=date)
     signals['signal'] = 0.0
     signals['shortMA'] = price.rolling(window=shortW, min_periods=1, center=False).mean()
     signals['longMA'] = price.rolling(window=longW, min_periods=1, center=False).mean()
     signals['signal'][shortW:] = np.where(signals['shortMA'][shortW:] > signals['longMA'][shortW:], 1.0, 0.0)   
     signals['pos'] = signals['signal'].diff()
     print(signals)
     return signals

# Bollinger bands
def BolingerBands(price, mw, nStds):
    movMean = price.rolling(window=mw).mean()
    movStd  = price.rolling(window=mw).std()
    upr = movMean + (movStd * nStds)
    lwr = movMean - (movStd * nStds)
    return movMean, upr, lwr

