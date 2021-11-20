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