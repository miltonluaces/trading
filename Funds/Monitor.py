# Definitions
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

from os import path
import sys
sys.path.append(path.abspath('D:/source/repos'))

from trading.Funds.DBMgr import DBMgr
from trading.Funds.FundProcess import *
from trading.Stocks.StockProcess import *
from trading.Funds.VisualFunds import VisualFunds

db = DBMgr()
vf = VisualFunds()

# Monitor groups
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

sell = ['ES0173394034', 'LU0048365026', 'LU0607516092']
news = ['LU1731833304', 'LU0267388220']  
dfns = ['LU0219434361','']
minvol = ['LU15643111410','IE00B6R33267','LU0450104905']
grow = []
perf = ['LU1715324858']
hiyi = ['LU0370790650']


# Methods
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

def UpdateProportionVolatility():
        UpdateInvProportion()
        UpdateFundVolatility()

def Initialize():  
    vf = VisualFunds()
    print('Initialized')

def UpdateAssetsPerformance():
    UpdateFundValues()
    UpdateStockValues()
    UpdateOptionValues()
    InsertPerformanceFunds()
    InsertPerformanceStocks()
    InsertPerformanceOptions()
    InsertPerformanceTotal()

def ShowInvCharts():
    isins = db.GetInvestIsins(1)
    vf.ShowCharts(isins)

def ShowInvFTCharts():
    isinCurrs = db.GetInvestIsinCurrs(1)
    vf.ShowFTCharts(isinCurrs)

    
# Monitoring
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    print('test')
    #Initialize(upd=True)

    #vf.ShowDB()

    #vf.ShowChart('LU0607512851')

    #funds = ['LU0607512851','LU0155303323','LU0130729220','IE00B3DJ5M15','LU0255976994']
    #vf.ShowMSCharts(funds)
    #vf.ShowCharts(news)

    #vf.ShowSP500()
    #vf.ShowChart('LU0049842262')


    #ShowInvFTCharts()
