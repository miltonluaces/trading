import sys
sys.path.append('D:/source/repos')
from utilities.std_imports import *
from trading.Funds.DBMgr import DBMgr


def GetStockSwingOperations():
    stock_operations = pd.read_excel(io='D:/Invest/Data/Trading/Swing.xlsx', sheet_name='Stocks')
    stock_operations = stock_operations.iloc[1:, 1:6]
    stock_operations = stock_operations.dropna(how='all')
    stock_operations.columns = ['ticker', 'shares', 'value', 'eurValue','op']
    return stock_operations

def RegisterSwingOperations(sso):
    dbMgr = DBMgr()
    for row in sso.iterrows():
        if row[1]['op'] == 'B':
            dbMgr.AddPortfolio_Stock(ticker=row[1]['ticker'], shares=row[1]['shares'], purchValue=row[1]['eurValue'], trading='POS', broker='IB')
        elif row[1]['op'] == 'S':
            print('Not implemented')
        else:
            print('Error')
    
    print('\n Operations registered.')
    


if __name__ == '__main__':

    sso = GetStockSwingOperations()
    print(sso)

    RegisterSwingOperations(sso)