from os import path
import sys
sys.path.append(path.abspath('D:/source/repos/ProblemSolving/'))
from trading.Funds.FundReader import FundReader
from trading.Funds.DBMgr import DBMgr

dbMgr = DBMgr()



if __name__ == '__main__':

    # Initialize
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    fr = FundReader()
    dbMgr = DBMgr()

    # Funds
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    
    
    #dbMgr.AddFund(fund)

    url = fr.GetUrl(isin)
    #dbMgr.UpdateUrl(isin,  url)


    # Invest
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    

    dbMgr.AddInvest(inv)

    # Update investment
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    