from tkinter import *
import requests
import json
import pprint

#import os
#os.system('cls')

#api_request = requests.get("a6e2a4fb-fc21-43cc-8157-3f2f0eb1f6e9")
#api = json.loads(api_request.content)

#print(api)

#from requests import Session
#from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
#import json
root =Tk()
root.title("Crypto Currency Portfolio")


pprint.pprint("---------------------------------------------------------------")

def lookup():
  api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY=a6e2a4fb-fc21-43cc-8157-3f2f0eb1f6e9&start=1&limit=5000&convert=USD")
  api = json.loads(api_request.content)
  #My Crypto_Portfolio
  
  my_crypto_portfolio =[  
    {
     "sym": "BTC",
     "amount_owned": 100,
     "price_paid_perCoin": 5000
    },
    {
     "sym": "XRP",
     "amount_owned": 20000,
     "price_paid_perCoin": 1.8
    },
    {
     "sym": "LUNA",
     "amount_owned": 100,
     "price_paid_perCoin": 30
    },
    {
     "sym": "SHIB",
     "amount_owned": 100000000,
     "price_paid_perCoin": .000004
    },
    {
     "sym": "ETH",
     "amount_owned": 100,
     "price_paid_perCoin": 2000
    },
    {
     "sym": "VET",
     "amount_owned": 100000,
     "price_paid_perCoin": .1
    },
    {
     "sym": "ADA",
     "amount_owned": 10000,
     "price_paid_perCoin": 1.5
    },
    {
     "sym": "CHZ",
     "amount_owned": 10000,
     "price_paid_perCoin": .5
    },
    {
     "sym": "FET",
     "amount_owned": 10000,
     "price_paid_perCoin": .75
    },
    {
     "sym": "XLM",
     "amount_owned": 10000,
     "price_paid_perCoin": .3
    }
  ]
  portfolio_profit_loss =0
  row_count =1
  for crypto in api['data']:
      for coin in my_crypto_portfolio:
        if coin["sym"] == crypto["symbol"]:

          #Doing some mathmatical calculations
          total_amountPaid = float(coin["amount_owned"]) * float(coin["price_paid_perCoin"])
          current_value = float(coin["amount_owned"]) * float(crypto["quote"]["USD"]["price"])
          profit_loss = current_value - total_amountPaid
          portfolio_profit_loss += profit_loss
          profit_loss_perCoin = float(crypto["quote"]["USD"]["price"])- float(coin["price_paid_perCoin"])

          pprint.pprint(crypto["symbol"])
          pprint.pprint(crypto["name"])
          pprint.pprint(" Current Price: ${0:.2f}".format(float(crypto["quote"]["USD"]["price"])))
          pprint.pprint(" Profit/Loss Per Coin: ${0:2f}".format(float(profit_loss_perCoin)))
          pprint.pprint(" Circulating Supply: {0:.2f}".format(float(crypto["circulating_supply"])))
          pprint.pprint(" Total Supply: {0:.2f}".format(float(crypto["total_supply"])))
          pprint.pprint(" Rank: {0:.0f}".format(float(crypto["cmc_rank"])))
          pprint.pprint("------------------------------------------------------------")
          #-------------------Note: I can also do this with a loop-------
          name = Label(root, text=crypto["name"], bg="white")
          name.grid(row=row_count, column=0, sticky =N+S+W)

          rank = Label(root, text=crypto["cmc_rank"], bg="silver")
          rank.grid(row=row_count, column=1, sticky =N+S+W)

          current_price_perCoin = Label(root, text="${0:2f}".format(float(crypto["quote"]["USD"]["price"])), bg="white")
          current_price_perCoin.grid(row=row_count, column=2, sticky =N+S+W)

          price_paid_perCoin = Label(root, text="${0:2f}".format(float(coin["price_paid_perCoin"])), bg="silver")
          price_paid_perCoin.grid(row=row_count, column=3, sticky =N+S+W)

          profit_loss_perCoin = Label(root, text="${0:2f}".format(float(profit_loss_perCoin)), bg="white")
          profit_loss_perCoin.grid(row=row_count, column=4, sticky =N+S+W)

          one_hr_change = Label(root, text="{0:2f}%".format(float(crypto["percent_change_1hr"])), bg="silver")
          one_hr_change.grid(row=row_count, column=5, sticky =N+S+W)

          twenty4_hr_change = Label(root, text="{0:2f}%".format(float(crypto["percent_change_24h"])), bg="white")
          twenty4_hr_change.grid(row=row_count, column=6, sticky =N+S+W)

          seven_day_change = Label(root, text="{0:2f}%".format(float(crypto["percent_change_7d"])), bg="silver")
          seven_day_change.grid(row=row_count, column=7, sticky =N+S+W)

          current_value = Label(root, text="${0:2f}".format(float(current_value)), bg="white")
          current_value.grid(row=row_count, column=8, sticky =N+S+W)

          profit_loss_total = Label(root, text="${0:2f}".format(float(profit_loss)), bg="silver")
          profit_loss_total.grid(row=row_count, column=9, sticky =N+S+W)

          row_count +=1

  pprint.pprint("Portfolio Profit/Loss: ${0:2f}".format(float(portfolio_profit_loss)))

root.mainloop()
lookup()