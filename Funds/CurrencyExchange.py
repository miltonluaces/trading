from os import path
import sys
sys.path.append(path.abspath('D:/source/repos/ProblemSolving/'))

import requests
import datetime

class CurrencyExchange:
    
    def __init__(self):
        self.baseUrl = 'http://data.fixer.io/api/latest?access_key='
        self.now = datetime.datetime.now().strftime("%Y/%m/%d")
        self.apikey = 'd9bb694d1f325deaf333b760235b0d52'
 
    
    def LoadRates(self, base):
        api = self.baseUrl + self.apikey + '&date=' + self.now; data = requests.get(api); jsonData = data.json()
        self.rates = jsonData['rates']
	 
    def GetRate(self, to):
	    return self.rates[to]

    def Eur2Curr(self, curr):
	    return self.rates[curr]

    


if __name__ == '__main__':

    ce = CurrencyExchange()
    ce.LoadRates('EUR')
    print(ce.GetRate('USD'))
    #print(ce.GetRate('EUR', 'USD'))
    #print(ce.GetRate('EUR', 'CHF'))
    #print(ce.Eur2Usd())
    
