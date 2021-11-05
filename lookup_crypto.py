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
  api_request = session.get(url, params=parameters)
  api = json.loads(api_request.content)
  print(api)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

currencies = {'BTC','XRP','LUNA','SHIB','ETH','VET','ADA','CHZ','FET','MATIC'}

for x in api:
    for coin in currencies:
        if coin == int(x['symbol']):
            print(str(x['symbol']))
