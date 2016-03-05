#!/usr/bin/python
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
import requests
from lxml import html
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read("/Users/Wei/pricetracking.cfg")
sender = config.get('msg','sender')
receiver = config.get('userinfo','receiver')
sender_pwd = config.get('msg','sender_pwd')
smtp_server = config.get('msg','smtp_server')
product_url = config.get('userinfo','URL')
expect_price = config.get('userinfo','expect_price')

def send_mail():

    message_content = open("/Users/Wei/pricealartmessage.txt",'rb')
    msg = MIMEText(message_content.read())
    message_content.close()

    msg['Subject'] = "Price Alert"
    msg['From'] = sender
    msg['To'] = receiver 

    s = smtplib.SMTP(smtp_server)
    s.starttls()
    s.login(sender,sender_pwd)
    s.sendmail(sender,receiver,msg.as_string())
    s.quit()

product_xpath = '//*[@id="column_center"]/div/div[1]/div/div[2]/div/div[2]/span[2]/text()' 
status_xpath = '//*[@class="input_button_css "]'
price_xpath = '//*[@id="productPrices"]/span[4]/text()'

r = requests.get(product_url)
tree = html.fromstring(r.content)

product = tree.xpath(product_xpath)
get_status = tree.xpath(status_xpath)
status = get_status[0].text
get_price = tree.xpath(price_xpath)
price = float((get_price[0].split())[0].strip('$'))

if status == 'Sold Out':
    print 'Sold Out'
elif status == '+ Add To Cart':
    if price < float(expect_price):
        print 'Send Mail' 
        send_mail()
    else:
        pass
else:
    pass

print '%s\n%s\n%s' % (product,status,price)

