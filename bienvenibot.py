from common import get_api
from common import list_read
from common import list_append
from common import list_write

# Messages
message = "¡Hola, te doy la bienvenida a Mastodon :mastodon: en https://masto.es!\n\nTe recomiendo que empieces escribiendo una publicación con la etiqueta #presentación y tus intereses para darte a conocer.\n\n¡Espero que tengas un buen comienzo! Si necesitas ayuda, ¡cuenta conmigo!"


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
