from os import path
import sys
sys.path.append('D:/source/repos')
from utilities.std_imports import *
import webbrowser as wb

#https://stackoverflow.com/questions/25338608/download-all-stock-symbol-list-of-a-market


class Exchange:

    def __init__(self):
        self.path = 'D:/Invest/Data/exchange/'
        self.nyse = 'https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download'
        self.nasdaq ='https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download'
        self.amex = 'https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download'

        self.exchg = None

    def download_exchanges(self):
        wb.open(nyse)
        wb.open(nasdaq)
        wb.open(amex)
        #copy from download

    def gen_exchange(self):
        nyse = pd.read_csv(self.path_ + 'nyse.csv')[['Symbol', 'Name']]
        nyse['exchange'] = 'NYSE'
        nasdaq = pd.read_csv(self.path + 'nasdaq.csv')[['Symbol', 'Name']]
        nasdaq['exchange'] = 'NASDAQ'
        amex = pd.read_csv(self.path + 'amex.csv')[['Symbol', 'Name']]
        amex['exchange'] = 'AMEX'

        df = pd.concat([nyse, nasdaq, amex])
        df.to_csv(path + 'exchange.csv')
        print('exchange.csv generated.')

    def load_exchange(self):
        self.exchg = pd.read_csv(self.path + 'exchange.csv')
        self.exchg.index = self.exchg['Symbol']

    
    def get_exchange(self, ticker):
        try:
            return self.exchg[self.exchg['Symbol']==ticker]['exchange'][0]
        except:
            print(ticker, 'not found.')

    def get_sector(self, ticker):
        try:
            return self.sector[self.sector['Symbol']==ticker]['Sector'][0]
        except:
            print (ticker, 'exchange not found')
            return ''






if __name__ == '__main__':

    ex = Exchange()
    #ex.gen_exchange()
    ex.load_exchange()

    print(ex.get_exchange('ACN'))
    print(ex.get_exchange('AAPL'))

    print(ex.get_sector('ACN'))
    print(ex.get_sector('AAPL'))
    #df = ex.exchg
    #print(df.head())
    #df['Symbol']




