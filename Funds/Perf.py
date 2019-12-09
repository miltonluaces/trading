from os import path
import sys
sys.path.append(path.abspath('D:/source/repos/ProblemSolving/'))

import numpy as np
import pandas as pd
import datetime

class Perf:

    def __init__(self, isin, name=None):
        self.isin = isin
        self.name = name
        
        currYr = datetime.datetime.now().year

        self.annRows = {'rer': 0, 'cat': 1, 'idx' : 2, 'rnk' : 3}
        self.annCols = np.transpose([currYr-7, currYr-6, currYr-5, currYr-4, currYr-3, currYr-2, currYr-1, currYr])

        self.acuRows = { '1d': 0, '1w': 1, '1m': 2, '3m': 3, '6m': 4, '1y': 5, '3y': 6, '5y': 7, '10y': 8 }
        self.acuCols = np.transpose(['per', 'cat', 'idx'])

        self.triRows = { currYr-1:0, currYr-2:1, currYr-3:2, currYr-4:3, currYr-5:4}
        self.triCols = np.transpose([1,2,3,4])

    def LoadData(self, annArr, acuArr, triArr): 
        self.ann = pd.DataFrame(data=annArr, columns=self.annCols, dtype=float)
        self.acu = pd.DataFrame(data=acuArr, columns=self.acuCols, dtype=float)
        self.tri = pd.DataFrame(data=triArr, columns=self.triCols, dtype=float)
    
    def GetAnnVal(self, row, col): return(self.ann[col][self.annRows[row]])
    def GetAnnCol(self, col): return self.ann[col];
    def GetAnnRow(self, row): return(self.ann.iloc[self.annRows[row]])

    def GetAcuVal(self, row, col): return(self.acu[col][self.acuRows[row]])
    def GetAcuCol(self, col): return self.acu[col];
    def GetAcuRow(self, row): return(self.acu.iloc[self.acuRows[row]])

    def GetTriVal(self, row, col): return(self.tri[col][self.triRows[row]])
    def GetTriCol(self, col): return self.tri[col];
    def GetTriRow(self, row): return(self.tri.iloc[self.triRows[row]])



if __name__ == '__main__':

    annArr = [[13.05, 25.43, 28.40, 12.02, 14.32, 6.12, -0.43, -11.76],[2.06, -0.10,2.3,2.5,1.57,0.60,2.09,-0.45],[-1.58,-1.93,-0.55,-0.4,-1.08,-0.77,-0.45,-0.73],[27,52,30,24,34,44,28,66]]
    acuArr = [[-1.22,-2.15,0.07],[-0.38,-1.38,0.07],[0.9,-1.16,0.16],[17.61,1,-0.61],[0.26,-0.84,-0.33],[13.53,-1.63,-0.51],[16.86,2.15,-0.74],[12.1,0.62,-0.96],[14.27,1.48,-0.65],[17.3,1.69,-1.21]]
    triArr = [[-3.25,8.67,8.04,-12.32],[4.38,-3.53,0.59,4.78],[-3.6,4.88,2.45,10.38],[13.51,-3.54,-6.8,9.77],[1.58,5.71,9.38,9.32]]

    pf = Perf('IE0002639668', 'Vanguard US 500 Stock Index USD')
    pf.LoadData(annArr, acuArr, triArr)
     
    print(pf.ann)
    print(pf.acu)
    print(pf.tri)

    print(pf.GetAnnVal('idx', 2016))
    print(pf.GetAnnCol(2016))
    print(pf.GetAnnRow('idx'))

    print(pf.GetAcuVal('1w', 'cat'))
    print(pf.GetTriVal(2015, 2))
