from urllib import request as rq
import tkinter as tk


price = rq.urlopen('https://api.binance.com/api/v3/ticker/price')

print(price.read())
