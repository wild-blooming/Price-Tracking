from Tkinter import *
import ConfigParser
import ttk

def save_entry_to_cfg():
    #try RawConfigParser.items(section) later
    #must indicate instance of RawConfigParser
    config = ConfigParser.RawConfigParser()
    config.read("/Users/Wei/pricetracking.cfg")
    config.set('userinfo','URL',URL.get())
    config.set('userinfo','receiver',mailaddress.get())
    config.set('userinfo','expect_price',expectprice.get())
    with open("/Users/Wei/pricetracking.cfg",'wb') as configfile:
        config.write(configfile)

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


