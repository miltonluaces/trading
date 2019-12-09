from os import path
import sys
sys.path.append(path.abspath('D:/source/repos/ProblemSolving/'))

from Trading.Funds.FundReader import FundReader
from Trading.Funds.DBMgr import DBMgr


if __name__ == '__main__':

    # Initialize
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    fr = FundReader()
    dbMgr = DBMgr()

    # Funds
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    isin = 'IE00B29M2H10'

    fund ={ 'isin': isin, 
            'name': 'Robeco Global Fintech', 
            'asset' : 'F',
            'currency': 'EUR', 
            'market': 'GL', 
            'type': 'RV', 
            'sector': 'Tech',
            'size': 'Big', 
            'volatility':  0, 
            'risk': 2, 
            'ogc': 0.94, 
            'manager': 'BNY Mellon',
            'broker': 'Openbank' } 
    
    #dbMgr.AddFund(fund)

    #url = fr.GetUrl(isin)
    #dbMgr.UpdateUrl(isin,  url)


    # Invest
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------


    inv = {'isin': isin,
          'shares': 1027.6,  
          'purchValue' : 2.606,
          'portfolioId': 1}

    #dbMgr.AddInvest(inv)

    # Update investment
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    dbMgr.UpdateInv('LU0505655562', 492.72, 4.965)
  
    # Delete investment
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #dbMgr.DeleteFundInvest('LU0048365026')
  