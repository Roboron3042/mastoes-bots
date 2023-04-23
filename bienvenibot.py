from common import get_api
from common import list_read
from common import list_write

# Messages
message = "¡Hola! Soy Roberto, el administrador de este servidor de Mastodon :mastodon: (https://masto.es)\n\nSi es tu primera vez en Mastodon, he preparado una guía para ayudarte a empezar 🙂 https://masto.es/@rober/109412552189056438 \n\nPuedes preguntarme lo que quieras si necesitas más ayuda. Sígueme para estar al tanto de las novedades sobre Mastodon y este servidor."


# Initialization
bot_name = 'bienvenibot'
api = get_api('masto.es', 'rober')
last_ids = list_read(bot_name)
new_last_ids=[]
max_notifications=5
notifications = api.notifications(limit=max_notifications)
#notifications = mastodon.notifications(types=["admin.sign_up"], limit=5)
for n in notifications:
    new_last_ids.append(n['id'])

# Some notifications may have been deleted since last fetch
# Therefore, it is better to check less than the maximum number of notifications
for i in range(0, max_notifications - 1):
    n = notifications[i]
    if str(n['id']) not in last_ids:
        # Message new users
        username = n['account']['acct']
        if n['type'] == "admin.sign_up":
            api.status_post("@" + username + " " + message, visibility="direct")
        # Follow any user who interacted with our account
        #elif not "@" in username:
        elif n['type'] == "follow":
            api.account_follow(n['account']['id'])
        elif n['type'] == "admin.report":
            api.status_post("@Roboron@im-in.space Informe recibido de " + username, visibility="direct")

list_write(bot_name, new_last_ids)
