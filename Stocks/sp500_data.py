import sys
import yahoo_fin.stock_info as si
import yfinance as yf
import datetime
sys.path.append('D:/source/repos')
from utilities.std_imports import *
from trading.Funds.DBMgr import DBMgr
from trading.Stocks.exchange import Exchange
from trading.Stocks.Indices import Indices
from trading.Funds.CurrencyExchange import CurrencyExchange
import trading.Stocks.IdxCatAnalysis as ica

now = datetime.datetime.now().strftime("%Y/%m/%d")


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

def UpdateIndices_data(start, end):
    dbMgr = DBMgr()
    idx =  Indices()
    
    resDf = dbMgr.QueryStr('SELECT ticker FROM index')
    tickers = list(resDf['ticker'].values)
    idxs = [t for t in tickers if t.startswith('sp500')]
    
    # dts
    startdate, enddate, dts, bdts = idx.gen_index_bdts(ticker='sp500', start=start, end=end)
    dbMgr.UpdateDts('index', ticker='us_dates', startdts=start, enddts=end, bdts=bdts)
    
    # idxs
    for ticker in idxs:
        df = idx.get_hist(index=ticker, start=start, end=end, interval='Daily')
        dbMgr.UpdateHist(table='index', ticker=ticker, starthist=start, endhist=end, hist_ts=df['High'])
    
    print('SP500 Indices loaded')
    

def UpdateSP500_data(start, end, verbose=False):
    dbMgr = DBMgr()
    end=end+1
    tickers = si.tickers_sp500()
    tickers = [t.replace('.', '-') for t in tickers]
    startDts, dts = dbMgr.GetDts('index', 'us_dates')

    for ticker in tickers:
        try:
            hist = si.get_data(ticker, start_date=start, end_date=end)
            dbMgr.UpdateHist('Stock', ticker=ticker, starthist=start, endhist=end, hist_ts=hist['high'])
            if verbose: print(ticker, ' updated.')
        except:
            print('Error in ', ticker)


def LoadSP500_data():
    dbMgr = DBMgr()
    idx =  Indices()
    
    resDf = dbMgr.QueryStr('SELECT ticker FROM index')
    idx_tickers = list(resDf['ticker'].values)
    idx_tickers = [t for t in idx_tickers if t.startswith('sp500')]
   
    # dates
    startDts, dts = dbMgr.GetDts('index', 'us_dates')

    # indices
    Idxs = dict()
    for ticker in idx_tickers:
        try:
            idx_ts = dbMgr.GetHist(table='index', ticker='sp500')
            idx_ts.index = dts
            Idxs[ticker] = idx_ts
        except:
            print('Cannot load ', ticker)   
    # stocks
    stk_tickers = si.tickers_sp500()
    stk_tickers = [t.replace('.', '-') for t in stk_tickers]
    Stks = dict()
    for ticker in stk_tickers:
        try:
            stk_ts = dbMgr.GetHist('stock', ticker=ticker)
            stk_dts = dts[len(dts)-stk_ts.shape[0]:]
            stk_ts.index = stk_dts
            Stks[ticker] = stk_ts
        except:
            print('Cannot load ', ticker)
    print('SP500 data loaded.')
    return Idxs, Stks


def Gen_Idxcat_analytics(Idxs, Stks, path='D:/Invest/Data/stock_hist/'):
    dts = Idxs['sp500'].index

    Rows = []
    for ticker in Stks.keys():
        try:
            ts_stk = Stks[ticker]
            ts_idx = Idxs['sp500']
            if(ts_stk.shape[0] < 185):
                print(ticker, 'dropped due to short history.')
                continue;
            cat = 'sp500' + idx.get_sector(ticker).lower()
            ts_cat = Idxs[cat]
            months=6
            row = ica.build_idxcat_row(ticker, ts_stk, ts_idx, ts_cat, dts, months)
            Rows.append(row)
        except:
            print('Error in ', ticker)

    df = ica.build_idxcat_df(Rows)
    df.to_csv(path + 'idxcat_analysis.csv')
    print('idx_cat analysis generated.')
    return df




if __name__ == '__main__':

    
    start='01/01/2020'
    end='19/11/2020'

    dbMgr = DBMgr()
    idx=Indices()

    #ticker = 'BF-B'
    #hist_data = si.get_data(ticker=ticker, start_date=start, end_date=end)
    #hist_ts = hist_data['high']
    # print(hist_ts)

    #dbMgr.UpdateHist('Stock', ticker=ticker, starthist=start, endhist=end, hist_ts=hist_ts)

    # print('\ndata read\n')
    #hist_ts = idx.dbMgr.GetHist('Stock', ticker)
    #print(hist_ts.shape)

    #UpdateIndices_data(start, end)
    #UpdateSP500_data(start, end, verbose=True)

    Idxs, Stks = LoadSP500_data()
    Gen_Idxcat_analytics(Idxs, Stks)

