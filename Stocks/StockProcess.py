import sys
import yahoo_fin.stock_info as si
import yfinance as yf
import datetime
import psycopg2
sys.path.append('D:/source/repos')
from utilities.std_imports import *
from trading.Funds.DBMgr import DBMgr
from trading.Stocks.exchange import Exchange
from trading.Stocks.Indices import Indices
from trading.Funds.CurrencyExchange import CurrencyExchange

now = datetime.datetime.now().strftime("%Y/%m/%d")

def GetStockTickerCurrencies():
        dbMgr = DBMgr()
        query = "SELECT ticker, currency FROM stock WHERE updValue = 'Y'"
        res = dbMgr.QueryStr(query)
        return list(res['ticker'].values), list(res['currency'].values)

def GetStockValue(ticker):
        try:
            value = si.get_live_price(ticker)
            return value

        except(Exception) as error:
            print(Exception)       

def UpdateStockValues():
    ce = CurrencyExchange()
    ce.LoadRates('EUR')
    dbMgr = DBMgr()

    print('\nUpdating Stock Values...\n')
    tickers, currencies = GetStockTickerCurrencies()
    for i in range(len(tickers)):
        try:
            value = GetStockValue(tickers[i])
            if currencies[i] == 'EUR': eurValue = round(value,2)
            else : eurValue = round(value * (1/ce.GetRate(currencies[i])),2)
            dbMgr.UpdateStockValue(tickers[i], eurValue)
            print(tickers[i], value, eurValue)

        except(Exception) as error:
            print('No data for ', tickers[i])

def GetPortfolioStocks():
    dbMgr = DBMgr()
    query = "SELECT p.ticker AS ticker, s.name AS name, p.shares AS shares, p.purchvalue AS purchvalue, s.value AS currvalue FROM stock AS s INNER JOIN portfolio_stocks AS p ON s.ticker = p.ticker ORDER BY ticker"
    ps = dbMgr.QueryStr(query)
    ps['purchAmount'] = ps['shares'] * ps['purchvalue']
    ps['currAmount'] = ps['shares'] * ps['currvalue']
    ps['diff'] = ps['currAmount'] - ps['purchAmount']
    ps['relDiff'] = round((ps['diff']/ps['purchAmount'])*100,2)
    totCurrAmount = sum(ps['currAmount'])
    ps['prop'] = round((ps['currAmount']/totCurrAmount)*100,2)
    return ps

def GetPortfolioStocksTotals(ps):
    totPurchAmount = round(sum(ps['purchAmount']),2)
    totCurrAmount = round(sum(ps['currAmount']),2)
    totDiff = round(sum(ps['diff']),2)
    totRelDiff = round((totDiff/totPurchAmount * 100),2)
    return {'purchTotal': totPurchAmount , 'currTotal': totCurrAmount, 'diff':totDiff, 'relDiff': totRelDiff}

def InsertPerformanceStocks(ps):
    psTotals = GetPortfolioStocksTotals(ps)
    dbMgr = DBMgr()
    query = "INSERT INTO performance(date, purchase, current, diff, reldiff, volatility, ogc, change, portfolioId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
         dbMgr.connect()
         cursor = dbMgr.conn.cursor()
         cursor.execute(query, (now, psTotals['purchTotal'], psTotals['currTotal'], psTotals['diff'], psTotals['relDiff'], 0, 0, 0, 2))
         dbMgr.conn.commit()
         cursor.close()
         dbMgr.close()

    except (Exception, psycopg2.DatabaseError) as error: 
         print(error)

def AddStocks_SP500():
        dbMgr = DBMgr()
        idx = Indices()
        idx.load_sector()
        ex = Exchange()
        ex.load_exchange()
        
        currency='USD'
        type='STO'
        sp500='Y'
        rs2000='Y'
        

        tickers = si.tickers_sp500()
        for ticker in tickers:
            try:
                stk = yf.Ticker(ticker)
                name = stk.info['longName'][:32]
                market = ex.get_exchange(ticker)
                sector = idx.get_sector(ticker)
                dbMgr.AddStock(ticker=ticker, name=name, market=market, sector=sector)
                print(ticker, ' added.')
            except:
                print('Error in ', ticker)


        print('SP500 stocks added to Database.')

def UpdateStocks_SP500():
        dbMgr = DBMgr()
        idx = Indices()
        idx.load_sector()
        ex = Exchange()
        ex.load_exchange()
        
        currency='USD'
        type='STO'
        sp500='Y'
        rs2000='Y'
        

        tickers = si.tickers_sp500()
        for ticker in tickers:
            try:
                #market = ex.get_exchange(ticker)
                sector = idx.get_sector(ticker)
                dbMgr.UpdateStockColumn(ticker, 'sector', sector)
                print(ticker, ' updated.')
            except:
                print('Error in ', ticker)


        print('SP500 stocks added to Database.')


if __name__ == '__main__':

    #st, curr = GetStockTickerCurrencies()
    #print(st)
    #print(curr)

    #print(GetStockValue('AMZN'))

    #UpdateStockValues()

    #ps = GetPortfolioStocks()
    #print(ps)

    #totals = GetPortfolioStocksTotals(ps)
    #print(totals)
    
    #InsertPerformanceStocks(ps)
    
    #UpdateStocks_SP500()
    start='01/01/2020'
    end='18/11/2020'

    dbMgr = DBMgr()
    idx=Indices()

    ticker = 'AMZN'
    hist_data = si.get_data(ticker=ticker, start_date=start, end_date=end)
    hist_ts = hist_data['high']
    print(hist_ts)

    dbMgr.UpdateHist('Stock', ticker=ticker, starthist=start, endhist=end, hist_ts=hist_ts)

    print('\ndata read\n')
    hist_ts = idx.dbMgr.GetHist('Stock', ticker)
    print(hist_ts)