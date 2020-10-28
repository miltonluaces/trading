from os import path
import sys
sys.path.append(path.abspath('D:/source/repos/ProblemSolving/'))

from trading.Funds.FundReader import FundReader


class PortfolioReader:

    def __init__(self):
        self.fr = FundReader()
        self.funds = []

    def AddFund(self, isin, date, shares, val):
        self.funds.append({'isin': isin, 'inv': {'date':'', 'shares':0, 'purchValue':0}, 'act' : {'isin': isin, 'name': '', 'date':'', 'value': 0, 'change': 0, 'currency': ''}})

    def AddFunds(self, isins):
        for isin in isins:
            self.AddFund(isin, '', 0, 0)

    def GetData(self):
        for fund in self.funds:
            data = self.fr.GetData(fund['isin'])
            fund['act'] = data

    def Stats():
        orgTot= 0
        actTot = 0
        for fund in self.funds:
            orgTot = orgTot + fund['inv']['shares'] * fund['inv']['purchValue']
            actTot = actTot + fund['inv']['shares'] * fund['act']['value']
        diff = actTot - orgTot
        relDiff = diff/orgTot
        return orgTot, actTot, diff, relDiff

    def Print(self):
        for fund in self.funds:
            print(fund['act']['name'], fund['act']['value'])


if __name__ == '__main__':

    pr = PortfolioReader()
    pr.AddFunds(['LU0260870158', 'IE0002639668', 'LU0049842262', 'LU0122379950', 'LU0260869739', 'LU0097036916', 'LU0503631714', 'LU0335216932', 'LU0094560744', 'LU0386882277', 'LU0836513001','IE00B530N462', 'LU0243957742', 'LU0050372472', 'LU0366534344', 'LU1548497772', 'LU0011963328', 'LU0087412390', 'LU0072913022','LU1594335520','LU0026741651','ES0173394034', 'LU0048365026', 'DE0008490962','LU0607516092'])
    pr.GetData()
    pr.Print()