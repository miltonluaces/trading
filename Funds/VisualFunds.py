from os import path
import sys
sys.path.append('D:/source/repos')

import webbrowser as wb
import pandas as pd
import os
import string
from beautifultable import BeautifulTable
import matplotlib.pyplot as plt
import tableprint as tp
import seaborn as sb; sb.set()
from problem_solving.Visual.Misc.Tables import ShowDataFrame
from trading.Funds.DBMgr import DBMgr
from datetime import datetime
from trading.Funds.FundReader import FundReader

fr = FundReader()

class VisualFunds:
    
    def __init__(self):
        self.chartUrl = 'http://www.morningstar.es/es/funds/snapshot/snapshot.aspx?id='
        self.tab = '&tab=13'
        self.dbUrl = 'http://127.0.0.1:49830/browser/'
        dbMgr = DBMgr()
        self.fd = dbMgr.GetFundDict()
        #self.ftUrl = 'https://markets.ft.com/data/funds/tearsheet/charts?s='
        self.ftUrl = 'https://markets.ft.com/data/funds/tearsheet/charts?s='
        self.tvUrl = 'https://www.tradingview.com/chart/?symbol='
        self.tvIdxUrl = 'https://www.tradingview.com/chart/'
        self.histPath = 'D:/data/csv/funds/Portfolio/'
    
    def ShowDB(self):
        #wb.open(self.dbUrl)
        #pgAdmin = "'D:\ProgramFiles\Postgre\pgAdmin 4\bin\pgAdmin4.exe'"
        #os.system(pgAdmin);
        os.system('D:\\ProgramFiles\\Postgre\\"pgAdmin 4"\\bin\\pgAdmin4.exe')

    def ShowQueryRes(self, queryStr):
        dbMgr = DBMgr()
        res = dbMgr.QueryStr(queryStr)
        df = None
        for ro in res.values:
            rowDf = pd.DataFrame(row)
            if df is None:  df = pd.DataFrame(rowDf.T)
            else: df = df.append(rowDf.T)
        df.columns=res.columns.values
        print(df)

    def ShowSP500(self):
        url = 'https://www.marketwatch.com/investing/index/spx/charts'
        wb.open(url)  

    def ShowChart(self, isin):
        url = self.fd[isin]
        url = self.chartUrl + url + self.tab
        wb.open(url)

    def ShowCharts(self, isins):
        for isin in isins:
            self.ShowChart(isin)
            
    def ShowMSChart(self, isin):
        url = fr.GetUrl(isin)
        url = self.chartUrl + url + self.tab
        wb.open(url)

    def ShowMSCharts(self, isins):
        [self.ShowMSChart(isin) for isin in isins]
    
    def ShowFTChart(self, isin, currency):
        url = self.ftUrl + isin + ':' + currency
        wb.open(url)

    def ShowFTCharts(self, isinCurrs):
        for ic in isinCurrs:
            self.ShowFTChart(ic[0], ic[1])

    # fund tuple (isin, currency)
    def ShowFundChart(self, fund_tuple):
        url = self.ftUrl + fund_tuple[0] + ':' + fund_tuple[1]
        wb.open(url)
    
    def ShowFundCharts(self, funds):
        [self.ShowFundChart(fund) for fund in funds]
    
    def ShowTVStockChart(self, ticker, exchange):
        url = self.tvUrl + exchange + '%3A' + ticker
        wb.open(url) 
    
    def ShowTVIndex(self):
        wb.open(self.tvIdxUrl + 'NMfC5gPA' + '/')
        
    def GetQueryRes(self, queryStr):
        dbMgr = DBMgr()
        res = dbMgr.QueryStr(queryStr)
        df = None
        for row in res.values:
            rowDf = pd.DataFrame(row)
            if df is None:  df = pd.DataFrame(rowDf.T)
            else: df = df.append(rowDf.T)
        df.columns=res.columns.values
        return df

    def PrintQueryRes(self, queryStr):
        df = self.GetQueryRes(queryStr)
        print(df)

    def ShowQueryRes(self, queryStr):
       df = self.GetQueryRes(queryStr)
       tab = BeautifulTable()
       for row in df.iterrows:
            tab.append_row(row)
       print(tab)
   
    def ShowTs(self, isin, name):
        ts = pd.read_csv(self.histPath + isin + '.csv', sep='\t')
        ts['dnum'] = [datetime.strptime(x, '%d/%m/%y').date() for x in ts['date']]
        plt.figure(figsize=(22, 10))
        ts['value'].index = ts['dnum']
        sb.lineplot(data=ts['value'], color="blue").set_title(isin + "  " + name)

    
if __name__ == '__main__':

    vf = VisualFunds()
    #vf.ShowChart('LU1731833304')
    #vf.ShowChart('LU0260870158')
    #vf.ShowMSChart('LU0607512851')
    #isins = ['LU1731833304','LU0260870158']
    #vf.ShowCharts(isins)

    #vf.ShowDB()

    #def ShowResult(res):
    #    tab = BeautifulTable()
    #    tab.column_headers["name"]
    #    for row in res:
    #        table.append_row(row)
    #    print(table)


    #df = vf.GetQueryRes('SELECT * FROM fund') 
    #ShowDataFrame(df.head(5))
    #plt.show()

    #isin = 'ES0173394034'
    #vf.ShowFTChart(isin, 'EUR')

    #vf.ShowFTCharts()

    

    #vf.ShowFundChart(['IE00B52VLZ70', 'EUR'])
    #fr = FundReader()
    #monitor = fr.GetFundsDf('D:/Invest/Funds/Monitor.xlsx')
    #print(monitor)
    
    #buy = list(zip(monitor.buy_isin, monitor.buy_curr))
    #sell = list(zip(monitor.sell_isin, monitor.sell_curr))
    #vf.ShowFundCharts(buy)

    #vf.ShowTVStockChart('ACN', 'NYSE')
    
    vf.ShowTVIndex('SP500')