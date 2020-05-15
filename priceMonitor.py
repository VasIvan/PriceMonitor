#GUI
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
#functionality
import requests
from bs4 import BeautifulSoup
#Uncomment the next line of code if you want to have alert on the Windows!!!
#import ctypes
import time
import threading

root = Tk()
root.title("Price Monitor")
root.geometry("800x500")

website = "Choose website"

#Dropdown function when chosen
def comboclick(event):
    global website
    website = myCombo.get()


#Button onclick event
def onclick():
    URL = str(url.get()) #URL ADDRESS
    setPrice = eval(addPrice.get()) #MAX. PRICE
    timesDay = eval(times.get()) #Check X times a day
    website = str(myCombo.get()) #WEBSITE
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')


    
    var = "Maximum price: \n" + addPrice.get() + "€ \n\n URL to the website: \n" + URL + "\n\n Website: \n" + website + "\n\n ----------------------------- \n"
    
    #Cheking IF the URL and chosen option from dropdown matched
    if not website.lower() in URL:
        response = messagebox.showwarning("Warning", "The URL adress is not an actual URL from the website you chose! Please check that the link match with the website you chose from the dropdown menu!!!")
        #Setting inputs to default when OK is clicked
        if response == "ok":
            url.delete(first=0,last=1000)
            addPrice.delete(first=0,last=100)
            times.delete(first=0,last=100)
            myCombo.current(0)
        #Uncomment the next line of code if you want to have alert on the Windows!!!
        #ctypes.windll.user32.MessageBoxW(0, "The URL adress is not an actual URL from the website you chose! Please check that the link match with the website you chose from the dropdown menu!!!", "Error", 0)
        return

    myLabel = Label(root, text=str(var))
    myLabel2 = Label(root, text=str("\n\n Press Monitor button to start the program. When you started you can leave it working in the background \n and wait for notification when the price drop under the price you set"), fg="green")
    myLabel.pack()
    myLabel2.pack()
    btn.pack_forget()
    addPrice.pack_forget()
    addPriceLabel.pack_forget()
    urlLabel.pack_forget()
    url.pack_forget()
    timesLabel.pack_forget()
    times.pack_forget()
    myCombo.pack_forget()
    price = ""
    product = ""
    def monitor():
        myLabel2.pack_forget()
        mon.pack_forget()
        t = threading.Timer(86400/timesDay, monitor)
        t.start()
        global price
        global product
            #Extract price and product from URL    
        if website == "Tori.fi":
            price = soup.find(attrs={'class':'price'}).get_text()
            product = soup.find(attrs={'class':'topic'}).get_text()
        elif website == "Nettiauto":
            price = soup.find(id="rightLogoWrap").get_text()
            product = soup.find(id="heightForSlogan").get_text()
        elif website == "Etuovi":
            price = soup.find(attrs={'class':'flexboxgrid__col-xs-4__p2Lev flexboxgrid__col-sm-3__28H0F flexboxgrid__col-md-5__3SFMx'}).get_text()
            product = soup.find(attrs={'class':'ItemSummaryContainer__subTitle__2OjGg'}).get_text()
        fPrice = int("".join(i for i in price if i.isdigit()))
        #Check if the price is under the price we set
        if fPrice < setPrice:
            print("OK")
            #Alert that the price is less than the set price
            congr = messagebox.showinfo("Congratulation!", "The current price drop to: " + str(fPrice) + " €")
            #When X or OK button is pressed the program stop to monitor the price
            if congr == "ok":
                t.cancel()
                print("canceled")
                #Uncomment the next line of code if you want to have alert on the Windows!!!
                #ctypes.windll.user32.MessageBoxW(0, "The current price drop to: " + str(fPrice) + " €", "Price Alert", 0)
        #Displays the product name and price
        print(price + "   " + product)
        newInfoLabel = Label(root, text=str("\n\n Final result: \n\n Product name: " + product + "\n\n Current price: " + price + "\n\n If you want to continue monitoring the price you have to start the program again!"), fg="green")
        newInfoLabel.pack()
    #Monitor button for running the program    
    mon = Button(root, width=28 , text="Monitor", command=monitor)
    mon.pack()
    
  
    

#Input field
urlLabel = Label(root, text="Add URL here:")
urlLabel.pack()
url = Entry(root, width=33)
url.pack()
addPriceLabel = Label(root, text="Wished price:")
addPriceLabel.pack()
addPrice = Entry(root, width=33)
addPrice.pack()
timesLabel = Label(root, text="How much times per day you want to check the price:")
timesLabel.pack()
times = Entry(root, width=33)
times.pack()

#Dropdown options
options = ["Choose website",
    "Tori.fi",
    "Nettiauto",
    "Etuovi"]

#Dropdown
myCombo = ttk.Combobox(root, width=30, value=options)
myCombo.current(0)
myCombo.bind("<<ComboboxSelected>>", comboclick)
myCombo.pack()

#Button
btn = Button(root, width=28 , text="Start", command=onclick)
btn.pack()
root.mainloop()
