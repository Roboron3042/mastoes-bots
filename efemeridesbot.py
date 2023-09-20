import requests
from bs4 import BeautifulSoup
from common import get_api
from datetime import datetime
from random import choice
from locale import setlocale, LC_ALL
from collections import Counter

def append_random_text(message, texts):
    _message = message
    _message += "\n\n- " + choice(texts)
    if len(_message) < 1000:
        return _message
    return message


setlocale(LC_ALL, 'es_ES.UTF-8º')

today = datetime.today()
day = today.strftime('%d')
month = today.strftime('%B')

r = requests.get('https://www.hoyenlahistoria.com/efemerides/' + month + '/' + day)
html = BeautifulSoup(r.text, "html.parser")
basic_events = html.find_all('li', class_='event')
featured_events = html.find_all('p')
events = basic_events + featured_events[1 : -1]

texts1000 = []
texts1450 = []
texts1800 = []
texts1900 = []
texts1950 = []
texts2000 = []
texts2050 = []

for event in events:
    text = event.get_text()
    year = int(text.split(" ")[0])
    if year <= 1000:
        texts1000.append(text)
    elif year <= 1450:
        texts1450.append(text)
    elif year <= 1800:
        texts1800.append(text)
    elif year <= 1900:
        texts1900.append(text)
    elif year <= 1950:
        texts1950.append(text)
    elif year <= 2000:
        texts2000.append(text)
    elif year <= 2050:
        texts2050.append(text)

message = "Tal día como hoy, en el año:"
message = append_random_text(message, texts1000)
message = append_random_text(message, texts1450)
message = append_random_text(message, texts1800)
message = append_random_text(message, texts1900)
message = append_random_text(message, texts1950)
message = append_random_text(message, texts2000)
message = append_random_text(message, texts2050)

print(message)
print(len(message))

api = get_api('masto.es', 'efemeridesbot')
api.status_post(message)
