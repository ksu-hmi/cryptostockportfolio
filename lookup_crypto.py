#import requests
#import json

#import os
#os.system('cls')

#api_request = requests.get("a6e2a4fb-fc21-43cc-8157-3f2f0eb1f6e9")
#api = json.loads(api_request.content)

#print(api)

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

import datetime
from datetime import date, timedelta

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'a6e2a4fb-fc21-43cc-8157-3f2f0eb1f6e9',
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    #print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
   print(e)

currencies = ['BTC','XRP','LUNA','SHIB','ETH','VET','ADA','CHZ','FET','MATIC']

for x in data:
    for coin in currencies:
        if coin == x['symbol']:
            print(x['name'])
        
            print("${0:.2f}".format(float(x['price'])))
            print("Circulating Supply: {0:.2f}".format(float(x['circulating_supply'])))
            print("Total Supply: {0:.2f}".format(float(x['total_supply'])))
            print("Rank: {0:.0f}".format(float(x['cmc_rank'])))
