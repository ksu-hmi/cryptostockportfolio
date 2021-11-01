import os
import sys
import re
import shutil
import configparser
import json
import pkg_resources
import locale
import requests
import requests_cache


def get_price(coin, curr='USD'):
    #Get the data on a user specified coin from the cryptocompare website API
    
    fmt = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms={}&api_key=4120b66bee53ddad00260553cac1215997407f8b2abbdcb714c55a7f3240ed27'

    try:
        r = requests.get(fmt.format(coin, curr))
    except requests.exceptions.RequestException:
        sys.exit('Could not complete request')

    try:
        data_raw = r.json()['RAW']
        return [(float(data_raw[c][curr]['PRICE']),
                 float(data_raw[c][curr]['HIGH24HOUR']),
                 float(data_raw[c][curr]['LOW24HOUR'])) for c in coin.split(',') if c in data_raw.keys()]
    except:
        sys.exit('Could not parse data')


#example call to print the price of Bitcoin (symbol BTC)
print(get_price('BTC'))