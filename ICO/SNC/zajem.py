import json
import urllib2
import csv
import os
import sys

def zapisi_tabelo_snc(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w') as csv_dat:
        writer = csv.DictWriter(csv_dat, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            tmp = {your_key: slovar[your_key] for your_key in imena_polj}
            writer.writerow(tmp)

def zajemiSNC():
    url = 'http://api.etherscan.io/api?module=account&action=txlist&address=0x5fb3D432bae33FCd418edE263D98D7440E7fA3ea&apikey=BAVKRF75U3XC7I7JN3NPR2BWHGACDIH51X'
    json_obj = urllib2.urlopen(url)
    data = json.load(json_obj)
    data = data['result']
    polja = ['blockNumber', 'timeStamp', 'from', 'to', 'value']
    zapisi_tabelo_snc(data, polja, 'SNC.csv')
    return "Oujeaa"

def pripravi_imenik(ime_datoteke):
    '''Ce se ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)