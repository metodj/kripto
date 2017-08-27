import json
import urllib2
import csv
import os
import sys

url = 'https://www.bitstamp.net/api/transactions/?time=day'
#url = 'https://www.bitstamp.net/api/transactions/?time=minute'
json_obj = urllib2.urlopen(url)
data = json.load(json_obj)

#for item in data:
#    print(item['date'])

def pripravi_imenik(ime_datoteke):
    '''Ce se ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

def zapisi_tabelo(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w') as csv_dat:
        writer = csv.DictWriter(csv_dat, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)

def zajemi(par):
    url = 'https://www.bitstamp.net/api/v2/transactions/' + par + '/?time=day'
    json_obj = urllib2.urlopen(url)
    data = json.load(json_obj)
    ime_csv = par + '.csv'
    zapisi_tabelo(data, ['date', 'tid', 'price', 'amount', 'type'], ime_csv)
    rez = 'Par ' + par + ' zajet.'
    return rez

#par = tBTCUSD
def zajemiBitfinex(par):
    url = "https://api.bitfinex.com/v2/trades/" + par
    json_obj = urllib2.urlopen(url)
    data = json.load(json_obj)
    ime_csv = par + '.csv'
    zapisi_tabelo(data, ['MTS', 'AMOUNT', 'PRICE', 'RATE', 'PERIOD'], ime_csv)
    rez = 'Par ' + par + ' zajet.'
    return rez

#zapisi_tabelo(data, ['date', 'tid', 'price', 'amount', 'type'], 'bitstamp.csv' )