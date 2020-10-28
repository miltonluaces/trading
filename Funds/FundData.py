from os import path
import sys
sys.path.append(path.abspath('D:/source/repos/ProblemSolving/'))
import numpy as np
import pandas as pd
import PyPDF2
from six.moves.urllib.request import urlopen
import io
from tika import parser
from trading.Funds.DBMgr import DBMgr
import psycopg2
import requests

class FundData:

    def __init__(self, isin):
        self.path ='D:\\data\\csv\\funds\\pdf\\'
        self.isin = isin
        self.name = ''
        self.acufun = []; self.acuidx = []; self.acucat = []
        self.anufun = []; self.anuidx = []; self.anucat = []
        self.stafun = []; self.staidx = []; self.starat = [] 

    def Parse(self):
        raw = parser.from_file(self.path + self.isin + '.pdf')
        avisoLegal = raw['content'].find('Aviso Legal')
        text = raw['content'][: avisoLegal]
        text = '\n'.join([line.rstrip() for line in text.splitlines() if line.strip()])
        return text

    def LoadData(self):
        text = self.Parse()
        text = text.replace('%', '')
        
        self.name = text.splitlines()[0]

        acu = text.find('Rentabilidad Acumulada')
        anu = text.find('Rentabilidad Anualizada')
        sta = text.find('Estadísticas')
        igr = text.find('Información General')

        acuTable = text[acu:anu].replace(',','.').splitlines()[4:]
        self.acufun = self.Strs2Floats(acuTable[0].split()[1:])
        self.acuidx = self.Strs2Floats(acuTable[1].split()[1:])
        self.acucat = self.Strs2Floats(acuTable[2].split()[2:])

        anuTable = text[anu:sta].replace(',','.').splitlines()[2:]
        self.anufun = self.Strs2Floats(anuTable[0].split()[1:])
        self.anuidx = self.Strs2Floats(anuTable[1].split()[1:])
        self.anucat = self.Strs2Floats(anuTable[2].split()[2:])
    
        staTable = text[sta:igr].replace(',','.').splitlines()[3:]
        self.stafun = self.Strs2Floats(staTable[0].split()[1:])
        self.staidx = self.Strs2Floats(staTable[1].split()[1:])
        self.starat = self.Strs2Floats(staTable[2].split())

    def SavePdf(self):
        url = 'https://pi.bnpparibas.es/pdf/fondos-fichas/'+ self.isin + '.pdf'
        response = requests.get(url)
        with open(self.path + isin + '.pdf', 'wb') as f:
            f.write(response.content)

    def Strs2Floats(self, strs):
        return [float(str) for str in strs]

    #name': '', 'startdate': '', 'enddate': '', 'currency': '', 'type': '', 'transfer': '', 'dividends': 0,  'mininvest': 0, 'ocf': 0, 'suscr': 0, 'refund': 0,
        
if __name__ == '__main__':

    #fd = FundData('LU0102827648')
    #fd.LoadData()
    #print(fd.acufun)
    #print(fd.acuidx)
    #print(fd.acucat)
    #print(fd.anufun)
    #print(fd.anuidx)
    #print(fd.anucat)
    #print(fd.stafun)
    #print(fd.staidx)
    #print(fd.starat)


    #dbMgr = DBMgr()
    #dbMgr.AddFundData(fd)
    
    db = DBMgr()
    path = 'D:/data/csv/funds/'
    ccf = pd.read_csv(path + 'CConsFunds.csv')
    isins = ccf['isin']

    print('\nSave PDFs\n')
    for isin in isins:
        try:
            fd = FundData(isin)
            fd.SavePdf()
        except (Exception, psycopg2.DatabaseError) as error: 
            print('Error : ' + isin)
    
    print('\nSave data in DB\n')
    for isin in isins:
        try:
            fd = FundData(isin)
            fd.LoadData()
            db.AddFundData(fd)
            print(isin)
        except (Exception, psycopg2.DatabaseError) as error: 
            print('Error : ' + isin)
   
    