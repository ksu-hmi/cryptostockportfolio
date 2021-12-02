import json
import pprint
from tkinter import *
import matplotlib.pyplot as plt

import requests

def red_green(amount):
  if amount >= 0:
    return "green"
  else:
    return "red"

root = Tk()

#name = Label(root, text = "Usen", bg="blue",fg="white")
#name.grid(row=0, column=0, sticky =N+S+E+W)

root.title("Crypto Currency Portfolio")

#----------------------CREATE HEADER-------------------------------------------
#----------------------Note: This steps can also be done with a loop-----------
header_name = Label(root, text="Name", bg="white", font = "Verdana 8 bold")
header_name.grid(row=0, column=0, sticky =N+S+E+W)

header_rank = Label(root, text="Rank", bg="silver", font = "Verdana 8 bold")
header_rank.grid(row=0, column=1, sticky =N+S+E+W)

header_current_price = Label(root, text="Current Price", bg="white", font = "Verdana 8 bold")
header_current_price.grid(row=0, column=2, sticky =N+S+E+W)

header_price_paid = Label(root, text="Price Paid", bg="silver", font = "Verdana 8 bold")
header_price_paid.grid(row=0, column=3, sticky =N+S+E+W)

header_profit_loss_per = Label(root, text="Profit/Loss Per", bg="white", font = "Verdana 8 bold")
header_profit_loss_per.grid(row=0, column=4, sticky =N+S+E+W)

header_one_hr_change = Label(root, text="1 HR Change", bg="silver", font = "Verdana 8 bold")
header_one_hr_change.grid(row=0, column=5, sticky =N+S+E+W)

header_twenty4_hr_change = Label(root, text="24 HR Change", bg="white", font = "Verdana 8 bold")
header_twenty4_hr_change.grid(row=0, column=6, sticky =N+S+E+W)

header_seven_day_change = Label(root, text="7 Day Change", bg="silver", font ="Verdana 8 bold")
header_seven_day_change.grid(row=0, column=7, sticky =N+S+E+W)

header_current_value = Label(root, text="Current Value", bg="white", font="Verdana 8 bold")
header_current_value.grid(row=0, column=8, sticky =N+S+E+W)

header_profit_loss_total = Label(root, text="Profit/Loss Total", bg="silver", font = "Verdana 8 bold")
header_profit_loss_total.grid(row=0, column=9, sticky =N+S+E+W)


#root.mainloop()



def lookup():
  api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY=a6e2a4fb-fc21-43cc-8157-3f2f0eb1f6e9&start=1&limit=5000&convert=USD")
  api = json.loads(api_request.content)

  my_crypto_portfolio =[
    {
      "sym": "BTC",
      "amount_owned": 2.5,
      "price_paid_per": 5000
    },
    {
      "sym": "XRP",
      "amount_owned": 100000,
      "price_paid_per": 1.8
    },
    {
      "sym": "LUNA",
      "amount_owned": 100,
      "price_paid_per": .02
    },
    {
      "sym": "SHIB",
      "amount_owned": 100000000,
      "price_paid_per": .000004
    },
    {
      "sym": "ETH",
      "amount_owned": 100,
      "price_paid_per": 2000
    },
    {
      "sym": "VET",
      "amount_owned": 100000,
      "price_paid_per": .1
    },
    {
      "sym": "ADA",
      "amount_owned": 130000,
      "price_paid_per": 1.5
    },
    {
      "sym": "CHZ",
      "amount_owned": 10000,
      "price_paid_per": .5
    },
    {
      "sym": "FET",
      "amount_owned": 10000,
      "price_paid_per": .75
    },
    {
      "sym": "XLM",
      "amount_owned": 10000,
      "price_paid_per": .3
    }
  ]
  pprint.pprint("------------------------------------------------------------------------")
  portfolio_profit_loss = 0
  total_current_value =0
  row_count = 1
  pie = []
  pie_size = []
  for crypto in api['data']:
    for coin in my_crypto_portfolio:
      if coin["sym"] == crypto["symbol"]:
        #Doing some mathmatical calculations
        total_paid = float(coin["amount_owned"]) * float(coin["price_paid_per"])
        current_value = float(coin["amount_owned"]) * float(crypto["quote"]["USD"]["price"])
        profit_loss = current_value - total_paid
        portfolio_profit_loss += profit_loss
        profit_loss_per_coin = float(crypto["quote"]["USD"]["price"])- float(coin["price_paid_per"])
        total_current_value += current_value
        pie.append(crypto["name"])
    
        #pie_size.append(coin["amount_owned"])
        pie_size.append(current_value)

        #pprint.pprint(crypto["symbol"])
        #pprint.pprint(crypto["name"])
        #pprint.pprint(" Current Price: ${0:.2f}".format(float(crypto["quote"]["USD"]["price"])))
        #pprint.pprint(" Profit/Loss Per Coin: ${0:.2f}".format(float(profit_loss_per_coin)))
        #pprint.pprint(" Circulating Supply: {0:.2f}".format(float(crypto["circulating_supply"])))
        #pprint.pprint(" Total Supply: {0:.2f}".format(float(crypto["total_supply"])))
        #pprint.pprint(" Total Paid: ${0:.2f}".format(float(current_value)))
        #pprint.pprint(" Rank: {0:.0f}".format(float(crypto["cmc_rank"])))
        #pprint.pprint(" Profit/Loss: ${0:.2f}".format(float(profit_loss)))
        #pprint.pprint("------------------------------------------------------------------------")
        
        #-------------------Note: This step can also be done with a loop-------
        name = Label(root, text=crypto["name"], bg="white")
        name.grid(row=row_count, column=0, sticky =N+S+E+W)

        rank = Label(root, text=crypto["cmc_rank"], bg="silver")
        rank.grid(row=row_count, column=1, sticky =N+S+E+W)

        current_price = Label(root, text="${0:.2f}".format(float(crypto["quote"]["USD"]["price"])), bg="white")
        current_price.grid(row=row_count, column=2, sticky =N+S+E+W)

        price_paid = Label(root, text="${0:.2f}".format(float(coin["price_paid_per"])), bg="silver")
        price_paid.grid(row=row_count, column=3, sticky =N+S+E+W)

        profit_loss_per = Label(root, text="${0:.2f}".format(float(profit_loss_per_coin)), bg="white", fg= red_green(float(profit_loss_per_coin)))
        profit_loss_per.grid(row=row_count, column=4, sticky =N+S+E+W)

        one_hr_change = Label(root, text="{0:.2f}%".format(float(crypto["quote"]["USD"]["percent_change_1h"])), bg="silver", fg= red_green(float(crypto["quote"]["USD"]["percent_change_1h"])))
        one_hr_change.grid(row=row_count, column=5, sticky =N+S+E+W)

        twenty4_hr_change = Label(root, text="{0:.2f}%".format(float(crypto["quote"]["USD"]["percent_change_24h"])), bg="white", fg= red_green(float(crypto["quote"]["USD"]["percent_change_24h"])))
        twenty4_hr_change.grid(row=row_count, column=6, sticky =N+S+E+W)

        seven_day_change = Label(root, text="{0:.2f}%".format(float(crypto["quote"]["USD"]["percent_change_7d"])), bg="silver", fg= red_green(float(crypto["quote"]["USD"]["percent_change_7d"])))
        seven_day_change.grid(row=row_count, column=7, sticky =N+S+E+W)

        current_value = Label(root, text="${0:.2f}".format(float(current_value)), bg="white")
        current_value.grid(row=row_count, column=8, sticky =N+S+E+W)

        profit_loss_total = Label(root, text="${0:.2f}".format(float(profit_loss)), bg="silver", fg= red_green(float(profit_loss)))
        profit_loss_total.grid(row=row_count, column=9, sticky =N+S+E+W)

        row_count +=1
  
  portfolio_profits = Label(root, text = "Total Portfolio Profit/Loss: ${0:2f}".format(float(portfolio_profit_loss)), font = "Verdana 8 bold", fg=red_green(float(portfolio_profit_loss)))
  portfolio_profits.grid(row=row_count,column =0, sticky = W, padx = 10, pady = 10)

  root.title("Crypto Currency Portfolio - Porfolio Value: ${0:.2f}".format(float(total_current_value)))

  api = ""
  update_button = Button(root, text = "Update Prices", command = lookup)
  update_button.grid(row=row_count, column =9, sticky = E+S, padx= 10, pady =10)


# Data to plot
  def graph(pie, pie_size):
    labels = pie
    sizes = pie_size
    colors = ['yellowgreen', 'gold','lightskyblue','lightcoral', 'red', 'brown', 'blue','orange','pink','green']
    patches, texts= plt.pie(sizes, colors= colors, shadow= True, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
  
  graph_button = Button(root, text="Pie Chart", command= lambda: graph(pie, pie_size))
  graph_button.grid(row=row_count, column =8, sticky = E+S, padx=10, pady=10)
  

lookup()
root.mainloop()