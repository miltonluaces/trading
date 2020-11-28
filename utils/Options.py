import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from yahoo_fin import options

def GetDates(ticker):
    exp_dates = options.get_expiration_dates(ticker)
    return pd.DataFrame(exp_dates)

def GetDate(df, idx):
    return df.iloc[idx].values[0]

def GetChain(ticker, dates, idx, type='calls'):
    chain = options.get_options_chain(ticker, GetDate(dates, idx))
    return chain[type]

def GetPrice(ticker, date, strike, type='calls'):
    chain = options.get_options_chain(ticker, date)[type]
    return (float)(chain[chain['Strike']==strike]['Last Price'])

def OptAnalysis(tbl, target_prices):
    tabl = tbl
    for tp in target_prices:
       tabl[tp] = -tabl['Idm'].subtract(tp)   
       tabl[tp][tabl[tp]<0] = 0
    for tp in target_prices:
       tabl[str(tp)+'%'] = round(tabl[tp]/tabl['Premium']*100).astype(int)
    return tabl

def PlotAnalysis(tbl, n=0):
    if n==0: 
        tabl= tbl
    else:
        tabl=tbl.head(n)
    


if __name__ == '__main__':
    print('Options\n')