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

    
    AddPLOperation(isin = 'ACN',  shares = 15,  purchValue = 165.50, currValue = 210.46)
    AddPLOperation(isin = 'JETS', shares = 130, purchValue = 15.07, currValue = 20.65)
    AddPLOperation(isin = 'JETS', shares = 40,  purchValue = 15.96, currValue = 20.68)
    AddPLOperation(isin = 'GOOG', shares = 1,   purchValue = 1431.39, currValue = 1793.52)
    AddPLOperation(isin = 'ACN',  shares = 10,  purchValue = 165.5, currValue = 245.48)
    AddPLOperation(isin = 'ACN',  shares = 10,  purchValue = 165.5, currValue = 245.48)
    AddPLOperation(isin = 'CPRI', shares = 100, purchValue = 6.73,  currValue = 7.55)
    AddPLOperation(isin = 'KO'  , shares = 100, purchValue = 6.45, currValue = 9.98)

    