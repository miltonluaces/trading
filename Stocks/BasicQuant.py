import quandl
import matplotlib.pyplot as plt
import yahoo_fin.stock_info as si
from datetime import date, timedelta

shares = [156, 1, 15, 25]
purchase = []
stocks = ['ACN', 'AMZN', 'VOO', 'DPW.DE']
today = date.today()
yesterday = today - timedelta(1)
today = today.strftime('%Y-%m-%d')
yesterday = yesterday.strftime('%Y-%m-%d')

def GetHist():
    for stock in stocks:
        data = si.get_data(stock, start_date='01-09-2018', end_date=today)
        prices = data.iloc[:,2].values
        plt.plot(prices)
        plt.title(stock)
        plt.show()

def PortfolioValue(prnt=True):
    try:
        tot = 0
        for i in range(len(stocks)):
            value = si.get_data(stocks[i], start_date=yesterday, end_date=today).iloc[:,2].values[0]
            amount = shares[i] * value
            tot = tot + amount
            if(prnt):
                print(stocks[i])
                print('Shares : ', '{0:.2f}'.format(shares[i]))
                print('Value  : ', '{0:.2f}'.format(value))
                print('Amount : ', '{0:.2f}'.format(amount))
                print('')

        print('Total : ', '{0:.2f}'.format(tot), '\n')
        return tot
    except(Exception) as error:
            print('Error')

if __name__ == '__main__':

    print('test')

    #PortfolioValue(True)
    #GetHist()

    
    
