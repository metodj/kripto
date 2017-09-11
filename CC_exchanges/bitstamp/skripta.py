import json
import urllib2
import csv
import os
import sys
import datetime

datum = str(datetime.datetime.now())[:10]
os.mkdir(datum)

def pripravi_imenik(ime_datoteke):
    '''Ce se ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

def zapisi_tabelo(slovarji, imena_polj, ime_datoteke, orders):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    datum = str(datetime.datetime.now())[:10]
    ime_datoteke = datum + '/' + ime_datoteke
    #pripravi_imenik(ime_datoteke)
    if orders:
        ime_datoteke = 'orders/' + ime_datoteke
    with open(ime_datoteke, 'w') as csv_dat:
        writer = csv.DictWriter(csv_dat, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)

def zajemi(par, time='day', orders=False):
    url = 'https://www.bitstamp.net/api/v2/transactions/' + par + '/?time=' + time
    json_obj = urllib2.urlopen(url)
    data = json.load(json_obj)
    ime_csv = par + '.csv'
    zapisi_tabelo(data, ['date', 'tid', 'price', 'amount', 'type'], ime_csv, orders)
    rez = 'Par ' + par + ' zajet.'
    return rez
	

pari = ['btcusd', 'btceur', 'eurusd', 'xrpusd', 'xrpeur', 'xrpbtc', 'ltcusd', 'ltceur', 'ltcbtc', 'ethusd', 'etheur', 'ethbtc']
for par in pari:
	zajemi(par)
