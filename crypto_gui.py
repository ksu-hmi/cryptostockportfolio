from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Menu
import matplotlib.pyplot as plt
import sys
import requests
from os import path


addcoin = {"1":False}
my_crypto_portfolio = {}

class MyPortfolio(Frame):
    def __init__(self, win):

        Frame.__init__(self, win)

        self.rows = 1

        if my_crypto_portfolio != {}:
            self.get_api_data()
        self.create_headers()
        self.create_portfolio()
        self.create_bottom()
        self.grid()

        menu = Menu(window)
        new_item = Menu(menu, tearoff=0)
        new_item.add_command(label="Open", command= lambda: self.open())
        new_item.add_command(label="Save As", command= lambda: self.saveport())
        menu.add_cascade(label="File", menu=new_item)
        window.config(menu=menu)

        window.title("Crypto Currency Portfolio - Total Value: ${0:.2f}".format(float(self.total_current_value)))
        
    def get_api_data(self):

        listofcrypto = []
        for lineitem in my_crypto_portfolio:
            listofcrypto.append(lineitem)
        listofcrypto_str = ",".join(listofcrypto)

        fmt = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms={}&api_key=4120b66bee53ddad00260553cac1215997407f8b2abbdcb714c55a7f3240ed27'

        try:
            r = requests.get(fmt.format(listofcrypto_str, "USD"))
        except requests.exceptions.RequestException:
            sys.exit('Could not complete request')

        try:
            self.data_raw = r.json()['RAW']
        except:
            sys.exit('Could not parse data')

    def does_coin_exist(self, sym):
        
        fmt = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=USD&api_key=4120b66bee53ddad00260553cac1215997407f8b2abbdcb714c55a7f3240ed27'

        try:
            r = requests.get(fmt.format(sym))
        except requests.exceptions.RequestException:
            sys.exit('Could not complete request')

        try:
            data_raw = r.json()
            if 'Message' in data_raw:
                return False
            elif 'PRICE' in data_raw['RAW'][sym]['USD']:
                return True
            else:
                pass

        except:
            sys.exit('Could not parse data')

    def create_headers(self):

        self.header_name = Label(self, text="Symbol", bg="white", font = "Verdana 8 bold")
        self.header_name.grid(row=0, column=0, sticky =N+S+E+W)

        self.header_current_price = Label(self, text="Current Price", bg="silver", font = "Verdana 8 bold")
        self.header_current_price.grid(row=0, column=1, sticky =N+S+E+W)

        self.header_quantity = Label(self, text="Quantity", bg="white", font = "Verdana 8 bold")
        self.header_quantity.grid(row=0, column=2, sticky =N+S+E+W)

        self.header_current_value = Label(self, text="Current Value", bg="silver", font="Verdana 8 bold")
        self.header_current_value.grid(row=0, column=3, sticky =N+S+E+W)

        self.header_price_paid = Label(self, text="Price Paid Per", bg="white", font = "Verdana 8 bold")
        self.header_price_paid.grid(row=0, column=4, sticky =N+S+E+W)

        self.header_profit_loss_per = Label(self, text="Profit/Loss Per", bg="silver", font = "Verdana 8 bold")
        self.header_profit_loss_per.grid(row=0, column=5, sticky =N+S+E+W)

        self.header_profit_loss_total = Label(self, text="Profit/Loss Total", bg="white", font = "Verdana 8 bold")
        self.header_profit_loss_total.grid(row=0, column=6, sticky =N+S+E+W)

        self.header_one_hr_change = Label(self, text="1 HR Change", bg="silver", font = "Verdana 8 bold")
        self.header_one_hr_change.grid(row=0, column=7, sticky =N+S+E+W)

        self.header_twenty4_hr_change = Label(self, text="24 HR Change", bg="white", font = "Verdana 8 bold")
        self.header_twenty4_hr_change.grid(row=0, column=8, sticky =N+S+E+W)

        #self.header_seven_day_change = Label(self, text="7 Day Change", bg="silver", font ="Verdana 8 bold")
        #self.header_seven_day_change.grid(row=0, column=9, sticky =N+S+E+W)

        #header_rank = Label(root, text="Rank", bg="silver", font = "Verdana 8 bold")
        #header_rank.grid(row=0, column=1, sticky =N+S+E+W)

        self.modify_remove = Label(self, font = "Verdana 8 bold")
        self.modify_remove.grid(row=0, column=9, sticky =N+S+E+W, padx=40)
    
    def create_portfolio(self):

        self.portfolio_profits = 0
        self.total_current_value = 0
        self.pie = []
        self.pie_size = []

        for item in my_crypto_portfolio:
            sym = item
            qty = my_crypto_portfolio[sym][0]
            paid = my_crypto_portfolio[sym][1]
            total_paid = float(qty) * float(paid)

            current_price = self.data_raw[sym]["USD"]["PRICE"]
            current_value = float(qty) * float(current_price)
            profit_loss = current_value - total_paid
            self.portfolio_profits += profit_loss
            profit_loss_per_coin = float(current_price) - float(paid)
            self.total_current_value += current_value
            onehourchange = float(self.data_raw[sym]["USD"]["CHANGEPCTHOUR"])
            daychange = float(self.data_raw[sym]["USD"]["CHANGEPCT24HOUR"])

            self.pie.append(sym)
            self.pie_size.append(current_value)

            self.symbol = Label(self, text=sym, bg="white")
            self.symbol.grid(row=self.rows, column=0, sticky=N+S+E+W)

            self.currentpricelabel = Label(self, text="${0:.2f}".format(float(current_price)), bg="silver")
            self.currentpricelabel.grid(row=self.rows, column=1, stick=N+S+E+W)

            self.quantity = Label(self, text=qty, bg="white")
            self.quantity.grid(row=self.rows, column=2, sticky=N+S+E+W)

            self.currentvaluelabel = Label(self, text="${0:.2f}".format(float(current_value)), bg="silver")
            self.currentvaluelabel.grid(row=self.rows, column=3, stick=N+S+E+W)

            self.pricepaidper = Label(self, text="${0:.2f}".format(float(paid)), bg="white")
            self.pricepaidper.grid(row=self.rows, column=4, sticky=N+S+E+W)

            self.profitlossper = Label(self, text="${0:.2f}".format(float(profit_loss_per_coin)), bg="silver", fg= self.red_green(float(profit_loss_per_coin)))
            self.profitlossper.grid(row=self.rows, column=5, sticky=N+S+E+W)

            self.profitlosstotal = Label(self, text="${0:.2f}".format(float(profit_loss)), bg="white", fg= self.red_green(float(profit_loss)))
            self.profitlosstotal.grid(row=self.rows, column=6, sticky=N+S+E+W)

            self.onehrchange = Label(self, text="{0:.2f}%".format(float(onehourchange)), bg="silver", fg= self.red_green(float(onehourchange)))
            self.onehrchange.grid(row=self.rows, column=7, sticky=N+S+E+W)

            self.dailychange = Label(self, text="{0:.2f}%".format(float(daychange)), bg="white", fg= self.red_green(float(daychange)))
            self.dailychange.grid(row=self.rows, column=8, sticky=N+S+E+W)

            self.modifybutton = Button(self, text="Modify", command= lambda rownumber = self.rows, symbol=sym: self.modify(rownumber, symbol))
            self.modifybutton.grid(row=self.rows, column =10, sticky = W+S, padx=45, pady=0)

            self.deletebutton = Button(self, text="Delete", command= lambda symbol=sym: self.delete(symbol))
            self.deletebutton.grid(row=self.rows, column =10, sticky = E+S, padx=0, pady=0)

            self.rows += 1
        
        if addcoin["1"] == True:

            self.symbolentry = Entry(self, font="Verdana 8")
            self.symbolentry.grid(row=self.rows, column=0, sticky = N+S+E+W)

            self.qtyentry = Entry(self, font="Verdana 8")
            self.qtyentry.grid(row=self.rows, column=2, sticky = N+S+E+W)

            self.paidentry = Entry(self, font="Verdana 8")
            self.paidentry.grid(row=self.rows, column=4, sticky = N+S+E+W)

            self.savebutton = Button(self, text="Save", command= lambda symbol=self.symbolentry.get(): self.save(symbol))
            self.savebutton.grid(row=self.rows, column =9, sticky = E+S, padx=0, pady=0)

            self.rows += 1   
            addcoin["1"] = False

    def modify(self, rownumber, sym):

        qty = my_crypto_portfolio[sym][0]
        paid = my_crypto_portfolio[sym][1]

        self.symbolentry = Entry(self, font="Verdana 8")
        self.symbolentry.grid(row=rownumber, column=0, sticky = N+S+E+W)
        self.symbolentry.insert(0, sym)

        self.qtyentry = Entry(self, font="Verdana 8")
        self.qtyentry.grid(row=rownumber, column=2, sticky = N+S+E+W)
        self.qtyentry.insert(0, qty)

        self.paidentry = Entry(self, font="Verdana 8")
        self.paidentry.grid(row=rownumber, column=4, sticky = N+S+E+W)
        self.paidentry.insert(0, paid)

        self.savebutton = Button(self, text="Save", command= lambda rownumber=self.rows, symbol=sym: self.save(symbol))
        self.savebutton.grid(row=rownumber, column =9, sticky = E+S, padx=0, pady=0)

    def save(self, symbol):

        newsymbol = self.symbolentry.get().upper()
        newqty = self.qtyentry.get()
        newpaid = self.paidentry.get()

        if self.does_coin_exist(newsymbol) == False:
            message = newsymbol + " is not a valid crypto currency symbol."
            response = messagebox.showerror("Invalid Entry", message)
            return

        if symbol in my_crypto_portfolio:  
            del my_crypto_portfolio[symbol]
        my_crypto_portfolio[newsymbol] = [newqty, newpaid]

        self.savebutton.destroy()
        self.symbolentry.destroy()
        self.qtyentry.destroy()
        self.paidentry.destroy()

        self.refresh()

    def delete(self, symbol):

        message = "Are you sure you want to delete " + symbol + " from your portfolio?"
        response = messagebox.askyesno("Delete Crypto", message)

        if response:
            del my_crypto_portfolio[symbol]
        else:
            pass

        self.refresh()

    def create_bottom(self):

        self.portfolio_profits_label = Label(self, text = "Total Portfolio Profit/Loss: ${0:.2f}".format(float(self.portfolio_profits)), font = "Verdana 8 bold", fg=self.red_green(float(self.portfolio_profits)))
        self.portfolio_profits_label.grid(row=self.rows ,column =0, sticky = W, padx = 10, pady = 10)

        self.update_button = Button(self, text = "Update Prices", command = lambda: self.refresh())
        self.update_button.grid(row=self.rows, column =8, sticky = E+S, padx= 10, pady =10)

        self.add_coin_button = Button(self, text = "Add A Coin", command =lambda: self.add_coin())
        self.add_coin_button.grid(row=self.rows, column= 9, sticky = E+S, padx = 10, pady = 10)
  
        self.graph_button = Button(self, text="Pie Chart", command= lambda: self.graph(self.pie, self.pie_size))
        self.graph_button.grid(row=self.rows, column =7, sticky = E+S, padx=10, pady=10)

    def red_green(self, amount):

        if amount >= 0:
            return "green"
        else:
            return "red"

    def refresh(self):

        Frame.destroy(self)
        MyPortfolio(window)

    def add_coin(self):

        addcoin["1"] = True
        self.refresh()

    def graph(self, pie, pie_size):
        self.labels = pie
        self.sizes = pie_size
        self.colors = ['yellowgreen', 'gold','lightskyblue','lightcoral', 'red', 'brown', 'blue','orange','pink','green']
        self.patches, self.texts= plt.pie(self.sizes, colors= self.colors, shadow= True, startangle=90)
        plt.legend(self.patches, self.labels, loc="best")
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
    
    def open(self):
        files = [("Text Document", "*.txt")]
        file = filedialog.askopenfile(mode="r", initialdir= path.dirname(__file__), filetypes=files, defaultextension = files)
        
        if file:
            my_crypto_portfolio.clear()
            savedportfolio_contents = file.read().splitlines()
    
            for line in savedportfolio_contents:
                entries = line.split()
                my_crypto_portfolio[entries[0]] = [entries[1], entries[2]]
            file.close()
            self.refresh()
        else:
            pass

    def saveport(self):
        files = [("Text Document", "*.txt")]
        file = filedialog.asksaveasfile(mode="w", initialdir= path.dirname(__file__), filetypes=files, defaultextension = files)

        if file:
            for crypto in my_crypto_portfolio:
                lineitem = crypto + " " + str(my_crypto_portfolio[crypto][0]) + " " + str(my_crypto_portfolio[crypto][1]) + "\n"
                file.writelines(lineitem)
            file.close()
        else:
            pass

window = Tk()
openapp = MyPortfolio(window)
window.mainloop()