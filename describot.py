from common import get_api
from common import list_append
from common import list_read
from common import list_write
from common import get_new_notifications

message = "¡Hola! He detectado que has publicado imágenes o vídeo sin texto alternativo. Añadir una descripción de texto alternativa a tus vídeos e imágenes es esencial para que las personas con alguna discapacidad visual puedan disfrutar de nuestras publicaciones. \n\n Por favor, considera añadir texto alternativo a tus publicaciones la próxima vez (o edita esta publicación para añadírselo). Si necesitas ayuda para saber cómo hacerlo, consulta la publicación fijada en mi perfil: https://masto.es/@TeLoDescribot/110249937862873987 \n\n ¡Gracias por hacer de este espacio un lugar más accesible para todos! \n\n Bip bop. Esta es una cuenta automatizada, si no quieres que te mencione más, eres libre de bloquearme."


bot_name = 'describot'
api_mastoes = get_api('masto.es', bot_name)
max_posts=20
warned=[]

def check_timeline(domain, api_external, timeline_name = 'local'):
    last_ids = list_read(bot_name + "_" + domain + "_last_ids")
    warned.extend(list_read(bot_name + "_" + domain))
    timeline = api_external.timeline(timeline=timeline_name, limit=max_posts)
    new_last_ids=[]
    for post in timeline:
        new_last_ids.append(post['id'])
    for i in range(0, len(timeline) - 2):
        post = timeline[i]
        if str(post['id']) not in last_ids and (str(post['account']['acct']) not in warned or timeline_name == 'home'): 
            for media in post['media_attachments']:
                if media['description'] is None:
                    print('Warning ' + post['account']['acct'])
                    api_mastoes.status_reply(post, message, visibility="unlisted")
                    warned.append(post['account']['acct'])
                    if domain != 'home':
                        list_append(bot_name + "_" + domain, post['account']['acct'])
                    break
    list_write(bot_name + "_" + domain + "_last_ids", new_last_ids)

notifications = get_new_notifications(api_mastoes, bot_name, types=['follow'])
for n in notifications:
    print("Following: " + n['account']['acct'])
    api_mastoes.account_follow(n['account']['id'])


check_timeline('masto.es', api_mastoes)
check_timeline('home', api_mastoes, timeline_name='home')
