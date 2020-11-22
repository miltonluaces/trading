import sys
import datetime
from dateutil.relativedelta import relativedelta
sys.path.append('D:/source/repos')
from utilities.std_imports import *
from trading.Funds.DBMgr import DBMgr
from trading.Stocks.Indices import Indices
from ds_topics.utils.time_series import *
import yahoo_fin.stock_info as si



def subtract_months(dts, now, months):
    new_date = now - relativedelta(months=months)
    while new_date not in dts:
        new_date = new_date - datetime.timedelta(days=1)
    return new_date

def get_reldiff(ts, prev, now):
    return round(((ts[now]/ts[prev])-1)*100,2)

def get_reldiffs(ts, dates, now):
    return [get_reldiff(ts, date, now) for date in dates]

def idxcat_one_analysis(ts_stk, ts_idx, ts_cat, dts, months):
    now = dts[len(dts)-1]
    dates = [subtract_months(dts, now, m) for m in range(1,7)]
    
    rds_stk = get_reldiffs(ts_stk, dates, now)
    rds_idx = get_reldiffs(ts_idx, dates, now)
    rds_cat = get_reldiffs(ts_cat, dates, now)
    
    df = pd.DataFrame({'stk': rds_stk, 'idx': rds_idx, 'cat': rds_cat})
    df['diff_idx'] = df['stk'] - df['idx']
    df['diff_cat'] = df['stk'] - df['cat']
    return df  


def build_idxcat_row(ticker, ts_stk, ts_idx, ts_cat, dts, months):
    now = dts[len(dts)-1]
    dates = [subtract_months(dts, now, m) for m in range(1,7)]
    
    rds_stk = get_reldiffs(ts_stk, dates, now)
    rds_idx = get_reldiffs(ts_idx, dates, now)
    rds_cat = get_reldiffs(ts_cat, dates, now)
    
    diff_idx = [round(i[0]-i[1],2) for i in zip(rds_stk, rds_idx)] 
    diff_cat = [round(i[0]-i[1],2) for i in zip(rds_stk, rds_cat)] 
    
    row = [*rds_stk, *rds_idx, *rds_cat, * diff_idx, *diff_cat]
    return [ticker, *row]

def build_idxcat_df(rows):
    df = pd.DataFrame(rows)
    df.columns = 'ticker','stk1','stk2','stk3','stk4','stk5','stk6','idx1','idx2','idx3','idx4','idx5','idx6','cat1','cat2','cat3','cat4','cat5','cat6','didx1','didx2','didx3','didx4','didx5','didx6','dcat1','dcat2','dcat3','dcat4','dcat5','dcat6'
    return df   


        

if __name__ == '__main__':

    dbMgr = DBMgr()
    idx = Indices()

    startDts, dts = dbMgr.GetDts('index', 'us_dates')

    amzn = dbMgr.GetHist('stock', ticker='AMZN')
    amzn = amzn.append(pd.Series([3190]))
    amzn.index = dts

    sp500 = dbMgr.GetHist(table='index', ticker='sp500')
    sp500.index = dts

    df_ica = idxcat_one_analysis(ts_stk=amzn, ts_idx=sp500, ts_cat=sp500, dts=dts, months=6)
    print(df_ica)

    row1 = build_idxcat_row(ticker='AMZN', ts_stk=amzn, ts_idx=sp500, ts_cat=sp500, dts=dts, months=6)
    row2 = build_idxcat_row(ticker='GOOG', ts_stk=amzn, ts_idx=sp500, ts_cat=sp500, dts=dts, months=6)
    row3 = build_idxcat_row(ticker='AAPL', ts_stk=amzn, ts_idx=sp500, ts_cat=sp500, dts=dts, months=6)
    rows = [row1, row2, row3]
    df = build_idxcat_df(rows)
    print(df)