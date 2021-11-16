import requests
import json

#import os
#os.system('cls')

#api_request = requests.get("a6e2a4fb-fc21-43cc-8157-3f2f0eb1f6e9")
#api = json.loads(api_request.content)

#print(api)

#from requests import Session
#from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
#import json
import pprint

#from datetime import date, timedelta

#url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
#parameters = {
  #'symbol':'BTC,XRP,LUNA,SHIB,ETH,VET,ADA,CHZ,FET,MATIC',
  
  #'convert':'USD'
#}
#headers = {
  #'Accepts': 'application/json',
  #'X-CMC_PRO_API_KEY': 'a6e2a4fb-fc21-43cc-8157-3f2f0eb1f6e9'
#}

#session = Session()
#session.headers.update(headers)

#try:
    #response = session.get(url, params=parameters)
    #data = json.loads(response.content)
    #print(data)
#except (ConnectionError, Timeout, TooManyRedirects) as e:
   #print(e)

#response = session.get(url, params=parameters)
#data = (json.loads(response.text)['data']['2']['quote']['USD'])
#pprint.pprint(data)

#currencies = ['BTC']
#'XRP','LUNA','SHIB','ETH','VET','ADA','CHZ','FET','MATIC']

api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY=a6e2a4fb-fc21-43cc-8157-3f2f0eb1f6e9&start=1&limit=5000&convert=USD")

api = json.loads(api_request.content)

#currencies = ["BTC","XRP","LUNA","SHIB","ETH","VET","ADA","CHZ","FET"]
# My Crypto_Portfolio
my_crypto_portfolio = [  
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
     "price_paid_perCoin": 0.75
   },
   {
     "sym": "XLM",
     "amount_owned": 10000,
     "price_paid_perCoin": .3
   }
]

portfolio_profit_loss = 0

pprint.pprint("---------------------------------------------------------------")

for crypto in api['data']:
    for coin in my_crypto_portfolio:
      if coin["sym"] == crypto["symbol"]:

        #Doin some mathmatical calculations
        total_amountPaid = float(coin["amount_owned"]) * float(coin["price_paid_perCoin"])
        current_value = float(coin["amount_owned"]) * float(crypto["quote"]["USD"]["price"])
        profit_loss = current_value - total_amountPaid
        portfolio_profit_loss += profit_loss
        profit_loss_perCoin = float(crypto["quote"]["USD"]["price"])- float(coin["price_paid_perCoin"])

        pprint.pprint(crypto["symbol"])
        pprint.pprint(crypto["name"])
        #pprint.pprint(crypto["quote"]["USD"]["price"])
        
        pprint.pprint(" Current Price: ${0:.2f}".format(float(crypto["quote"]["USD"]["price"])))
        pprint.pprint(" Profit/Loss Per Coin: ${0:2f}".format(float(profit_loss_perCoin)))
        pprint.pprint(" Circulating Supply: {0:.2f}".format(float(crypto["circulating_supply"])))
        pprint.pprint(" Total Supply: {0:.2f}".format(float(crypto["total_supply"])))
        pprint.pprint(" Rank: {0:.0f}".format(float(crypto["cmc_rank"])))
        pprint.pprint("------------------------------------------------------------")

pprint.pprint("Portfolio Profit/Loss: ${0:2f}".format(float(portfolio_profit_loss)))
