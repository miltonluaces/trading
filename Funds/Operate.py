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

    isin = 'LU0996182563'

    fund ={ 'isin': 'LU0996182563', 
            'name': 'Amundi Index MSCI World AE-C', 
            'asset' : 'F',
            'currency': 'EUR', 
            'market': 'WO', 
            'type': 'RV', 
            'sector': 'All',
            'size': 'Big', 
            'volatility':  0, 
            'risk': 2, 
            'ogc': 0.3, 
            'manager': 'Amundi',
            'broker': 'CC' } 
    
    #dbMgr.AddFund(fund)

    url = fr.GetUrl(isin)
    #dbMgr.UpdateUrl(isin,  url)


    # Invest
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    isin = 'LU0996182563'

    inv = {'isin': isin,
          'shares': 17.3,  
          'purchValue' : 173.39,
          'portfolioId': 1}

    dbMgr.AddInvest(inv)

    # Update investment
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #dbMgr.UpdateInv('LU0171310443', 155.14, 32.23)
  
    # Delete investment
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #dbMgr.DeleteFundInvest('LU0048365026')
  