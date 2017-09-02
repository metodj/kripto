import requests
import re
import csv
import os
import sys

regex_ticker = re.compile(r'<td><a href=".*?>(?P<borza>.+?)</a></td>.*?target='
                          r'"_blank">(?P<par>.+?)</a>.*?native=".+?">(?P<volume>.+?)</span>'
                          r'</td>.*?native=".+?">(?P<price>.+?)</span>',
                          flags=re.DOTALL)
						  
imena_polj = ['borza', 'par', 'volume', 'price']

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
def pripravi_imenik(ime_datoteke):
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

def shrani(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        print('Shranjujem {}...'.format(url))
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno ze od prej!')
            return
        r = requests.get(url, headers)
    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')
    else:
        pripravi_imenik(ime_datoteke)
        with open(ime_datoteke, 'w') as datoteka:
            datoteka.write(r.text)
            print('shranjeno!')
            

def vsebina_datoteke(ime_datoteke):
    with open(ime_datoteke) as datoteka:
        vsebina = datoteka.read()
    return vsebina


def datoteke(imenik):
    '''Vrne imena vseh datotek v danem imeniku skupaj z imenom imenika.'''
    return [os.path.join(imenik, datoteka) for datoteka in os.listdir(imenik)]

def zapisi_tabelo(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w') as csv_dat:
        writer = csv.DictWriter(csv_dat, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)


def naredi_csv(html, ime_fajla):
    sez = []
    for match in re.finditer(regex_ticker, vsebina_datoteke(html)):
        sez.append(match.groupdict())
    zapisi_tabelo(sez, imena_polj, ime_fajla)
    return 'Uspesno narejena csv datoteka'