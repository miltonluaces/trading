import pandas as pd
import investpy

class Indices:

    def __init__(self):
        self.Idx = pd.read_csv('D:/Invest/data/indices.csv', encoding = 'ISO-8859-1')

    def get_hist(self, index, start, end, interval):
        idex = self.Idx[self.Idx['Index']==index]['Name'].values[0]
        return investpy.get_index_historical_data(index=idex, country='united states', from_date=start, to_date=end, interval=interval)



if __name__ == '__main__':

    idx = Indices()
    df = idx.get_hist(index='sp500re', start='01/01/2020', end='01/11/2020', interval='Daily')
    print(df.shape[0])
    print(df.head())