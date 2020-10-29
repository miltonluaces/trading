from os import path
import sys
sys.path.append(path.abspath('D:/source/repos/ProblemSolving/'))

import webbrowser as wb
import pandas as pd
import os
from beautifultable import BeautifulTable
import matplotlib.pyplot as plt
import tableprint as tp
import seaborn as sb; sb.set()
from problem_solving.Visual.Misc.Tables import ShowDataFrame
from trading.Funds.DBMgr import DBMgr
from datetime import datetime

class VisualFunds:
    
    def __init__(self):
        self.chartUrl = 'http://www.morningstar.es/es/funds/snapshot/snapshot.aspx?id='
        self.tab = '&tab=13'
        self.dbUrl = 'http://127.0.0.1:49830/browser/'
        dbMgr = DBMgr()
        self.fd = dbMgr.GetFundDict()
        self.ftUrl = 'https://markets.ft.com/data/funds/tearsheet/charts?s='
        self.histPath = 'D:/data/csv/funds/Portfolio/'
    
    def ShowDB(self):
        #wb.open(self.dbUrl)
        #pgAdmin = "'D:\ProgramFiles\Postgre\pgAdmin 4\bin\pgAdmin4.exe'"
        #os.system(pgAdmin);
        os.system('D:\\ProgramFiles\\Postgre\\"pgAdmin 4"\\bin\\pgAdmin4.exe')

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

    def ShowFTChart(self, isin, currency):
        url = self.ftUrl + isin + ':' + currency
        wb.open(url)

    def ShowFTCharts(self, isinCurrs):
        for ic in isinCurrs:
            self.ShowFTChart(ic[0], ic[1])

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