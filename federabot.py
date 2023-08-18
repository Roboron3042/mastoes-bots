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
    'mastorock.com',
    'frikiverse.zone',
    '41020.social',
    'tuiter.rocks',
    'mastorock.com',
    'meetiko.org',
    'mastodon.cr',
    # Relay nobigtech.es
    'sindicato.social',
    'mastodon.uy',
    'red.niboe.info',
    'nobigtech.es',
    'loa.masto.host',
    'bizkaia.social',
    'mstdn.mx',
    'federa.social',
    # Non-spanish accounts >:(
    'sportsbots.xyz',
    'press.coop'
]

bot_name = 'federabot'
api_mastoes = get_api('masto.es', 'rober')

following = list_read(bot_name)
date_recent = datetime.today() - timedelta(days=30)

follows_limited = list_read(bot_name + '_follows_limited')
dms_limited = list_read(bot_name + '_messages_limited')

list_write(bot_name + "_follows_limited", [])
list_write(bot_name + "_messages_limited", [])

def try_follow(user_id):
    try:
        api_mastoes.account_follow(user_id)
    except:
        list_append(bot_name + '_follows_limited', str(user_id))
        print("Fail to follow. Will retry next time")

def try_dm(username, user_domain):
    try:
        api_mastoes.status_post("@" + username + " " + get_message(user_domain), visibility="direct")
        print("Welcome new user: " + username)
    except:
        list_append(bot_name + '_messages_limited', username)
        print("Fail to welcome new user: " + username + ". Will retry next time")

def check_follows():
    notifications = api_mastoes.notifications(types=["follow"])
    for n in notifications:
        username = n['account']['acct']
        user_domain = username.split("@")[1] if "@" in username else "masto.es"
        date_created = n['account']['created_at'].replace(tzinfo=None)
        if username not in following:
            print("Following: " + username)
            try_follow(n['account']['id'])
            following.append(username)
            list_append(bot_name, username)
            if date_created > date_recent and user_domain == 'mastodon.social':
                try_dm(username, user_domain)

def check_timeline(domain, timeline_name = 'public', api_external=None):
    
    if api_external is None:
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
            if date_created > date_recent and timeline_name == 'local' and user_domain == 'mastodon.social':
                try_dm(username, user_domain)
            print("Following: " + username)
            user = api_mastoes.search_v2("@" + username + " ", result_type="accounts")["accounts"][0]
            # Retrieve the post, it could be the first
            api_mastoes.search_v2(post['url'], result_type="posts")
            following.append(username)
            list_append(bot_name, username)
            try_follow(user['id'])

    if len(timeline) > 0:
        list_write(bot_name + "_last_id_" + domain, [timeline[0]['id']])


print('\nChecking previous attempts...')
for user_id in follows_limited:
    try_follow(user_id)

for username in dms_limited:
    user_domain = username.split("@")[1]
    try_dm(username, user_domain)

print('\nChecking follows...')
check_follows()


api=get_api('mastodon.social', bot_name + "_mastodon_social")
print('\nChecking mastodon.social local TL')
check_timeline('mastodon.social', 'local', api_external=api)
print('\nChecking mastodon.social federated TL')
check_timeline('mastodon.social', 'public', api_external=api)


print('\nChecking masto.es federated TL')
api=get_api('masto.es', bot_name)
check_timeline('masto.es', api_external=api)
