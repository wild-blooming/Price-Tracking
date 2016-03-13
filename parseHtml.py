#!/usr/bin/python
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from lxml import html
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read("/Users/Wei/pricetracking.cfg")
sender = config.get('msg','sender')
receiver = config.get('userinfo','receiver')
senderpwd = config.get('msg','sender_pwd')
smtpserver = config.get('msg','smtp_server')

def sendMail():

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Price Alert"
    msg['From'] = sender
    msg['To'] = receiver 

    text = "The product price now meet up to your expection:\n{}".format(config.get('userinfo','URL'))
    msg.attach(MIMEText(text,'plain'))
    s = smtplib.SMTP(smtpserver)
    s.starttls()
    s.login(sender,senderpwd)
    s.sendmail(sender,receiver,msg.as_string())
    s.quit()

r = requests.get(config.get('userinfo','URL'))
tree = html.fromstring(r.content)

product = tree.xpath('//*[@id="column_center"]/div/div[1]/div/div[2]/div/div[2]/span[2]/text()')
status = (tree.xpath('//*[@class="input_button_css "]')[0]).text
specialornot = tree.xpath('//*[@id="productPrices"]/span[1]/text()')
print specialornot
if specialornot == ['Special:']:
    price = float(((tree.xpath('//*[@id="productPrices"]/span[4]/text()'))[0].split())[0].strip('$'))
else:
    price = float(((tree.xpath('//*[@id="productPrices"]/text()'))[4].split())[1].strip('$')) 

if status == 'Sold Out':
    print 'Sold Out'
elif status == '+ Add To Cart':
    if price < float(config.get('userinfo','expect_price')):
        print 'Send Mail' 
        sendMail()
    else:
        pass
else:
    pass

print '%s\n%s\n%s' % (product,status,price)

