import pandas as pd 
import codecs


def GenR4csv(path, filename):
    f = codecs.open(path + filename + '.txt','r', 'utf-8') 
    Rows = []
    #i=1
    while True:
        #i=i+1
        row = f.readline()
        row = row.replace('\r\n', '')
        if row == '':
            row = f.readline()
            row = row.replace('\r\n', '')
        if not row: break
        #if i==50: break
        rest = f.readline()
        tokens = rest.split(sep='\t')
        row = [row] + tokens[:-1]
        Rows.append(row)
    f.close() 

    df = pd.DataFrame(Rows)
    df.columns = ['name', 'isin', 'sector', 'cat', 'region', 'comg', 'rent1m', 'rent3m', 'rent6m', 'rcat1m', 'rcat3m', 'rcat6m', 'volat', 'sharpe', 'beta']
    df.to_csv(path + filename + '.csv')
    print(filename + '.csv generated.')


if __name__ == '__main__':

    GenR4csv('D:/Invest/Funds/', 'FundsR4')
    