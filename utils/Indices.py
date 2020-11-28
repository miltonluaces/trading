import pandas as pd
import investpy

class Indices:

    def __init__(self):
        

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
        sps = sps[~sps['Symbol'].astype(str).str.startswith('Downloaded')]
        sps.index = sps.Symbol
    
        sps.to_csv(self.path + 'sp500_sectors.csv')
        return sps
    
    def load_sector(self):
        self.sps = pd.read_csv(self.path')
        self.sps.index = self.sps['Symbol']

    def get_sector(self, ticker):
        try:
            return self.sps[self.sps['Symbol']==ticker]['Sector'].values[0]
        except:
            print(ticker, 'not found.')

if __name__ == '__main__':

    idx = Indices()
    