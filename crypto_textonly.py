import json
import requests
from columnar import columnar
import sys
import re
import os

def main_menu():
    #The home screen, by default the program always returns here

    while True:
        main_menu_response = input("\nChoose from any of the following options: \nA (Add crypto), R (Remove crypto), U (Update crypto), D (Display portfolio), L (Load portfolio), S (Save portfolio), N (New portfolio), Q (Quit): ")
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
        elif main_menu_response.upper().startswith("T"):
            top_ten_prices()
        elif main_menu_response.upper().startswith("N"):
            portfolio_new()
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

def does_coin_exist(coin, curr='USD'):
    #Checks whether the crypto currency actually exists using an API call

    fmt = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms={}&api_key=4120b66bee53ddad00260553cac1215997407f8b2abbdcb714c55a7f3240ed27'

    try:
        r = requests.get(fmt.format(coin, curr))
    except requests.exceptions.RequestException:
        sys.exit('Could not complete request')
    
    try:
        data_raw = r.json()
        if 'Message' in data_raw:
            return False
        elif 'PRICE' in data_raw['RAW'][coin][curr]:
            return True
        else:
            pass
    
    except:
        sys.exit('Could not parse data')

def portfolio_add():
    #add user specified crypto to portfolio after checking if the coin actually exists

    coin_add = input("Enter crypto symbol to add to portfolio (E.G. BTC), Q to go back: ").upper()
    if coin_add.upper() == "Q":
        return
    while coin_add in crypto_dict:
        print(coin_add, "already exists in portfolio. Use the Update function in the main menu to change amount held.")
        coin_add = input("Enter crypto symbol to add to portfolio (E.G. BTC), Q to go back: ").upper()
        if coin_add.upper() == "Q":
            return

    while does_coin_exist(coin_add) == False:
        print(coin_add, "is not a valid cryptocurrency symbol.")
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
    
    #this is what actually adds the user selected crypto to the portfolio (crypto_dict)
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
    
    #this is what actually removes the user selected crypto from the portfolio (crypto_dict)
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

    #this is what actually updates the amount of currency held in the portfolio (crypto_dict)
    crypto_dict[coin_update] = coin_amount
    print(coin_update, "updated to", str(coin_amount))

def portfolio_display():
    #displays the entire portfolio with current prices using the columnar module to generate columns

    #makes sure the portfolio to be displayed isn't empty
    if crypto_dict == {}:
        print("Cannot display empty portfolio.")
        return

    #compiles all the crypto symbols in the portfolio into one comma separated string
    listofcrypto = []
    for lineitem in crypto_dict:
        listofcrypto.append(lineitem)
    listofcrypto_str = ",".join(listofcrypto)

    #feeds all of the crypto symbols in the portfolio into one API request in the get_price function, a list of prices in the same order is returned
    price_list = get_price(listofcrypto_str)
    
    #changes the portfolio (crypto_dict) into a list (data) with every crypto holding being a separate list (a list within a list)
    #each list corresponds to one crypto asset held and has four entries: currency(symbol), price, quantity, and total value
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

    #this is what actually displays the portfolio in a clean column format using columnar module
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
            print(portfolio_name, "has been overwritten.")
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
    print(portfolio_name, "portfolio has been saved.")

def portfolio_load():
    #loads single portfolio from savedportfolios.txt

    try:
        savedportfolios_file = open(os.path.join(sys.path[0], "savedportfolios.txt"), "r")
        savedportfolio_contents = savedportfolios_file.read().splitlines()
        savedportfolios_file.close()
    
    except:
        print("No saved portfolios were found on this computer.")
        return

    #check the file contents for portfolio name tags (@) and compile the names to a list (data)
    data = []
    portfolio_names_list = []
    for line in savedportfolio_contents:
        if line[0:6] == "@Begin":
            data.append([line[6:]])
            portfolio_names_list.append(line[6:])
        else:
            pass

    #show the names of the portfolios found using columnar
    print("We have found the following saved portfolios:")
    headers = ['Portfolio Name']
    table = columnar(data, headers, no_borders=True)
    print(table)

    loadportfolio_name = input("Enter the name of the portfolio you wish to load. Type \"Cancel\" to go back: ")
    if loadportfolio_name.upper() == "CANCEL":
        return
    
    while loadportfolio_name.upper() not in portfolio_names_list:
        print("Invalid entry.")
        loadportfolio_name = input("Enter the name of the portfolio you wish to load. Type \"Cancel\" to go back: ")
        if loadportfolio_name.upper() == "CANCEL":
            return

    #find the portfolio index to load in the file
    saved_portfolio_index = 0
    for line in savedportfolio_contents:
        if line == "@Begin" + loadportfolio_name.upper():
            portfolio_index_begin = saved_portfolio_index
        elif line == "@End" + loadportfolio_name.upper():
            portfolio_index_end = saved_portfolio_index
        else:
            pass
        saved_portfolio_index += 1
    
    #trim savedportfolio_contents of everything except for the user selected load portfolio
    del savedportfolio_contents[portfolio_index_end:]
    del savedportfolio_contents[:portfolio_index_begin+1]

    #load the single portfolio into crypto_dict
    crypto_dict.clear()
    for line in savedportfolio_contents:
        symbol, amount = line.split(" ")
        crypto_dict[symbol] = str(amount)
    print(loadportfolio_name, "portfolio loaded.")

def portfolio_new():
    #ask the user to save portfolio and then completely clear the existing portfolio

    askforsave = input("All unsaved data will be lost. Would you like to save the current portfolio before creating a new one? (Y/N) Type \"Cancel\" to go back: ")
    if askforsave.upper() == "CANCEL":
        return
        
    while askforsave[0] not in ("yYnN"):
        print("Invalid response")
        askforsave =  input("All unsaved data will be lost. Would you like to save the current portfolio before creating a new one? (Y/N) Type \"Cancel\" to go back: ")
        if askforoverwrite.upper() == "CANCEL":
            return
        else:
            pass
        
    if askforsave[0].upper() == "Y":
        portfolio_save()
    else:
        pass

    #clears portfolio
    crypto_dict.clear()
    print("New portfolio created.")

def top_ten_prices():
    print("Here are the top ten crypto currencies by market cap:")
    print("1  BTC  Bitcoin")

print("Welcome to the Crypto Portfolio Display App")

#blank portfolio (dictionary format) created here and is built up in the functions above
crypto_dict = {}

#loads the main menu, program begins here
main_menu()


