import requests
from bs4 import BeautifulSoup
from common import get_api
from datetime import datetime
from random import choice
from locale import setlocale, LC_ALL
from collections import Counter
from time import sleep

setlocale(LC_ALL, 'es_ES.UTF-8')

today = datetime.today()
day = today.strftime('%d')
month = today.strftime('%B')

headers = {'User-Agent': 'efemeridesbot/0.1 (https://masto.es/@efemeridesbot)'}
r = requests.get('https://es.m.wikipedia.org/wiki/' + day + '_de_' + month, headers=headers)
html = BeautifulSoup(r.text, "html.parser")
events = html.find('div', { 'id': 'bodyContent' }).find_all('ul')[0].find_all('li')

years = [1000,1500,1800,1850,1900,1935,1947,1960,1970,1980,1990,2000,2010,2050]
texts = {i: [] for i in years }

for event in events:
    text = event.get_text()
    try:
        text_year = int(text.split(":")[0].split(u'\xa0')[0].split(" ")[0].split(",")[0])
        for year in years:
            if text_year < year:
                texts[year].append(text)
                break
    except:
        print("Error: " + text)

api = get_api('masto.es', 'efemeridesbot')
last_id = 0
for year in years:
    if len(texts[year]):
        message = day + " de " + month + " de " + choice(texts[year]) + " #Efemérides"
        if last_id:
            status = api.status_post(message, in_reply_to_id=last_id, visibility="unlisted")
            last_id = status['id']
        else:
            status = api.status_post(message)
            last_id = status['id']
    sleep(60 * 60)

