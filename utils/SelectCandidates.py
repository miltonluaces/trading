import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import datetime as dt
import yahoo_fin.stock_info as si
import plotly.graph_objects as go
import plotly.express as px
from pylab import rcParams
rcParams['figure.figsize'] = 20, 15

def PlotIntStock(df, ticker):
    fig = px.line(df, y=ticker, title=ticker)
    fig.update_xaxes(rangeslider_visible=True,rangeselector=dict(
            buttons=list([
                dict(count=15, label="15d", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    fig.show()

if __name__ == '__main__':
    print('Select Candidates\n')