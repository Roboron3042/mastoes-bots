from common import get_api
from common import list_read
from common import list_append
from common import list_write

# Messages
message = "¡Hola! Soy Roberto, el administrador de este servidor de Mastodon :mastodon: (https://masto.es)\n\nSi es tu primera vez en Mastodon, he preparado una guía para ayudarte a empezar 🙂 https://masto.es/@rober/109412552189056438 \n\nPuedes preguntarme lo que quieras si necesitas más ayuda. Sígueme para estar al tanto de las novedades sobre Mastodon y este servidor."


# Initialization
bot_name = 'bienvenibot'
api = get_api('masto.es', 'rober')
users = list_read(bot_name)
users_limited = list_read(bot_name + "_limited")
users_limited_new = []
notifications = api.notifications(types=["admin.sign_up"])

def try_dm(user):
    try:
        api.status_post("@" + user + " " + message, visibility="direct")
    except:
        users_limited_new.append(user)

for user in users_limited:
    try_dm(user)

for n in notifications:
    # Message new users
    user = n['account']['acct']
    if n['type'] == "admin.sign_up" and user not in users:
        list_append(bot_name, user)
        try_dm(user)

list_write(bot_name + "_limited", users_limited_new)
