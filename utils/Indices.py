import pandas as pd
import investpy

class Indices:

    def __init__(self):
        self.path = 'D:/Invest/Data/stock_lists/sp500_sectors/'
        self.sectors = ['CD', 'CS', 'HC', 'I', 'IT','M', 'RE', 'TS', 'U', 'F', 'E']
        self.Idx = pd.read_csv('D:/Invest/data/indices.csv', encoding = 'ISO-8859-1')
        self.sps = pd.read_csv(self.path + 'sp500_sectors.csv')

    def get_hist(self, index, start, end, interval):
        idex = self.Idx[self.Idx['Index']==index]['Name'].values[0]
        return investpy.get_index_historical_data(index=idex, country='united states', from_date=start, to_date=end, interval=interval)

    def get_sp500_sectors(self):
        dfs = []
        for sector in self.sectors:
            df = pd.read_csv(self.path + 'sp500' + sector + '.csv')
            df['Sector'] = sector
            dfs.append(df)

        sps = pd.concat(dfs)
        sps.index = sps.Symbol
        sps.to_csv(self.path + 'sp500_sectors.csv')
        return sps
        
    def get_sector(self, ticker):
        return str(self.sps[self.sps['Symbol']==ticker]['Sector'].values[0])

if __name__ == '__main__':

    idx = Indices()
    #df = idx.get_hist(index='sp500re', start='01/01/2020', end='01/11/2020', interval='Daily')
    #print(df.shape[0])
    #print(df.head())

    #idx.sectors = ['CD', 'TS']
    #sps = idx.get_sp500_sectors()
    #print(sps)

    #print(sps[sps['Symbol']=='AMZN']['Sector'])

    print(idx.get_sector(ticker = 'AMZN'))