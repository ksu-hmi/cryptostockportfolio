import json
import requests
from columnar import columnar
import sys
import re
import os

def main_menu():
    while True:
        main_menu_response = input("\nChoose from any of the following options: \nA (Add crypto), R (remove crypto), U (Update crypto), D (Display portfolio), L (Load portfolio), S (Save portfolio) Q (Quit): ")
        if main_menu_response.upper().startswith("A"):
            portfolio_add()
        elif main_menu_response.upper().startswith("R"):
            portfolio_remove()
        elif main_menu_response.upper().startswith("U"):
            portfolio_update()
        elif main_menu_response.upper().startswith("D"):
            portfolio_display()
        elif main_menu_response.upper().startswith("Q"):
            print("Thank you for using the Crypto Portfolio Display App. Have a nice day!")
            exit()
        elif main_menu_response.upper().startswith("S"):
            portfolio_save()
        elif main_menu_response.upper().startswith("L"):
            portfolio_load()
        else:
            print("Invalid response.")

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
    while re.search("[^0-9^.]", amount_add):
        print("Invalid entry")
        amount_add = input("Enter amount held for " + coin_add + " , Q to go back: ")
        if amount_add.upper() == "Q":
            return
   
    crypto_dict[coin_add] = amount_add
    print(str(amount_add), coin_add, "added to portfolio.")

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
    print(coin_remove, "removed from portfolio.")

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
    while re.search("[^0-9^.]", coin_amount):
        print("Invalid entry")
        coin_amount = input("Enter amount held for " + coin_update + " , Q to go back: ")
        if coin_amount.upper() == "Q":
            return

    crypto_dict[coin_update] = coin_amount
    print(coin_update, "updated to", str(coin_amount))

def portfolio_display():
    #displays the entire portfolio with current prices using the columnar module to generate columns

    listofcrypto = []
    
    for lineitem in crypto_dict:
        listofcrypto.append(lineitem)
    listofcrypto_str = ",".join(listofcrypto)

    price_list = get_price(listofcrypto_str)
    price_list_index = 0
    headers = ["Currency", "Price", "Quantity", "Total Value"]
    data = []
    total_portfolio_value = 0

    for lineitem in crypto_dict:
        price = price_list[price_list_index]
        price_list_index += 1
        quantity = crypto_dict[lineitem]
        total_value = price*float(quantity)
        total_portfolio_value += total_value
        data.append([lineitem, "$"+str(price), quantity, "$"+str(total_value)])

    table = columnar(data, headers, no_borders=True)
    print(table)
    print("TOTAL PORTFOLIO VALUE: " + "$" + str(total_portfolio_value))

def portfolio_save():
    #can save multiple portfolios to a single text file (savedportfolios.txt) with identifier tags to distinguish each

    portfolio_name = input("Enter a name for the portfolio (no special characters) type \"Cancel\" to go back: ")
    if portfolio_name.upper() == "CANCEL":
        return
    
    #read in the saved portfolios file or create a new one if it doesn't already exist
    savedportfolios_file = open(os.path.join(sys.path[0], "savedportfolios.txt"), "a+")
    savedportfolios_file.seek(0)
    savedportfolio_contents = savedportfolios_file.read().splitlines()
    savedportfolios_file.close()

    #check if the user selected portfolio name already exists in the file, ask user for overwrite if true
    while ("@Begin" + portfolio_name.upper()) in savedportfolio_contents:
        askforoverwrite =  input(str(portfolio_name) + " portfolio already exists, would you like to overwrite it? (Y/N) Type \"Cancel\" to go back: ")
        if askforoverwrite.upper() == "CANCEL":
            return
        while askforoverwrite[0] not in ("yYnN"):
            print("Invalid response") 
            askforoverwrite =  input(str(portfolio_name) + " portfolio already exists, would you like to overwrite it? (Y/N) Type \"Cancel\" to go back: ")
            if askforoverwrite.upper() == "CANCEL":
                return
            else:
                pass
        
        if askforoverwrite.upper().startswith("Y") == True:
            #Find the index where the existing portfolio to be overwritten is located in the file
            
            saved_portfolio_index = 0
            for line in savedportfolio_contents:
                if line == "@Begin" + portfolio_name.upper():
                    portfolio_index_begin = saved_portfolio_index
                elif line == "@End" + portfolio_name.upper():
                    portfolio_index_end = saved_portfolio_index
                else:
                    pass
                saved_portfolio_index += 1
            
            #Using the index, delete the portion of the file selected to be overwritten and write brand new file (technically not overwriting)
                
            del savedportfolio_contents[portfolio_index_begin:portfolio_index_end+1]  
            savedportfolios_file = open(os.path.join(sys.path[0], "savedportfolios.txt"), "w+")
            for line in savedportfolio_contents:
                savedportfolios_file.writelines(line+"\n")
            savedportfolios_file.close()
            print(portfolio_name, "overwritten")
            break
        else:
            portfolio_name = input("Enter a name for the portfolio (no special characters) type \"Cancel\" to go back: ")
            if portfolio_name.upper() == "CANCEL":
                return

    #The main part of the save function which appends the new user created portfolio to the existing text file
    savedportfolios_file = open(os.path.join(sys.path[0], "savedportfolios.txt"), "a+")
    savedportfolios_file.writelines("@Begin" + portfolio_name.upper() + "\n")

    for lineitem in crypto_dict:
        savedportfolios_file.writelines(lineitem + " " + crypto_dict[lineitem] + "\n")

    savedportfolios_file.writelines("@End" + portfolio_name.upper() + "\n")
    savedportfolios_file.close()



print("Welcome to the Crypto Portfolio Display App")

crypto_dict = {}

main_menu()

#print(sys.path[0])





