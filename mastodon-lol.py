from common import get_api
from common import list_read
from common import list_append

# Initialization
bot_name = 'mastodon_lol'
api_mastolol = get_api('mastodon.lol')
api_mastoes = get_api('masto.es', 'rober')
warned_users = list_read(bot_name)
message = "¡Hola! He detectado que sigues usando tu cuenta de https://mastodon.lol, pero ese servidor cerrará en menos de un mes (+info: https://mastodon.lol/@nathan/109836633022272265).\n\nAntes de que eso ocurra necesitarás mudar tu cuenta de Mastodon si quieres seguir usando la red. Como administrador de https://masto.es, te invito a unirte a nuestro servidor, pero da igual cuál servidor escojas para mudar tu cuenta, ¡lo importante es que lo hagas pronto!\n\nSi necesitas más información sobre cómo mudar tu cuenta, aquí te dejo un par de recursos:\n\n - Resumen: https://anartist.org/es/docs/social/como-migrar-de-una-instancia-a-otra \n - Guía más completa con capturas que escribió uno de mis usuarios: https://www.xataka.com/basics/como-migrar-tu-cuenta-mastodon-instancia-a-otra \n\n Naturalmente, también puedes preguntarme a mi si lo necesitas 🙂"

timeline = api_mastolol.timeline(timeline='local', limit=40)

for post in timeline:
    user = post['account']['acct']
    if post['language'] == 'es' and user not in warned_users:
        warned_users.append(user)
        list_append(bot_name, user)
        api_mastoes.status_post("@" + user + "@mastodon.lol " + message, visibility="direct")
