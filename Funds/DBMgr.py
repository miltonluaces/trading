from os import path
import sys
sys.path.append(path.abspath('D:/source/repos/ProblemSolving/'))
sys.path.append(path.abspath('D:/source/repos'))

import psycopg2
import sys, os
import datetime
import numpy as np
import pandas as pd
import pandas.io.sql as psql
from trading.Funds.FundReader import FundReader


class DBMgr:

 

    # Constructor
    def __init__(self):
        self.user = 'postgres'
        self.password = 'ml'
        self.dbName = 'trading'
        self.conn = None
        self.now = datetime.datetime.now().strftime("%Y/%m/%d")


 
    
    # Insert methods
    def AddFund(self, fund):
        query = 'INSERT INTO fund(isin, name, asset, currency, market, type, sector, size, risk, ogc, volatility, manager, broker, update, created, modified) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(query, (fund['isin'], fund['name'], fund['asset'], fund['currency'], fund['market'], fund['type'], fund['sector'], fund['size'], fund['risk'], fund['ogc'], fund['volatility'], fund['manager'], fund['broker'], 'Y', self.now, self.now))
            self.conn.commit()
            cursor.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error: 
            print(error)
    
    def AddStock(self, ticker, name, currency='USD', type='STO', market='', sector='', sp500='N', rs2000='N'):
        query = 'INSERT INTO stock(ticker, name, currency, type, market, sector, sp500, rs2000, value, hist, updvalue, updhist, starthist, endhist, datevalue) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
        try:
            self.connect()
            cursor = self.conn.cursor()
            value = 0
            hist = ''
            updvalue = 'N'
            updhist = 'N'
            starthist = '01/01/2000'
            endhist = '01/01/2000'
            datevalue = '01/01/2000'
            cursor.execute(query, (ticker, name, currency, type, market, sector, sp500, rs2000, value, hist,  updvalue, updhist, starthist, endhist, datevalue))
            self.conn.commit()
            cursor.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error: 
            print(error)
    query = "insert into stock(ticker, name, currency, market, sector, value, broker, trading, type, update, created) values ('DPW.DE', 'Deutch P W', 'EUR', 'INTER', '', 0, 'IB', 'POS', 'STO', 1, now())"
    
    def AddInvest(self, inv):
        query = 'INSERT INTO invest(isin, open, shares, purchValue, portfolioId, created, modified) VALUES(%s, %s, %s, %s, %s, %s, %s);'
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(query, (inv['isin'], self.now, inv['shares'], inv['purchValue'], inv['portfolioId'], self.now, self.now))
            self.conn.commit()
            cursor.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error: 
            print(error)

    def AddPortfolio_Stock(self, ticker, shares, purchValue, trading='SWG', broker='FT'):
        query_ps = "INSERT INTO portfolio_stocks(ticker, shares, purchValue, trading, broker, created, modified) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        query_s = "UPDATE stock SET updValue = %s WHERE ticker = %s"

        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(query_ps, (ticker, shares, purchValue, trading, broker, self.now, self.now))
            cursor.execute(query_s, ('Y', ticker))
            self.conn.commit()
            cursor.close()
            self.close()
            print(ticker, ' added to portfolio.')
        except (Exception, psycopg2.DatabaseError) as error: 
            print(error)


    def AddOperation(self, isinBuy, isinSell, amount, type='T', status='P', comission=0, portfolioId=1):
        queryIns = 'INSERT INTO operation(isinBuy, isinSell, amount, type, comission, portfolioId, status, created, modified) VALUES(%s, %s, %s, %s, %s, %s, %s,  %s, %s);'
        queryUpd = "UPDATE operation SET prevsharesbuy = t1.sharesbuy, postsharesbuy = round((t1.sharesbuy + amount/t1.valuebuy)*100)/100, prevsharessell = t2.sharessell, postsharessell = round((t2.sharessell - amount/t2.valuesell)*100)/100 FROM \
        (SELECT f.value as valuebuy, i.shares AS sharesbuy FROM fund AS f INNER JOIN invest AS i ON f.isin = i.isin WHERE f.isin = %s) AS t1, \
        (SELECT f.value as valuesell, i.shares AS sharessell FROM fund AS f INNER JOIN invest AS i ON f.isin = i.isin WHERE f.isin = %s) AS t2;"
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(queryIns, (isinBuy, isinSell, amount, type, comission, portfolioId, status, self.now, self.now))
            cursor.execute(queryUpd, (isinBuy, isinSell))
            self.conn.commit()
            cursor.close()
            self.close()


        except (Exception, psycopg2.DatabaseError) as error: 
            print(error)

    def AddPLOperation(self, isin, shares, purchValue, currValue, currency, asset):
        query = 'INSERT INTO operation(date, type, isin, shares, purchValue, currValue, currency, plcurr, pleur, asset) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
        plcurr = round(shares * (currValue - purchValue), 2)
        pleur =  round(plcurr * currency, 2)
        
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(query, (self.now, 'S', isin, shares, purchValue, currValue, currency, plcurr, pleur, asset))
            self.conn.commit()
            cursor.close()
            self.close()


        except (Exception, psycopg2.DatabaseError) as error: 
            print(error)
  
    # Update methods
    def UpdateUrl(self, isin, url):
           query = 'UPDATE fund SET url = %s WHERE isin = %s'
           try:
                self.connect()
                cursor = self.conn.cursor()
                cursor.execute(query, (url, isin))
                self.conn.commit()
                cursor.close()
                self.close()
           except (Exception, psycopg2.DatabaseError) as error: 
                print(error)

    def UpdateFundValue(self, isin, value, change):
           query = 'UPDATE fund SET value = %s, change = %s WHERE isin = %s'
           try:
                self.connect()
                cursor = self.conn.cursor()
                cursor.execute(query, (value, change, isin))
                self.conn.commit()
                cursor.close()
                self.close()
           except (Exception, psycopg2.DatabaseError) as error: 
                print(error)

    def UpdateStockValue(self, ticker, value):
           query = 'UPDATE stock SET value = %s WHERE ticker = %s'
           try:
                self.connect()
                cursor = self.conn.cursor()
                cursor.execute(query, (value, ticker))
                self.conn.commit()
                cursor.close()
                self.close()
           except (Exception, psycopg2.DatabaseError) as error: 
                print(error)

    def UpdateOptionValue(self, ticker, date, strike, value):
           query = 'UPDATE option SET currvalue = %s WHERE ticker = %s and exercise=%s and strike=%s'
           try:
                self.connect()
                cursor = self.conn.cursor()
                cursor.execute(query, (value, ticker, date, strike))
                self.conn.commit()
                cursor.close()
                self.close()
           except (Exception, psycopg2.DatabaseError) as error: 
                print(error)

    def UpdateInv(self, isin, shares, purchValue):
            queryInv = "UPDATE invest SET shares = %s, purchvalue = %s, modified = NOW() WHERE isin = %s;"
            try:
                self.connect()
                cursor = self.conn.cursor()
                cursor.execute(queryInv, (shares, purchValue, isin))
                self.conn.commit()
                cursor.close()
                self.close()
                print('Invest updated.')
            except (Exception, psycopg2.DatabaseError) as error: 
                print(error)


    def UpdateFundVolatility(self, isin, volatility):
           query = 'UPDATE fund SET volatility = %s WHERE isin = %s'
           try:
                self.connect()
                cursor = self.conn.cursor()
                cursor.execute(query, (volatility, isin))
                self.conn.commit()
                cursor.close()
                self.close()
           except (Exception, psycopg2.DatabaseError) as error: 
                print(error)


    def UpdateInvValue(self, isin, value):
          query = 'UPDATE invest SET currValue = %s WHERE isin = %s'
          try:
                self.connect()
                cursor = self.conn.cursor()
                cursor.execute(query, (value, isin))
                self.conn.commit()
                cursor.close()
                self.close()
          except (Exception, psycopg2.DatabaseError) as error: 
                print(error)

    def UpdateInvOperation(self, isin, shares, amount):
        queryOp = "UPDATE operation SET shares = %s, postsharesbuy = prevsharesbuy + %s, amount = %s, status = 'C', modified = NOW() WHERE isinbuy = %s;"
        queryInv = "UPDATE invest SET shares = shares + %s, purchvalue = round(((shares * purchvalue + %s)/(shares+%s))*100)/100, modified = NOW() WHERE isin = %s;"
        try:
                self.connect()
                cursor = self.conn.cursor()
                cursor.execute(queryOp, (shares, shares, amount, isin))
                cursor.execute(queryInv, (shares, amount, shares, isin))
                self.conn.commit()
                cursor.close()
                self.close()
                print('Invest and Operation updated.')
        except (Exception, psycopg2.DatabaseError) as error: 
                print(error)

    def UpdateOpenIsin(self, isin, name):
           query = 'UPDATE openfunds2 SET isin = %s WHERE name = %s'
           try:
                self.connect()
                cursor = self.conn.cursor()
                cursor.execute(query, (isin, name))
                self.conn.commit()
                cursor.close()
                self.close()
           except (Exception, psycopg2.DatabaseError) as error: 
                print(error)


    # Select methods
    def QueryStr(self, query):
            self.connect()
            res = pd.read_sql(query, self.conn)
            self.close()
            return res

    def Query(self, tableName, filter=None):
        self.connect()
        query = 'SELECT * FROM ' + tableName
        if not filter==None: query = query + ' WHERE ' + filter
        query = query + ';'
        res = pd.read_sql(query, self.conn)
        self.close()
        return res

    def GetInvestIsins(self):
           res = self.QueryStr('SELECT isin from invest')
           invIsins = []
           for i in range(res.shape[0]):
                invIsins.append(res.values[i][0])
           return invIsins

    def GetInvestIsins(self, portfolio):
           res = self.QueryStr('SELECT isin from invest WHERE portfolioId =' + str(portfolio))
           invIsins = []
           for i in range(res.shape[0]):
                invIsins.append(res.values[i][0])
           return invIsins
    
    def GetFcodeCurr(self, isin):
        res = self.QueryStr("SELECT url, currency FROM fund WHERE isin ='" + isin + "'")
        return { 'fcode': res.values[0][0], 'currency': res.values[0][1]}
    
    def GetInvestIsinCurrs(self, portfolio):
           res = self.QueryStr('SELECT i.isin, f.currency f FROM fund AS f INNER JOIN invest AS i ON f.isin = i.isin WHERE portfolioId =' + str(portfolio))
           invIsinCurrs = []
           for i in range(res.shape[0]):
                invIsinCurrs.append([res.values[i][0], res.values[i][1]])
           return invIsinCurrs

    def GetInvestIsinNames(self, portfolio):
           res = self.QueryStr('SELECT i.isin, f.name f FROM fund AS f INNER JOIN invest AS i ON f.isin = i.isin WHERE portfolioId =' + str(portfolio))
           invIsinNames = []
           for i in range(res.shape[0]):
                invIsinNames.append([res.values[i][0], res.values[i][1]])
           return invIsinNames
     
    def GetFundIsins(self, onlyUrls=False):
           query = "SELECT isin FROM fund WHERE asset='F'"
           if onlyUrls: query = query + ' AND url IS NULL'
           res = self.QueryStr(query)
           fundIsins = []
           for i in range(res.shape[0]):
                fundIsins.append(res.values[i][0])
           return fundIsins

    def GetFundIsinsUrls(self, onlyUpd=True):
           query = "SELECT isin, url FROM fund WHERE asset='F'"
           if(onlyUpd): query = query + " AND update = 'Y'"
           res = self.QueryStr(query)
           isins = []
           urls = []
           for i in range(res.shape[0]):
                isins.append(res.values[i][0])
                urls.append(res.values[i][1])
           return isins, urls

    def GetFundDict(self):
           res = self.QueryStr("SELECT isin, url from fund WHERE asset='F'")
           dict = {}
           for i in range(res.shape[0]):
                dict[res.values[i][0]] = res.values[i][1]
           return dict

    def GetFundCurrencyAsset(self, isin):
           query = "SELECT currency, asset FROM fund WHERE isin='" + isin + "'"
           res = self.QueryStr(query)
           if res.shape[0]==0: return { 'currency': 'USD', 'asset': 'O'}   # TODO: review
           return { 'currency': res.values[0][0], 'asset': res.values[0][1]}

    def GetStockCodes(self):
           query = "SELECT isin FROM fund WHERE asset='S'"
           res = self.QueryStr(query)
           stockCodes = []
           for i in range(res.shape[0]):
                stockCodes.append(res.values[i][0])
           return stockCodes
    
    def GetStockCurrencies(self):
           res = self.QueryStr("SELECT isin, currency from fund WHERE asset='S'")
           dict = {}
           for i in range(res.shape[0]):
               dict[res.values[i][0]] = res.values[i][1]
           return dict

    def GetOptions(self):
           query = "SELECT ticker, exercise, strike, currency FROM option"
           res = self.QueryStr(query)
           options = []
           for i in range(res.shape[0]):
                options.append({'ticker':res.values[i][0], 'exercise':res.values[i][1], 'strike':res.values[i][2], 'currency':res.values[i][3]})
           return options
    

    def GetOptionCurrencies(self):
            return None

    def AddFundData(self, fd):
           query = 'INSERT INTO funddata(isin, name, acufun1m, acufun3m, acufun6m, acufun1y, acufun3y, acufun5y, acufunIni,acuidx1m, acuidx3m, acuidx6m, acuidx1y, acuidx3y, acuidx5y, acuidxIni, acucat1m, acucat3m, acucat6m, acucat1y, acucat3y, acucat5y, acucatIni, anufun0, anufun1, anufun2, anufun3, anufun4, anufun5, anuidx0, anuidx1, anuidx2, anuidx3, anuidx4, anuidx5, anucat0, anucat1, anucat2, anucat3, anucat4, anucat5, stafunvol, stafunrat, staidxvol, staidxrat, staratbet, staratinf, created, modified) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
           try:
                self.connect()
                cursor = self.conn.cursor()
                cursor.execute(query, (fd.isin, fd.name, fd.acufun[0],fd.acufun[1],fd.acufun[2],fd.acufun[3],fd.acufun[4],fd.acufun[5],fd.acufun[6], fd.acuidx[0],fd.acuidx[1],fd.acuidx[2],fd.acuidx[3],fd.acuidx[4],fd.acuidx[5],fd.acuidx[6], fd.acucat[0],fd.acucat[1],fd.acucat[2],fd.acucat[3],fd.acucat[4],fd.acucat[5],fd.acucat[6], fd.anufun[0],fd.anufun[1],fd.anufun[2],fd.anufun[3],fd.anufun[4],fd.anufun[5],fd.anuidx[0],fd.anuidx[1],fd.anuidx[2],fd.anuidx[3],fd.anuidx[4],fd.anuidx[5], fd.anucat[0],fd.anucat[1],fd.anucat[2],fd.anucat[3],fd.anucat[4],fd.anucat[5], fd.stafun[0], fd.stafun[1], fd.staidx[0], fd.staidx[1], fd.starat[0], fd.starat[1], self.now, self.now))
                self.conn.commit()
                cursor.close()
                self.close()
           except (Exception, psycopg2.DatabaseError) as error: 
                print(error)


    def GetFundData(self, isin):
           query = 'SELECT * FROM funddata WHERE isin=' + self.isin
           res = self.QueryStr(query)
           print(res.values[0])

    def connect(self):
        self.conn = psycopg2.connect(host="localhost", database=self.dbName, user=self.user, password=self.password, port = 5432)

    def close(self):
        if self.conn is not None: 
            self.conn.close()
  
    #HistData

    def AddHistData(self, isin, name, currency, startdate, enddate, data):
        query = 'INSERT INTO histdata(isin, name, currency, startdate, enddate, data, updated, created, modified) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(query, (isin, name, currency, startdate, enddate, data, 'Y',  self.now, self.now))
            self.conn.commit()
            cursor.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error: 
            print(error)


    def UpdateHistData(self, isin, enddate, data):
        query = 'UPDATE histdata SET enddate = %s, data = %s WHERE isin = %s'
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(query, (enddate, data, isin))
            self.conn.commit()
            cursor.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error: 
            print(error)

    def GetHistData(self, isin):
        query = "SELECT data FROM histdata WHERE isin = '"  + isin + "'"
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(query)
            #res = self.QueryStr(query)
            mview = cursor.fetchone()
            data = str(mview[0],'utf-8')
            return data
        except (Exception, psycopg2.DatabaseError) as error: 
            print(error)

    def DeleteFundInvest(self, isin):
        query = "DELETE FROM invest WHERE isin = '" + isin + "'"
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(query, (isin))
            self.conn.commit()
            cursor.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error: 
            print(error)
        query = "UPDATE fund SET update = 'N' WHERE isin = '" + isin + "'"
        
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(query, (isin))
            self.conn.commit()
            cursor.close()
            self.close()
        except (Exception, psycopg2.DatabaseError) as error: 
            print(error)

    


if __name__ == '__main__':
    
    dbMgr = DBMgr()

    path = 'D:/data/csv/funds/Portfolio/'
    #isin = 'IE0002639668'
    #name = 'Vanguard U.S. 500 Stock Index Fund USD Acc'
    #currency = 'USD'
    #startdate = datetime.datetime(2018, 6, 1)
    #enddate = datetime.datetime(2019, 5, 17)
    #file = open(path + isin + '.csv','rb')
    #data = pd.read_csv(path + isin + '.csv', sep='\t')
    #dbMgr.AddHistData(isin, name, currency, startdate, enddate, bytes(data))

    #data = dbMgr.GetHistData(isin)
    #print(data)
    #res = dbMgr.Query('fund')
    #print(res.shape)

    #fund = {'isin': 'LU1684797787', 'name': 'CS (Lux) High Yield USD Bond B' , 'asset': 'F', 'currency': 'USD', 'market': 'US', 'type': 'RF', 'sector': 'All',  'size': 'Big' , 'volatility':  0, 'risk': 2, 'ogc': 1.86, 'manager': 'CS', 'broker': 'OpenBank'}
    #dbMgr.AddFund(fund)
    #fr = FundReader()
    #url = fr.GetUrl('LU1684797787')
    #dbMgr.UpdateUrl('LU1684797787',  url)

    #inv = {'isin': 'LU1684797787', 'shares': 5.46, 'purchValue' : 317.49, 'portfolioId': 1}
    #dbMgr.AddInvest(inv)
    #dbMgr.Upda#teUrl('LU1684797787',  'mongo')

    #isins, urls = dbMgr.GetFundIsinsUrls()
    #for i in range(len(isins)):
        #print(isins[i], urls[i])

    #dbMgr.UpdateFundValue('LU0260870158',  0.1)
    
    #dbMgr.AddOperation('LU0267388220', 'LU0607516092', 1731.85)
    #dbMgr.AddOperation('IE00B03HCZ61', 'IE00B03HCZ61', 1500)
    #fd = dbMgr.GetFundDict()
    #print(fd['LU1731833304'])
    #print(fd['LU0260870158'])

    #dbMgr.UpdateInvOperation('IE00B03HCZ61', 61.33, 1499.94)

    #isins = dbMgr.GetFundIsins(True)
    #print(isins)

    #codes = dbMgr.GetStockCodes()
    #print(codes)

    #currencies = dbMgr.GetStockCurrencies()
    #print(currencies)

    #iic = dbMgr.GetInvestIsinNames(1)
    #print(iic)
    
    #dbMgr.GetFcodeCurr(isin='IE00B530N462')

    #dbMgr.AddStock(ticker='JETS', name='JETS Global', currency='USD', type='ETF', market='ARCA')

    #dbMgr.AddPortfolio_Stock(ticker='DPW.DE', shares=35, purchValue=29.51, trading='POS', broker='IB')
    #dbMgr.AddPortfolio_Stock(ticker='VOO', shares=10, purchValue=238.95, trading='POS', broker='IB')
    #dbMgr.AddPortfolio_Stock(ticker='AMZN', shares=2, purchValue=1723.34, trading='POS', broker='IB')
    #dbMgr.AddPortfolio_Stock(ticker='ACN', shares=221, purchValue=141.45, trading='POS', broker='MS')
    #dbMgr.AddPortfolio_Stock(ticker='CCL', shares=45, purchValue=22.83, trading='POS', broker='FT')
    #dbMgr.AddPortfolio_Stock(ticker='JETS', shares=140, purchValue=20.77, trading='POS', broker='IB')
    
    

   