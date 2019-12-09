from os import path
import sys
sys.path.append(path.abspath('D:/source/repos/ProblemSolving/'))

from Trading.Funds.DBMgr import DBMgr 
from Trading.Funds.FundReader import FundReader 
from Trading.Funds.PortfolioReader import FundReader 

def AddFunds():
    funds = []
    funds.append({'isin': 'LU0260870158', 'name': 'Franklin Technology Fund A'    , 'currency': 'EUR', 'market': 'US', 'type': 'RV', 'sector': 'Technology'  ,  'size': 'Big' , 'volatility': 12,'risk': 2, 'ogc': 1.81, 'manager': 'Franklin'   , 'broker': 'OpenBank'})
    funds.append({'isin': 'IE0002639668', 'name': 'Vanguard US 500 Stock Index'   , 'currency': 'USD', 'market': 'US', 'type': 'RV', 'sector': 'All'         ,  'size': 'Big' , 'volatility': 11,'risk': 1, 'ogc': 0.25, 'manager': 'Vanguard'   , 'broker': 'CConsors'}) 
    funds.append({'isin': 'LU0049842262', 'name': 'UBS (Lux) Equity - Mid Caps'   , 'currency': 'USD', 'market': 'US', 'type': 'RV', 'sector': 'All'         ,  'size': 'Mid' , 'volatility': 17,'risk': 2, 'ogc': 1.86, 'manager': 'UBS'        , 'broker': 'OpenBank'}) 
    funds.append({'isin': 'LU0122379950', 'name': 'Blackrock GF. World Healthcare', 'currency': 'USD', 'market': 'GL', 'type': 'RV', 'sector': 'Health'      ,  'size': 'Big' , 'volatility':  7,'risk': 1, 'ogc': 1.82, 'manager': 'Blackrock'  , 'broker': 'OpenBank'}) 
    funds.append({'isin': 'LU0260869739', 'name': 'Franklin US Opps Fund A (acc)' , 'currency': 'EUR', 'market': 'US', 'type': 'RV', 'sector': 'All'         ,  'size': 'Big' , 'volatility': 15,'risk': 3, 'ogc': 1.81, 'manager': 'Franklin'   , 'broker': 'OpenBank'})
    funds.append({'isin': 'LU0097036916', 'name': 'Blackrock Global-US Growth A2' , 'currency': 'USD', 'market': 'US', 'type': 'RV' ,'sector': 'All'         ,  'size': 'Big' , 'volatility': 13,'risk': 3, 'ogc': 1.82, 'manager': 'Blackrock'  , 'broker': 'OpenBank'})
    funds.append({'isin': 'LU0503631714', 'name': 'Pictet Global Envirnom. Opp P' , 'currency': 'EUR', 'market': 'GL', 'type': 'RV', 'sector': 'Environment ',  'size': 'Big' , 'volatility': 15,'risk': 2, 'ogc': 2.02, 'manager': 'Pictet'     , 'broker': 'OpenBank'})
    funds.append({'isin': 'LU0335216932', 'name': 'Morgan Stanley Glob Brands AH' , 'currency': 'EUR', 'market': 'US', 'type': 'RV', 'sector': 'Cons&Service',  'size': 'Big' , 'volatility': 10,'risk': 1, 'ogc': 1.68, 'manager': 'MgStanley'  , 'broker': 'OpenBank'}) 
    funds.append({'isin': 'LU0094560744', 'name': 'MFS Meridian Global Equity A1' , 'currency': 'EUR', 'market': 'GL', 'type': 'RV', 'sector': 'All'         ,  'size': 'Big' , 'volatility': 12,'risk': 1, 'ogc': 1.89, 'manager': 'Meridian '  , 'broker': 'OpenBank'}) 
    funds.append({'isin': 'LU0386882277', 'name': 'Pictet Global Megatrend Sel P' , 'currency': 'EUR', 'market': 'GL', 'type': 'RV', 'sector': 'All'         ,  'size': 'Big' , 'volatility': 13,'risk': 1, 'ogc': 2.01, 'manager': 'Pictet'     , 'broker': 'OpenBank'})  
    funds.append({'isin': 'LU0836513001', 'name': 'IShares North Am. Index LU A2' , 'currency': 'USD', 'market': 'US', 'type': 'RV', 'sector': 'All'         ,  'size': 'Big' , 'volatility': 14,'risk': 1, 'ogc': 0.54, 'manager': 'Blackrock'  , 'broker': 'OpenBank'}) 
    funds.append({'isin': 'IE00B530N462', 'name': 'AXA Rosenberg Alpha Trust B'   , 'currency': 'EUR', 'market': 'US', 'type': 'RV', 'sector': 'All'         ,  'size': 'Big' , 'volatility': 14,'risk': 2, 'ogc': 0.88, 'manager': 'AXA Rosem'  , 'broker': 'OpenBank'}) 
    funds.append({'isin': 'LU0243957742', 'name': 'Invesco Pan EU High Income E'  , 'currency': 'EUR', 'market': 'EU', 'type': 'MX', 'sector': 'All'         ,  'size': 'Big' , 'volatility':  6,'risk': 3, 'ogc': 2.11, 'manager': 'Invesco'    , 'broker': 'OpenBank'}) 
    funds.append({'isin': 'LU0050372472', 'name': 'Blackrock Glob Euro Bond A2'   , 'currency': 'EUR', 'market': 'EU', 'type': 'RF', 'sector': 'All'         ,  'size': 'Mid' , 'volatility':  1,'risk': 2, 'ogc': 0.97, 'manager': 'Blackrock'  , 'broker': 'OpenBank'}) 
    funds.append({'isin': 'LU0366534344', 'name': 'Pictet Nutrition P EUR'        , 'currency': 'EUR', 'market': 'GL', 'type': 'RV', 'sector': 'Agriculture' ,  'size': 'Big' , 'volatility': 12,'risk': 1, 'ogc': 2.01, 'manager': 'Pictet'     , 'broker': 'OpenBank'}) 
    funds.append({'isin': 'ES0155844030', 'name': 'Inverbanser FI'                , 'currency': 'EUR', 'market': 'EU', 'type': 'MX', 'sector': 'Finance'     ,  'size': 'Big' , 'volatility':  8,'risk': 2, 'ogc': 0.59, 'manager': 'Inverbanser', 'broker': 'OpenBank'})
    funds.append({'isin': 'LU1548497772', 'name': 'Allianz Gl Artif.Intell. AT'   , 'currency': 'EUR', 'market': 'GL', 'type': 'RV', 'sector': 'Technology'  ,  'size': 'Big' , 'volatility': 11,'risk': 2, 'ogc': 2.08, 'manager': 'Allianz'    , 'broker': 'OpenBank'})
    funds.append({'isin': 'LU0011963328', 'name': 'Aberdeen SICAV Australia A'    , 'currency': 'AUD', 'market': 'AU', 'type': 'RV', 'sector': 'All'         ,  'size': 'Big' , 'volatility': 12,'risk': 1, 'ogc': 1.69, 'manager': 'Aberdeen'   , 'broker': 'CConsors'})  
    funds.append({'isin': 'LU0087412390', 'name': 'DWS Concept DJE Alpha LC'      , 'currency': 'EUR', 'market': 'GL', 'type': 'MX', 'sector': 'All'         ,  'size': 'Big' , 'volatility':  6,'risk': 1, 'ogc': 1.37, 'manager': 'DWS'        , 'broker': 'OpenBank'})  
    funds.append({'isin': 'LU0072913022', 'name': 'UBS (Lux) Greater China P'     , 'currency': 'USD', 'market': 'CH', 'type': 'RV', 'sector': 'All'         ,  'size': 'Big' , 'volatility': 22,'risk': 3, 'ogc': 2.40, 'manager': 'UBS'        , 'broker': 'OpenBank'})  
    funds.append({'isin': 'LU1594335520', 'name': 'Allianz Dyn Multi Str 75 AT'   , 'currency': 'EUR', 'market': 'GL', 'type': 'MX', 'sector': 'All'         ,  'size': 'Big' , 'volatility': 12,'risk': 3, 'ogc': 1.77, 'manager': 'Allianz'    , 'broker': 'OpenBank'}) 
    funds.append({'isin': 'LU0026741651', 'name': 'GAM Multi stock Swiss CHF B'   , 'currency': 'CHF', 'market': 'SW', 'type': 'RV', 'sector': 'All'         ,  'size': 'Big' , 'volatility': 18,'risk': 3, 'ogc': 1.51, 'manager': 'GAM'        , 'broker': 'OpenBank'}) 
    funds.append({'isin': 'ES0173394034', 'name': 'Renta 4 Bolsa R FI'            , 'currency': 'EUR', 'market': 'SP', 'type': 'RV', 'sector': 'All'         ,  'size': 'Big' , 'volatility': 14,'risk': 1, 'ogc': 1.45, 'manager': 'Renta 4'    , 'broker': 'OpenBank'}) 
    funds.append({'isin': 'LU0306632414', 'name': 'St Life Global EU Small Cp A'  , 'currency': 'EUR', 'market': 'EU', 'type': 'RV', 'sector': 'All'         ,  'size': 'Sma' , 'volatility': 19,'risk': 3, 'ogc': 1.90, 'manager': 'Stand Life' , 'broker': 'OpenBank'}) 
    funds.append({'isin': 'LU0048365026', 'name': 'CS Invm 11 Small&Mid Cap EU B' , 'currency': 'EUR', 'market': 'EU', 'type': 'RV', 'sector': 'All'         ,  'size': 'Mid' , 'volatility': 21,'risk': 2, 'ogc': 2.11, 'manager': 'Cred Swisse', 'broker': 'OpenBank'}) 
    funds.append({'isin': 'DE0008490962', 'name': 'DSW Deutschland LC'            , 'currency': 'EUR', 'market': 'GE', 'type': 'RV', 'sector': 'All'         ,  'size': 'Big' , 'volatility': 25,'risk': 3, 'ogc': 1.40, 'manager': 'Detsche DWS', 'broker': 'OpenBank'}) 
    funds.append({'isin': 'LU0607516092', 'name': 'Invesco Japanese Val Disv E'   , 'currency': 'EUR', 'market': 'JP', 'type': 'RV', 'sector': 'All'         ,  'size': 'Big' , 'volatility': 20,'risk': 3, 'ogc': 2.39, 'manager': 'Invesco'    , 'broker': 'OpenBank'})
    funds.append({'isin': 'LU1731833304', 'name': 'Fidelity Glob Short Income A'  , 'currency': 'EUR', 'market': 'GL', 'type': 'RF', 'sector': 'All'         ,  'size': 'Big' , 'volatility': 2.5,'risk': 1, 'ogc': 1.08, 'manager': 'Fidelity'  , 'broker': 'OpenBank'})
    funds.append({'isin': 'LU0267388220', 'name': 'Fidelity Euro Short Term A Ac' , 'currency': 'EUR', 'market': 'EU', 'type': 'RF', 'sector': 'All'         ,  'size': 'Big' , 'volatility':  2, 'risk': 3, 'ogc': 0.71, 'manager': 'Fidelity'  , 'broker': 'OpenBank'})

    dbMgr = DBMgr()
    for fund in funds:   
         dbMgr.AddFund(fund)


def AddInvests():
    invs = []
    invs.append({'isin': 'LU0260870158', 'shares': 180.46, 'purchValue' : 16.62, 'portfolioId': 1})
    invs.append({'isin': 'IE0002639668', 'shares': 169.62, 'purchValue' : 25.29, 'portfolioId': 1})
    invs.append({'isin': 'LU0049842262', 'shares': 1.22,   'purchValue' : 25.29, 'portfolioId': 1})
    invs.append({'isin': 'LU0122379950', 'shares': 81.68,  'purchValue' : 37.13, 'portfolioId': 1})
    invs.append({'isin': 'LU0260869739', 'shares': 137.46, 'purchValue' : 14.55, 'portfolioId': 1})
    invs.append({'isin': 'LU0097036916', 'shares': 116.10, 'purchValue' : 19.02, 'portfolioId': 1})
    invs.append({'isin': 'LU0503631714', 'shares': 7.89,   'purchValue' : 190.11,'portfolioId': 1})
    invs.append({'isin': 'LU0335216932', 'shares': 25.25,  'purchValue' : 79.21, 'portfolioId': 1})
    invs.append({'isin': 'LU0094560744', 'shares': 62.31,  'purchValue' : 32.10, 'portfolioId': 1})
    invs.append({'isin': 'LU0386882277', 'shares': 8.44,   'purchValue' : 236.97,'portfolioId': 1})
    invs.append({'isin': 'LU0836513001', 'shares': 8.79,   'purchValue' : 175.06, 'portfolioId': 1})
    invs.append({'isin': 'IE00B530N462', 'shares': 118.34, 'purchValue' : 16.90, 'portfolioId': 1})
    invs.append({'isin': 'LU0243957742', 'shares': 74.81,  'purchValue' : 20.05, 'portfolioId': 1})
    invs.append({'isin': 'LU0050372472', 'shares': 51.89,  'purchValue' : 28.91, 'portfolioId': 1})
    invs.append({'isin': 'LU0366534344', 'shares': 7.24,   'purchValue' : 207.27,'portfolioId': 1})
    invs.append({'isin': 'LU0267388220', 'shares': 57.46,  'purchValue' : 25.60, 'portfolioId': 1})
    invs.append({'isin': 'LU1731833304', 'shares': 156.21, 'purchValue' : 9.93,  'portfolioId': 1})
    invs.append({'isin': 'LU1548497772', 'shares': 11.37,  'purchValue' : 131.91,'portfolioId': 1})
    invs.append({'isin': 'LU0011963328', 'shares': 54.60,  'purchValue' : 27.25, 'portfolioId': 1})
    invs.append({'isin': 'LU0087412390', 'shares': 16.12,  'purchValue' : 124.07,'portfolioId': 1})
    invs.append({'isin': 'LU0072913022', 'shares': 2.08,   'purchValue' : 363.49,'portfolioId': 1})
    invs.append({'isin': 'LU1594335520', 'shares': 18.79,  'purchValue' : 106.44,'portfolioId': 1})
    invs.append({'isin': 'LU0026741651', 'shares': 2.38,   'purchValue' : 638.77,'portfolioId': 1})
    invs.append({'isin': 'ES0173394034', 'shares': 27.05,  'purchValue' : 36.34, 'portfolioId': 1})
    invs.append({'isin': 'LU0306632414', 'shares': 65.82,  'purchValue' : 30.39, 'portfolioId': 1})
    invs.append({'isin': 'LU0048365026', 'shares': 0.63,   'purchValue' : 3174.60, 'portfolioId': 1})
    invs.append({'isin': 'DE0008490962', 'shares': 12.45,  'purchValue' : 241.04,'portfolioId': 1})
    invs.append({'isin': 'LU0607516092', 'shares': 97.90,  'purchValue' : 20.43 ,'portfolioId': 1})

    dbMgr = DBMgr()
    for inv in invs:   
         dbMgr.AddInvest(inv)


if __name__ == '__main__':

    #AddInvestments()
    dbMgr = DBMgr()
    #fund ={'isin': 'LU0171310443', 'name': 'Blackrock GF World Tech' , 'currency': 'EUR', 'market': 'GL', 'type': 'RV', 'sector': 'Technology'         ,  'size': 'Big' , 'volatility':  0, 'risk': 2, 'ogc': 1.50, 'manager': 'Blackrock'  , 'broker': 'OpenBank'}
    #inv = {'isin': 'LU0171310443', 'shares': 98.24,  'purchValue' : 30.537 ,'portfolioId': 1}
    #dbMgr.AddInvest(inv)

    #stock ={'isin': 'ACN', 'name': 'Accenture Plc.' , 'asset': 'S', 'currency': 'USD', 'market': 'US', 'type': 'RV', 'sector': 'Global'         ,  'size': 'Big' , 'volatility':  0, 'risk': 2, 'ogc': 0, 'manager': ''  , 'broker': 'Accenture'}
    #dbMgr.AddFund(stock)
    #fund ={'isin': 'DPW', 'name': 'Deutch P W' , 'asset': 'S', 'currency': 'EUR', 'market': 'DE', 'type': 'RV', 'sector': 'Global'         ,  'size': 'Big' , 'volatility':  0, 'risk': 2, 'ogc': 0, 'manager': ''  , 'broker': 'IB'}
    #dbMgr.AddFund(stock)
    #stock ={'isin': 'VOO', 'name': 'Vanguard SP500' , 'asset': 'S', 'currency': 'USD', 'market': 'US', 'type': 'RV', 'sector': 'Global'         ,  'size': 'Big' , 'volatility':  0, 'risk': 2, 'ogc': 0, 'manager': 'Vanguard'  , 'broker': 'IB'}
    #dbMgr.AddFund(fund)
    #stock ={'isin': 'AMZN', 'name': 'Amazon' , 'asset': 'S', 'currency': 'USD', 'market': 'US', 'type': 'RV', 'sector': 'Technology'         ,  'size': 'Big' , 'volatility':  0, 'risk': 2, 'ogc': 0, 'manager': ''  , 'broker': 'IB'}
    #dbMgr.AddFund(stock)
    inv = {'isin': 'DPW.DE', 'shares': 25,  'purchValue' : 29.9 ,'portfolioId': 2}
    dbMgr.AddInvest(inv)
    inv = {'isin': 'VOO', 'shares': 15,  'purchValue' : 261.76 ,'portfolioId': 2}
    dbMgr.AddInvest(inv)
    inv = {'isin': 'AMZN', 'shares': 1,  'purchValue' : 1764.41 ,'portfolioId': 2}
    dbMgr.AddInvest(inv)
    inv = {'isin': 'ACN', 'shares': 156,  'purchValue' : 128.60 ,'portfolioId': 2}
    dbMgr.AddInvest(inv)