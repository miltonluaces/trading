from os import path
import sys
sys.path.append(path.abspath('D:/source/repos/ProblemSolving/'))
import pandas as pd

import sys
import re
from decimal import Decimal
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote, urlsplit
import re
import quandl
import requests 
import yahoo_fin.stock_info as si
from datetime import date, timedelta
from yahoo_fin import options

class FundReader:

    def __init__(self):
        self.baseUrl = 'http://www.morningstar.es/es/funds/'
        self.searchUrl = 'SecuritySearchResults.aspx?search='
        self.valueUrl = '/es/funds/snapshot/snapshot.aspx?id='
        self.today = date.today() - timedelta(3)
        self.yesterday = self.today - timedelta(1)

    def GetData(self, isin):
        url = self.GetUrl(isin)
        return self.GetFundData(url)

    def GetUrl(self, isin):
        data = urlopen(self.baseUrl + self.searchUrl + quote(isin)).read()
        pHtml = BeautifulSoup(data, features="lxml")
        table = pHtml.find_all('table', id='ctl00_MainContent_fundTable')
        fund = table[0].find_all('tr')[1:][0]
        data = fund.find_all('td')
        name = data[0].text
        url = data[0].a.get('href')
        return url[-10:]
    
    def GetFundData(self, url):
        fundUrl = self.baseUrl + self.valueUrl + url
        data = urlopen(fundUrl).read()
        parsed_html = BeautifulSoup(data, features="lxml")
        name = parsed_html.find_all('div', class_='snapshotTitleBox')[0].h1.text
        table = parsed_html.find_all('table', class_='overviewKeyStatsTable')[0]
        for tr in table.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) != 3:
                continue
            if tds[0].text.startswith('VL'):
                date = tds[0].span.text
                (currency, value) = tds[2].text.split()
            if tds[0].text.startswith('Cambio del'):
                change = tds[2].text.strip()
            if tds[0].text.startswith('ISIN'):
                isin = tds[2].text.strip()
        return {'ISIN': isin, 'name': name, 'date': self.dmy2Date(date), 'value': value, 'change': change, 'currency': currency}

    def dmy2Date(self, value):
        return datetime.strptime(value, '%d/%m/%Y').date()

    def GetFundVolatility(self, url):
        try:
            tab = '&tab=2'
            volUrl = self.baseUrl + self.valueUrl + url + tab
            data = urlopen(volUrl).read()
            parsed_html = BeautifulSoup(data, features="lxml")
            volTxt = parsed_html.find_all('table', class_='ratingRiskTable')[0].text
            tokens = volTxt.split()
            try: vol = self.GetFloat(tokens[3].replace('Volatilidad', '').replace('*', ''))
            except(Exception): vol=-1
            #prof = GetFloat(tokens[6].replace('3a*', ''))
            #ratio = GetFloat(tokens[10].replace('Sharpe*', ''))
            prof=-1
            ratio=-1
        except(Exception): vol=-1; prof=-1; ratio = -1; 
        return {'volatility': vol, 'profit': prof, 'ratio': ratio}

    def GetFundPerf(self, url):
        tab = '&tab=1'
        volUrl = self.baseUrl + self.valueUrl + url + tab
        data = urlopen(volUrl).read()
        parsed_html = BeautifulSoup(data, features="lxml")
        annTxt = parsed_html.find_all('table', class_='snapshotTextColor snapshotTextFontStyle snapshotTable returnsCalenderYearTable')[0].text.split()
        per = annTxt[4] #'%13,0525,4328,4012,0214,326,12-0,4311,76+/-'
        cat = annTxt[5] #'Índice-1,58-1,93-0,55-0,40-1,08-0,77-0,45-0,73%'
        rnk = annTxt[12] #'100)2752302434442866'
        acuTbl = parsed_html.find_all('table', class_='snapshotTextColor snapshotTextFontStyle snapshotTable returnsTrailingTable')[0]
        for tr in acuTbl.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) != 3:
                continue
            if tds[0].text.startswith('1 dia'):
                date = tds[0].span.text
                (currency, value) = tds[2].text.split()
            if tds[0].text.startswith('1 semana'):
                change = tds[2].text.strip()
            if tds[0].text.startswith('1 mes'):
                isin = tds[2].text.strip()

        triTxt = parsed_html.find_all('table', class_='snapshotTextColor snapshotTextFontStyle snapshotTable returnsQuarterlyTable')[0]
        print('')

    def GetFundIsinMorning(self, name):
        nameStr = name.replace(' ', '%20')
        #url = self.baseUrl + 'SecuritySearchResults.aspx?search=First%20State%20Global%20Listed%20Infrastructure%20Fund%20Class%20I%20(Accumulation)%20EUR&type='
        url = self.baseUrl + 'SecuritySearchResults.aspx?search=' + nameStr + '&type='
        data = urlopen(url).read()
        html = BeautifulSoup(data, features="lxml")
        isin = html.find_all('td', class_='msDataText searchIsin')[0].text
        return isin

    def GetFundIsin(self, name):
        isinRe = '([A-Z]{2}[A-Z0-9]{9}[0-9]{1})'
        try:
            isinLength =12
            searchUrl = 'https://uk.search.yahoo.com/search?p='
            suffixUrl = '&fr=yfp-t&fp=1&toggle=1&cop=mss&ei=UTF-8'
            nameStr = name.replace(' ', '+')
            url = searchUrl + nameStr + suffixUrl
            data = urlopen(url).read()
            html = BeautifulSoup(data, features="lxml")
            isinTxt = html.find_all('div', class_='compTitle options-toggle')
            i=0
            for n in range(0,5):
                for i in range(len(isinTxt)):
                    isin = re.search(isinRe, isinTxt[i].text)
                    if(isin!=None): return isin.group()
            return 'NN0000000001'
        except:
            return 'NN0000000000'

    def GetFundIsinReq(self, code):
        url = 'https://api.openfigi.com/v1/mapping' 
        headers = {'Content-Type':'text/json', 'X-OPENFIGI-APIKEY':code } 
        payload = '[ {"idType":"ID_ISIN","idValue":"US4592001014"}]' 
        return requests.post(url, data=payload, headers=headers)
    
    def GetStockValue(self, code):
        try:
            value = si.get_live_price(code)
            return value
        except(Exception) as error:
            print(Exception)
    
    def GetOptionValue(self, ticker, date, strike, type='calls'):
        try:
            chain = options.get_options_chain(ticker, date)[type]
            return (float)(chain[chain['Strike']==strike]['Last Price'])
        except(Exception) as error:
            print(Exception)

    def GetFloat(self, str):
        return eval(str.replace(',','.'))

    def GetFundsDf(self, file):
        monitor = pd.read_excel(file)
        monitor.columns = ['none', 'fund_buy_isin', 'fund_buy_curr', 'fund_sell_isin', 'fund_sell_curr', 'none', 'stock_buy', 'stock_sell']
        monitor = monitor[2:]
        monitor = monitor.drop(['none'], axis=1)
        return monitor

if __name__ == '__main__':
    
    fr = FundReader()
    #url = fr.GetUrl('LU1684797787')
    #print(url)
    #data = fr.GetData('LU0329931090')
    #print('Value : ', data['value'])
    #print('Change : ', data['change'])
    #data = fr.GetFundData('F00000YCN2')
    #print('Name : ', data['name'])
    #print('Value : ', data['value'])
    #print('Change : ', data['change'])
    
    #data = fr.GetFundVolatility(url)
    #print('Volatility: ', data['volatility'])
    #print('Profit : ', data['profit'])
    #print('Ratio : ', data['ratio'])
    
    #data = fr.GetFundPerf(url)

    #isin = fr.GetFundIsin('Allianz Global Investors Fund - Allianz China Equity A EUR'); print(isin)
    #isin = fr.GetFundIsinReq('MSEQX'); print(isin)
    #value = si.get_data(code, start_date=self.yesterday, end_date=self.today).iloc[:,2].values[0]
    #value = fr.GetStockValue('AMZN')
    #value = fr.GetStockValue('AMZN')
    #print(value)
    #dbMgr = DBMgr()
    #names = dbMgr.QueryStr("select name from openfunds2")
    #for i in range(len(names.values)):
    #    name = names.values[i][0]
    #    name= name.replace(' ', '-')
    #    isin = fr.GetFundIsin('https://www.openbank.es/fondo-inversion/' + name + '-')
    #    dbMgr.UpdateOpenIsin(isin, name)
    #    print(isin)

    monitor = fr.GetFundsDf('D:/Invest/Funds/Monitor.xlsx')
    print(monitor)

    

    #po = fr.GetOptionValue('CSCO', "2021-01-15", 47)
    #print(po)