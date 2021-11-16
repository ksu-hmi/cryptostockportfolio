import json
from tkinter.constants import FALSE
import requests

def get_price(coin, curr='USD'):
    #Get the data on a user specified coin from the cryptocompare website API
    
    fmt = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms={}&api_key=4120b66bee53ddad00260553cac1215997407f8b2abbdcb714c55a7f3240ed27'

    try:
        r = requests.get(fmt.format(coin, curr))
    except requests.exceptions.RequestException:
        sys.exit('Could not complete request')

    try:
        data_raw = r.json()['RAW']
        return [(float(data_raw[c][curr]['PRICE'])) for c in coin.split(',') if c in data_raw.keys()]
          
    except:
        sys.exit('Could not parse data')

def portfolio_add():
    #add user specified crypto to portfolio

    coin_add = input("Enter crypto symbol to add to portfolio (E.G. BTC), Q to go back: ").upper()
    if coin_add.upper() == "Q":
        return
    while coin_add in crypto_dict:
        print(coin_add, "already exists in portfolio.")
        coin_add = input("Enter crypto symbol to add to portfolio (E.G. BTC), Q to go back: ").upper()
        if coin_add.upper() == "Q":
            return
   
    amount_add = input("Enter amount held for " + coin_add + " , Q to go back: ")
    if amount_add.upper() == "Q":
        return
    while amount_add.isdigit() == FALSE:
        print("Invalid entry")
        amount_add = input("Enter amount held for " + coin_add + " , Q to go back: ")
        if coin_amount.upper() == "Q":
            return
   
    crypto_dict[coin_add] = amount_add



def portfolio_remove():
    #remove user specified crypto from portfolio

    coin_remove = input("Enter crypto symbol to remove from portfolio (E.G. BTC), Q to go back: ").upper()
    if coin_remove.upper() == "Q":
        return
    while coin_remove not in crypto_dict:
        print(coin_remove, "not found in portfolio.")
        coin_remove = input("Enter crypto symbol to remove from portfolio (E.G. BTC), Q to go back: ").upper()
        if coin_remove.upper() == "Q":
            return
    del crypto_dict[coin_remove]

def portfolio_update():
    #update amount held of user specified crypto in portfolio

    coin_update = input("Enter crypto symbol to update amount held, Q to go back: ").upper()
    if coin_update.upper() == "Q":
        return
    while coin_update not in crypto_dict:
        print(coin_update, "not found in portfolio.")
        coin_update = input("Enter crypto symbol to update amount held (E.G. BTC), Q to go back: ").upper()
        if coin_update.upper() == "Q":
            return

    coin_amount = input("Enter amount held for " + coin_update + " , Q to go back: ")
    if coin_amount.upper() == "Q":
        return
    while coin_amount.isdigit() == FALSE:
        print("Invalid entry")
        coin_amount = input("Enter amount held for " + coin_update + " , Q to go back: ")
        if coin_amount.upper() == "Q":
            return

    crypto_dict[coin_update] = coin_amount


#example call to print the price of Bitcoin (symbol BTC)
#print(get_price('BTC,ETH'))

#main menu functions, testing the calls
crypto_dict = {"BTC":2}
print(crypto_dict)
portfolio_add()
print(crypto_dict)
portfolio_remove()
print(crypto_dict)
portfolio_update()
print(crypto_dict)

#testing potential crypto porfolio display code
#for lineitem in crypto_dict:
#    print(crypto_dict[lineitem])


