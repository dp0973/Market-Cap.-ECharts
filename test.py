import requests
from bs4 import BeautifulSoup

raw_data = requests.get('https://finance.naver.com/sise/sise_market_sum.nhn').text
soup = BeautifulSoup(raw_data, 'html.parser')
names = soup.select('tbody > tr > td:nth-child(2) > a', class_='title')
caps = soup.select('tbody > tr > td:nth-child(7)')
data = []
for name, cap in zip(names, caps):
    dic = {}
    cap = cap.get_text()
    dic['value'] = int(cap.replace(',', ''))
    dic['name'] = name.get_text()
    data.append(dic)
data = str(data)
data = data.replace("{'", '{')
data = data.replace("':", ':')
data = data.replace(", '", ', ')
print(data)