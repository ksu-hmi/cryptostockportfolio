# Raw Package
import numpy as np
import pandas as pd

#Data Source
import yfinance as yf

#Data viz
import plotly.graph_objs as go

#Interval required 5 minutes
data = yf.download(tickers='UBER', period='5d', interval='5m')
#Print data
print(data)
