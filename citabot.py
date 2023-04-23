import requests
from bs4 import BeautifulSoup
from common import get_api

# Get the quote of the day
r = requests.get('https://proverbia.net/frase-del-dia')
content = BeautifulSoup(r.text, "html.parser").find_all('blockquote')
message = content[0].p.get_text() + "\n\n"
message += "—" + content[0].a.get_text() + " " + content[0].em.get_text()

api = get_api('masto.es', 'citabot')
api.status_post(message)
