from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

def change_plain(data):
    for i in range(0, len(data)):
        plain = data[i].get_text()
        plain = plain.replace(',', '')
        data[i] = plain
    return data

def change_plain_int(data):
    for i in range(0, len(data)):
        plain = data[i].get_text()
        plain = int(plain.replace(',', ''))
        data[i] = plain
    return data


def getcap(sosok):
    raw_data = requests.get(f'https://finance.naver.com/sise/sise_market_sum.nhn?sosok={sosok}').text
    soup = BeautifulSoup(raw_data, 'html.parser')
    names = soup.select('tbody > tr > td:nth-child(2) > a', class_='title')
    caps = soup.select('tbody > tr > td:nth-child(7)')
    names = change_plain(names)
    caps = change_plain_int(caps)
    
    return names, caps

@app.route('/')
@app.route('/kospi')
def kospi():
    names, caps = getcap('0')
    return render_template('home.html', names=names, caps=caps, sosok='KOSPI')

@app.route('/kosdaq')
def kosdac():
    names, caps = getcap('1')
    return render_template('home.html', names=names, caps=caps, sosok='KOSDAQ')
    
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)