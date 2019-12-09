import requests
from IPython.core.display import HTML
from bs4 import BeautifulSoup
from dateutil import parser
import bs4
import pandas as pd
import numpy as np
from fastnumbers import isfloat 
from fastnumbers import fast_float
from datetime import datetime
from urllib.request import urlopen


class HistDataReader:

    def __init__(self):
        self.baseUrl = 'https://markets.ft.com/data/funds/tearsheet/historical?s='
   
    def GetHistData(self, isin, curr):
        url = self.baseUrl + isin + ':' + curr
        data = urlopen(url).read()
        content = BeautifulSoup(data, 'html.parser')
        #HTML(str(content))
        hist = content.find("div",attrs={'class':"mod-app clearfix mod-tearsheet-historical-prices mod-module mod-module--trans"})
        #HTML(str(hist))
        table = hist.find("table",attrs={'class':"mod-ui-table mod-tearsheet-historical-prices__results mod-ui-table--freeze-pane"})
        #HTML(str(table))
        tab = self.GetTable(table)
        df = self.GetHistDf(tab)
        start = df.iloc[0,0]
        end = df.iloc[df.shape[0]-1,0]
        return df, start, end

    def Ffloat(self, str):
        if str is None: return np.nan
        if type(str)==float or type(str)==np.float64: return str
        if type(str)==int or type(str)==np.int64: return str
        return fast_float(str.split(" ")[0].replace(',','').replace('%',''), default=np.nan)

    def Ffloats(self, strs):
        return list(map(Ffloat,strs))

    def RemoveSpaces(self, str):
        if type(str)==str: return ' '.join(str.split())
        return str

    def GetChild(self, content):
        children = list()
        for item in content.children:
            if type(item)==bs4.element.Comment: continue
            if type(item)==bs4.element.Tag or len(str(item).replace("\n","").strip()) > 0 : children.append(item)        
        return children

    def GetTable(self, table,isTag=True):
        elems = table.find_all('tr') if isTag else self.GetChild(table)
        tableData = list()
        for row in elems:       
            rowData = list()
            rowElems = self.GetChild(row)
            for elem in rowElems:
                text = elem.text.strip().replace("\n","")
                text = self.RemoveSpaces(text)
                if len(text)==0: continue
                rowData.append(text)
            tableData.append(rowData)
            df = pd.DataFrame(tableData)
        return df

    def GetDate(self, rawDateStr):
        ds = rawDateStr.split(sep=',')
        dl = ds[-2:]
        y = int(dl[1].strip())
        md = dl[0].split()
        m = datetime.strptime(md[0], '%b').month
        d = int(md[1])
        dt = datetime(y, m, d)
        return dt.strftime('%d/%m/%y') 

    def GetHistDf(self, tab):
        dts = tab.iloc[:,0][1:]
        dts = dts[::-1]
        dts = [self.GetDate(dt) for dt in dts]
        dts
        vals = tab.iloc[:,4][1:]
        vals = vals[::-1] 
        df = pd.DataFrame(dts)
        df = pd.DataFrame({'Date':dts, 'Value':vals})
        return df



if __name__ == '__main__':

    hdr = HistDataReader()
    isin = 'IE0002639668'
    curr = 'USD'
    df, start, end = hdr.GetHistData(isin, curr)
    print(df)
    print(start + ' ' + end)
     