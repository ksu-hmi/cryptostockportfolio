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

#declare figure
fig = go.Figure()

#Candlestick
fig.add_trace(go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'], name = 'market data'))

# Add titles
fig.update_layout(
    title='Uber live share price evolution',
    yaxis_title='Stock Price (USD per Shares)')

# X-Axes
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=15, label="15m", step="minute", stepmode="backward"),
            dict(count=45, label="45m", step="minute", stepmode="backward"),
            dict(count=1, label="HTD", step="hour", stepmode="todate"),
            dict(count=3, label="3h", step="hour", stepmode="backward"),
            dict(step="all")
        ])
    )
)

#Show
fig.show()


def main_menu():
    #The home screen, by default the program always returns here

    while True:
        quote = input("Enter Stock holdings quotes or 'Q' to quit")
        if quote.isalpha():
            data = yf.download(tickers = "quote", period='5d', interval='5m')
        elif quote == 'Q':
            break
        else:
            print("Please enter a valid stock quote")
    print(data)
