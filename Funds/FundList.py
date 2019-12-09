import numpy as np
import pandas as pd
from Trading.Funds.FundReader import FundReader

if __name__ == '__main__':

    path ='D:\\data\\csv\\morningstar\\'
    data = pd.read_csv(path + 'funds1' + '.txt', sep="\t|,", engine='python').replace('\"','')
    #print(data)
    #print(data.iloc[0]['isin'])

    fr = FundReader()
    for i in range(data.shape[0]):
        name = data['name'][i]
        isin = fr.GetFundIsin(name)
        data.at[i, 'isin'] = isin
        print(isin, name)


    print('Done')
    data.to_csv(path + 'funds1.csv', encoding='utf-8')