import sys
sys.path.append('D:/source/repos')
from trading.Funds.DBMgr import DBMgr
from trading.Funds.CurrencyExchange import CurrencyExchange

dbMgr = DBMgr()
ce = CurrencyExchange()
ce.LoadRates('EUR')

def AddPLOperation(isin, shares, purchValue, currValue):
    currAss = dbMgr.GetFundCurrencyAsset(isin)
    currency = round(1.0/ce.GetRate(currAss['currency']),2)
    asset = currAss['asset']
    dbMgr.AddPLOperation(isin, shares, purchValue, currValue, currency, asset)
    print('Added operation on ', isin)



if __name__ == '__main__':

    
    