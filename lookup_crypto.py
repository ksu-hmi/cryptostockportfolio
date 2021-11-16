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
#import pprint

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

currencies = ["BTC","XRP","LUNA","SHIB","ETH","VET","ADA","CHZ","FET"]


for x in api['data']:
    for coin in currencies:
      if coin == x["symbol"]:
        print(x["symbol"])
        print(x["name"])
        print(x["quote"]["USD"]["price"])
        
        print("${0:.2f}".format(float(x["quote"]["USD"]["price"])))
        print("Circulating Supply: {0:.2f}".format(float(x["circulating_supply"])))
        print("Total Supply: {0:.2f}".format(float(x["total_supply"])))
        print("Rank: {0:.0f}".format(float(x["cmc_rank"])))
