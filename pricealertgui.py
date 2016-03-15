#!/usr/bin/python
import sqlite3
from Tkinter import *
import tkMessageBox
import re
import ConfigParser
import ttk

def save_entry_to_cfg():
    #try RawConfigParser.items(section) later
    #must indicate instance of RawConfigParser
    config = ConfigParser.RawConfigParser()
    config.read("/Users/Wei/pricetracking.cfg")
    config.set('userinfo','URL',URL.get())
    config.set('userinfo','receiver',mailaddress.get())
    
    #data storage with sqlite3
    conn = sqlite3.connect('PriceDropAlerts.db')
    c = conn.cursor()
    #c.execute('''CREATE TABLE userinfo
    #(URL,mail address,expect price)
    #''')

    if re.match('^[-+]?([0-9]+\.[0-9]+|[0-9]+)$',expectprice.get()):
        #integer may start with naught
        config.set('userinfo','expect_price',expectprice.get())

        c.execute("INSERT INTO userinfo VALUES ('%s','%s','%s')" % (URL.get(),mailaddress.get(),expectprice.get()))
        #inscure way
        #put format arguments into a tuple
    else:
        tkMessageBox.showerror("Expect Price","Please input a valid number")
        print "invalid number."


    with open("/Users/Wei/pricetracking.cfg",'wb') as configfile:
        config.write(configfile)
        
        c.close()
        conn.commit()
        conn.close()

root = Tk()
root.title("Price Drop Alerts")

frame = ttk.Frame(root,padding="5",relief="")

URLlabel = ttk.Label(frame,text="URL")
mailaddresslabel = ttk.Label(frame,text="Your Mail Address")
expectpricelabel = ttk.Label(frame,text="Expect Price")

URL = ttk.Entry(frame)

mailaddress = ttk.Entry(frame)
expectprice = ttk.Entry(frame)

submit = ttk.Button(frame,text="Submit",command=save_entry_to_cfg)

frame.grid()
URLlabel.grid(column=0,row=0)
mailaddresslabel.grid(column=0,row=1)
expectpricelabel.grid(column=0,row=2)

URL.grid(column=1,row=0)
mailaddress.grid(column=1,row=1)
expectprice.grid(column=1,row=2)
submit.grid(column=0,row=3,columnspan=2)

root.mainloop()


