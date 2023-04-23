from common import get_api
from common import list_append
from common import list_read
from common import list_write
from datetime import datetime, timedelta

def get_message(user_domain):
    return "¡Hola! Veo que es tu primera vez en Mastodon, ¡te doy la bienvenida si así es!\n\nSoy Roberto, el administrador del servidor de Mastodon en español https://masto.es. Ya ves que aunque estemos en servidores diferentes, somos capaces de comunicarnos gracias al modelo federado de Mastodon :mastodance:\n\nAunque yo no sea tu administrador en " + user_domain + ", si necesitas ayuda para empezar puedes consultar la guía que he preparado para mis usuarios: https://masto.es/@rober/109412552189056438\n\nY si tienes alguna duda más, estaré encantado de ayudarte, solo responde a este mensaje privado 🙂"

excluded_domains = [
    'masto.es',
    # Relay tkz.one
    'mst.universoalterno.es',
    'masto.friki.lol',
    'mastodon.com.py',
    'comunidad.nvda.es',
    'mast.lat',
    'viajes.social',
    'ferrocarril.net',
    'tkz.one',
    'mastorol.es',
    'shrimply.social',
    'mstdn.jmiguel.eu',
    # Relay chocoflan
    'mk.mistli.net',
    'izta.mistli.net',
    'novoa.nagoya',
    'quey.la',
    'social.hispabot.freemyip.com',
    'mastodon.uy',
    'mstdn.mx',
    'el-spot.xyz',
    'mastodonperu.xyz',
    '41020.social',
    #'mast.lat',
    'acc4e.com',
    #'mastodon.com.py',
    #'shrimply.social',
    'nonomastodon.redirectme.net',
    'arguos.com',
    'social.wikimedia.es',
    'tarugo.ddns.net',
    'pleroma.lyricaltokarev.fun',
    # Relay nobigtech.es
    'sindicato.social',
    #'mastodon.uy',
    'red.niboe.info',
    'nobigtech.es',
    'loa.masto.host',
    'bizkaia.social',
    #'mstdn.mx',
    'federa.social'
]

bot_name = 'federabot'
api_mastoes = get_api('masto.es', 'rober')
following = list_read(bot_name)
date_recent = datetime.today() - timedelta(days=7)

def check_timeline(domain, timeline_name = 'public'):
    api_external = get_api(domain)
    last_id = list_read(bot_name + "_last_id_" + domain)[0]
    timeline = api_external.timeline(
        timeline=timeline_name, 
        since_id=last_id, 
        remote=(True if timeline_name == 'public' else False)
    )

    for post in timeline:
        if timeline_name == 'local':
            username = post['account']['acct'] + "@" + domain
            user_domain = domain
        else:
            username = post['account']['acct']
            user_domain = username.split("@")[1]
        if (
            post['language'] == 'es' 
            and not "nobot" in post['account']['note'] 
            and user_domain not in excluded_domains 
            and username not in following
        ):
            date_created = post['account']['created_at'].replace(tzinfo=None)
            if date_created > date_recent and user_domain == 'mastodon.social':
                print("New user: " + username)
                api_mastoes.status_post("@" + username + " " + get_message(user_domain), visibility="direct")
            print("Following: " + username)
            user = api_mastoes.search_v2("@" + username + " ", result_type="accounts")["accounts"][0]
            # Retrieve the post, it could be the first
            api_mastoes.search_v2(post['url'], result_type="posts")
            api_mastoes.account_follow(user['id'])
            following.append(username)
            list_append(bot_name, username)

    if len(timeline) > 0:
        list_write(bot_name + "_last_id_" + domain, [timeline[0]['id']])

check_timeline('masto.es')
check_timeline('mastodon.social', 'local')
