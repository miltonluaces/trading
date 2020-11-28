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

    