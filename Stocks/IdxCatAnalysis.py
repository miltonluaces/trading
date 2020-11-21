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

def idxcat_analysis(ts_stk, ts_idx, ts_cat, dts, months):
    now = dts[len(dts)-1]
    dates = [subtract_months(dts, now, m) for m in range(1,7)]
    
    rds_stk = get_reldiffs(ts_stk, dates, now)
    rds_idx = get_reldiffs(ts_idx, dates, now)
    rds_cat = get_reldiffs(ts_cat, dates, now)
    
    df = pd.DataFrame({'stk': rds_stk, 'idx': rds_idx, 'cat': rds_cat})
    df['diff_idx'] = df['stk'] - df['idx']
    df['diff_cat'] = df['stk'] - df['cat']
    return df  



if __name__ == '__main__':

    dbMgr = DBMgr()
    idx = Indices()

    startDts, dts = dbMgr.GetDts('index', 'us_dates')

    amzn = idx.dbMgr.GetHist('stock', ticker='AMZN')
    amzn = amzn.append(pd.Series([3190]))
    amzn.index = dts

    sp500 = dbMgr.GetHist(table='index', ticker='sp500')
    sp500.index = dts

    df_ica = idxcat_analysis(ts_stk=amzn, ts_idx=sp500, ts_cat=sp500, dts=dts, months=6)
    print(df_ica)