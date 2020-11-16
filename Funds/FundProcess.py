from os import path
import sys
sys.path.append(path.abspath('D:/source/repos/ProblemSolving/'))

from trading.Funds.DBMgr import DBMgr
from forex_python.converter import CurrencyRates
import psycopg2
import datetime
import requests
from trading.Funds.FundReader import FundReader
from trading.Funds.CurrencyExchange import CurrencyExchange
from trading.Stocks import BasicQuant as bq

def LoadUrls():
    dbMgr = DBMgr()
    isins = dbMgr.GetFundIsins(onlyUrls=True)
    
    fr = FundReader()
    for isin in isins:
        url = fr.GetUrl(isin)
        dbMgr.UpdateUrl(isin, url)
        #print(isin, url)
        
def UpdateFundValues():
    fr = FundReader()
    ce = CurrencyExchange()
    ce.LoadRates('EUR')
    dbMgr = DBMgr()

    print('\nUpdating Fund Values...\n')
    isins, urls = dbMgr.GetFundIsinsUrls()
    for i in range(len(isins)):
        try:
            data = fr.GetFundData(urls[i])
            value = GetFloat(data['value'])
            currency = data['currency']
            change = GetPerc(data['change'])
            if currency == 'EUR': eurValue = value
            else : eurValue = round(value * (1/ce.GetRate(currency)),2)
            dbMgr.UpdateFundValue(isins[i], eurValue, change)
            print(isins[i], value, eurValue)
        except(Exception) as error:
            print('No data for ', isins[i])

def UpdateStockValues():
    fr = FundReader()
    ce = CurrencyExchange()
    ce.LoadRates('EUR')
    dbMgr = DBMgr()

    print('\nUpdating Stock Values...\n')
    codes = dbMgr.GetStockCodes()
    currencies = dbMgr.GetStockCurrencies()
    for i in range(len(codes)):
        try:
            value = fr.GetStockValue(codes[i])
            currency = currencies[codes[i]]
            change = 0
            if currency == 'EUR': eurValue = round(value,2)
            else : eurValue = round(value * (1/ce.GetRate(currency)),2)
            dbMgr.UpdateFundValue(codes[i], eurValue, 0)
            print(codes[i], value, eurValue)
        except(Exception) as error:
            print('No data for ', codes[i])

def UpdateOptionValues():
    fr = FundReader()
    ce = CurrencyExchange()
    ce.LoadRates('EUR')
    dbMgr = DBMgr()

    print('\nUpdating Option Values...\n')
    options = dbMgr.GetOptions()
    for i in range(len(options)):
        try:
            value = fr.GetOptionValue(options[i]['ticker'], str(options[i]['exercise']), options[i]['strike'])
            currency = options[i]['currency']
            change = 0
            if currency == 'EUR': eurValue = round(value,2)
            else : eurValue = round(value * (1/ce.GetRate(currency)),2)
            eurTotValue = eurValue*100
            dbMgr.UpdateOptionValue(options[i]['ticker'], options[i]['exercise'], options[i]['strike'], eurTotValue)
            print(options[i]['ticker'], value, eurTotValue)
        except(Exception) as error:
            print('No data for ', options[i]['ticker'])

def UpdateInvProportion():
     print('\nUpdating Proportions...\n')
     dbMgr = DBMgr()
  
     query = 'UPDATE invest SET proportion = t.proportion FROM \
     (SELECT isin, round(currAmount/totcurramount*1000)/10 AS proportion FROM \
     (SELECT i.isin as isin, round(i.shares * f.value) AS curramount FROM fund AS f INNER JOIN invest AS i ON f.isin = i.isin) AS t1, \
     (SELECT round(sum(shares * f.value)) AS totcurramount FROM fund AS f INNER JOIN invest AS i ON f.isin = i.isin) AS t2) AS t \
     WHERE invest.isin = t.isin;'
     try:
         dbMgr.connect()
         cursor = dbMgr.conn.cursor()
         cursor.execute(query)
         dbMgr.conn.commit()
         cursor.close()
         dbMgr.close()
     except (Exception, psycopg2.DatabaseError) as error: 
         print(error)

def UpdateFundVolatility():
    dbMgr = DBMgr()
    isins, urls = dbMgr.GetFundIsinsUrls()

    fr = FundReader()
    print('\nUpdating Volatilities...\n')
    for i in range(len(isins)):
        data = fr.GetFundVolatility(urls[i])
        dbMgr.UpdateFundVolatility(isins[i], data['volatility'])
        print(isins[i], data['volatility'])

def InsertPerformanceFunds():
    print('\nUpdating Performance Portfolio Funds ...\n')
    dbMgr = DBMgr()
    query = "INSERT INTO performance(date, purchase, current, diff, reldiff, volatility, ogc, change, portfolioId) \
    (SELECT NOW() AS date, purchase, current, current-purchase AS diff, (round(((current-purchase)/purchase)*10000))/100 AS relDiff, volatility, ogc, change, %s FROM \
    (SELECT (round(sum(i.proportion * f.volatility)))/100 AS volatility, round(sum(i.proportion * f.ogc))/100 AS ogc, round(sum(i.proportion * f.change))/100 AS change, round(sum(shares * purchvalue)) AS purchase, round(sum(shares * f.value)) AS current FROM fund AS f INNER JOIN invest AS i ON f.isin = i.isin WHERE portfolioid=%s) AS t1);"

    try:
         dbMgr.connect()
         cursor = dbMgr.conn.cursor()
         cursor.execute(query, (1, 1))
         dbMgr.conn.commit()
         cursor.close()
         dbMgr.close()
    except (Exception, psycopg2.DatabaseError) as error: 
         print(error)

def InsertPerformanceOptions():
    print('\nUpdating Performance Portfolio Options... \n')
    dbMgr = DBMgr()
    query = "INSERT INTO performance(date, purchase, current, diff, reldiff, volatility, ogc, change, portfolioId) \
SELECT NOW() AS date, sum(purchvalue) AS purchase, sum(currvalue) AS current, sum(currvalue)-sum(purchvalue) AS diff, (round(((sum(currvalue)-sum(purchvalue))/(sum(purchvalue)))*10000))/100 AS relDiff, 0 as volatility, 0 as ogc, 0 as change, 3 as portfolioId FROM option;"

    try:
         dbMgr.connect()
         cursor = dbMgr.conn.cursor()
         cursor.execute(query)
         dbMgr.conn.commit()
         cursor.close()
         dbMgr.close()
    except (Exception, psycopg2.DatabaseError) as error: 
         print(error)

def InsertPerformanceTotal():
    print('\nUpdating Performance Portfolio Total ...\n')
    now = datetime.datetime.now().strftime("%Y/%m/%d")
    dbMgr = DBMgr()
    query = "INSERT INTO performance (date, purchase, current, diff, reldiff, volatility, portfolioId) \
    SELECT date(%s) as date, SUM(purchase) AS purchase, SUM(current) AS current, SUM(diff) AS diff, 0 AS reldiff, 0 as volatility, 0 AS portfolioId FROM performance WHERE date=%s GROUP BY (date) ORDER BY date DESC;"

    try:
         dbMgr.connect()
         cursor = dbMgr.conn.cursor()
         cursor.execute(query, (now, now))
         dbMgr.conn.commit()
         cursor.close()
         dbMgr.close()
    except (Exception, psycopg2.DatabaseError) as error: 
         print(error)

def GetFloat(str):
     return eval(str.replace(',','.'))

def GetPerc(str):
     return eval(str.replace(',','.').replace('%',''))
     
def UpdateValuesDeprecated():
    cc = CurrencyRates()
    Currency = cc.get_rates('EUR')
    dbMgr = DBMgr()
    isins, urls = dbMgr.GetFundIsinsUrls()
     
    fr = FundReader()
    print('\nUpdating Values...\n')
    for i in range(len(isins)):
        try:
            data = fr.GetFundData(urls[i])
            value = GetFloat(data['value'])
            currency = data['currency']
            change = GetPerc(data['change'])
            if currency == 'EUR': eurValue = value
            else : eurValue = round(value * (1/Currency[currency]),2)
            dbMgr.UpdateFundValue(isins[i], eurValue, change)
            print(isins[i], value, eurValue)
        except(Exception) as error:
            print('No data for ', isins[i])
            
def InsertStocksPerformanceDeprecated():
    print('\nUpdating Stocks Performance...\n')
    now = datetime.datetime.now().strftime("%Y/%m/%d")
  
    value = round(bq.PortfolioValue(False),2)
    dbMgr = DBMgr()
    query = 'INSERT INTO performance(date, purchase, current, diff, reldiff, volatility, portfolioId) VALUES(%s, 0, %s, 0, 0, 0, 2)'

    try:
         dbMgr.connect()
         cursor = dbMgr.conn.cursor()
         cursor.execute(query, (now, value))
         dbMgr.conn.commit()
         cursor.close()
         dbMgr.close()
    except (Exception, psycopg2.DatabaseError) as error: 
         print(error)


if __name__ == '__main__':
    
    #LoadUrls()
    #UpdateFundValues()
    #UpdateStockValues()
    #UpdateOptionValues()
    #UpdateFundVolatility()
    #InsertPerformance(1)
    #InsertPerformance(2)
    #InsertPerformanceTotal()
    #cc = CurrencyRates()
    #Currency = cc.get_rates('EUR')
    #print(Currency['USD'])
    InsertPerformanceOptions()
    print('end')