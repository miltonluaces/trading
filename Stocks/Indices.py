import numpy as np
import pandas as pd
import investpy
import sys
import datetime
import psycopg2
sys.path.append('D:/source/repos')
from trading.Funds.DBMgr import DBMgr
from ds_topics.utils.time_series import *

class Indices:

    def __init__(self):
        self.dbMgr = DBMgr()
        self.path = 'D:/Invest/Data/stock_lists/sp500_sectors/'
        self.sectors = ['CD', 'CS', 'HC', 'I', 'IT','M', 'RE', 'TS', 'U', 'F', 'E']
        self.Idx = pd.read_csv('D:/Invest/data/indices.csv', encoding = 'ISO-8859-1')
        self.sps = pd.read_csv(self.path + 'sp500_sectors.csv')

    def get_hist(self, index, start, end, interval):
        idex = self.Idx[self.Idx['Index']==index]['Name'].values[0]
        return investpy.get_index_historical_data(index=idex, country='united states', from_date=start, to_date=end, interval=interval)

    def gen_sp500_sectors(self):
        dfs = []
        for sector in self.sectors:
            df = pd.read_csv(self.path + 'sp500' + sector + '.csv')
            df['Sector'] = sector
            dfs.append(df)

        sps = pd.concat(dfs)
        sps = sps[~sps['Symbol'].astype(str).str.startswith('Downloaded')]
        sps.index = sps.Symbol
    
        sps.to_csv(self.path + 'sp500_sectors.csv')
        return sps
    
    def load_sector(self):
        self.sps = pd.read_csv(self.path + 'sp500_sectors.csv')
        self.sps.index = self.sps['Symbol']

    def get_sector(self, ticker):
        try:
            return self.sps[self.sps['Symbol']==ticker]['Sector'].values[0]
        except:
            print (ticker, 'sector not found')
            return ''

    def gen_index_bdts(self, ticker, start, end):
        df = self.get_hist(index=ticker, start=start, end=end, interval='Daily')
        dts = list(df.index.values)
        dts = [pd.to_datetime(dt).date() for dt in dts]
        startdate = str(dts[0].strftime('%d/%m/%Y'))
        enddate = str(dts[len(dts)-1].strftime('%d/%m/%Y'))
        bdts = serialize_dates(dts)
        return startdate, enddate, dts, bdts

    def update_index_dts(self, table, ticker, starthist, endhist, dts):
        starthist = datetime.datetime.strptime(starthist,  '%d/%m/%Y').strftime("%m-%d-%Y")
        endhist = datetime.datetime.strptime(endhist,  '%d/%m/%Y').strftime("%m-%d-%Y")
        query = "UPDATE " + table + " SET starthist = %s, endhist = %s, hist = %s WHERE ticker = %s"
        try:
            self.dbMgr.connect()
            cursor = self.dbMgr.conn.cursor()
            cursor.execute(query, (starthist, endhist, dts, ticker))
            self.dbMgr.conn.commit()
            cursor.close()
            self.dbMgr.close()
        except (Exception, psycopg2.DatabaseError) as error: 
            print(error)


if __name__ == '__main__':

    idx = Indices()
    dbMgr = DBMgr()

    #idx.gen_sp500_sectors()
    
    start = '01/01/2020'
    end = '18/11/2020'
    ticker = 'sp500'
    
    #startdate, enddate, dts, bdts = idx.gen_index_bdts(ticker=ticker, start=start, end=end)
    #print(startdate, enddate)
    #print(dts[0:5])

    #dbMgr.UpdateDts('index', ticker='us_dates', startdts=startdate, enddts=enddate, bdts=bdts)

    startDts, dts = dbMgr.GetDts('index', 'us_dates')
    #print(startDts)
    #print('dts len ', len(dts))
    #print(dts[0])
    #print(dts[len(dts)-1])

    #df = idx.get_hist(index=ticker, start=start, end=end, interval='Daily')
    #print(df.shape[0])
    #print(df.head())
    #print(df.tail())

    #hist_ts = df['High']
    #print('lenght ', hist_ts.shape[0])
    #print(hist_ts.head())
    #print(hist_ts.tail())
    

    #dbMgr = DBMgr()
    #dbMgr.UpdateHist('index', ticker, start, end, hist_ts)

    hist_ts = idx.dbMgr.GetHist('index', ticker)
    print(type(hist_ts))
    #hist_ts.index = dts
    print('hist ', hist_ts.shape)
    print(hist_ts.head())
    print(hist_ts.tail())
    print(hist_ts.index)

    #sps = idx.get_sp500_sectors()
    #print(sps)

    #print(sps[sps['Symbol']=='AMZN']['Sector'])

    #idx.load_sector()
    #print(idx.get_sector(ticker = 'AMZN'))

    #startdate, enddate, bdts = idx.gen_index_bdts('sp500')
    #print(startdate, enddate, bdts[0:50])

    #idx.update_index_dts('index', 'us_dates', startdate, enddate, bdts)

    #dts = idx.dbMgr.GetHist('index', 'us_dates')
    #print(dts)