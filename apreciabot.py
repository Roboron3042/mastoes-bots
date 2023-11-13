import re
from bs4 import BeautifulSoup
from common import get_api
from common import list_append
from common import list_read
from common import list_write


# Messages
mensaje = "Alguien que te aprecia mucho quiere recordarte que eres una persona maravillosa :ablobcatheartsqueeze: ¡Sigue así, "
mensaje_croqueta = "Alguien que te aprecia mucho quiere enviarte croquetas :croqueta: :croqueta: :croqueta:"
mensaje_cumple = ["Alguien me ha revelado que hoy es tu día, ", ". ¡Feliz cumpleaños de su parte! :blobcatbirthday:"]
mensaje_mismo = "La persona más importante que debes apreciar eres tú. ¡Eres increíble! ❤"
mensaje_nobot = "La cuenta objetivo tiene la etiqueta #nobot en su biografía. ¡No tengo poder aquí!"
mensaje_aviso = "Has intentado apreciar a alguien pero no has usado un mensaje directo/privado. ¡Tienes que mencionarme en un mensaje directo/privado para que funcione!"
mensaje_error = "No pude procesar tu apreciación. ¡Asegúrate de no incluir saltos de línea ni otros caracteres extraños! El mensaje debería ser tal que así: \"@apreciabot@masto.es usuario@servidor\n"
mensaje_no_encontrado = " No se pudo encontrar la cuenta del usuario especificado. \n\nRevisa que has escrito bien  la cuenta con el formato \"usuario@servidor\" (por ejemplo, rober@masto.es, excluyendo el primer @ para evitar mencionarlo).\n\nSi lo has mencionado por error, ¡borra el mensaje antes de que se de cuenta!"

# Initialization
bot_name = 'apreciabot'
api = get_api('masto.es', bot_name)
last_ids = list_read(bot_name)
max_notifications=10
new_last_ids=[]
notifications = api.notifications(types=["mention"],limit=max_notifications)
no_unicode_spaces_pattern = r"[\u200B-\u200D\u202A\u202C\uFEFF]"
mode_croqueta_words=["croqueta", "croquetas"]
mode_cumple_words=["cumple", "cumpleaños", "felicidades"]

def check_mode(mode_words, content):
    for word in mode_words:
        if ( (word in content) or ( ('"' + word +'"') in content) ):
            return True
    return False

for n in notifications:
    new_last_ids.append(n['id'])

# Some notifications may have been deleted since last fetch
# Therefore, it is better to check less than the maximum number of notifications
for i in range(0, max_notifications - 5):
    n = notifications[i]
    if str(n['id']) not in last_ids:
        # Mentions data are HTML paragraphs so we delete everything between <> to clean it up
        rawContent = BeautifulSoup(n['status']['content'], "html.parser").get_text()
        content = re.sub(no_unicode_spaces_pattern, "", rawContent).split(" ")
        try:
            first_mention = content[0]
            target = "@" + content[1]
            user = "@" + n['account']['acct']
        except:
            api.status_reply(n['status'], mensaje_error)
            continue
        # The bot is meant to be anonymous so only allow directs
        if n['status']['visibility'] == "direct":
            if user == target:
                api.status_reply(n['status'], mensaje_mismo, visibility="unlisted")
            else:
                # Find account if it is not known by the server
                api.search(target, result_type="accounts")
                try:
                    bio = api.account_lookup(target)
                except:
                    api.status_post(user + mensaje_no_encontrado, in_reply_to_id=n['status']['id'], visibility="direct" )
                else:
                    if "nobot" in bio['note']:
                        api.status_reply(n['status'], mensaje_nobot)
                    else:
                        #api.status_post(mensaje + target + "!", in_reply_to_id=n['status']['id'], visibility="unlisted")
                        if check_mode(mode_croqueta_words, content):
                            new_status = api.status_post(target + " " + mensaje_croqueta, visibility="unlisted")
                        elif check_mode(mode_cumple_words, content):
                            new_status = api.status_post(mensaje_cumple[0] + target + mensaje_cumple[1], visibility="unlisted")
                        else: 
                            new_status = api.status_post(mensaje + target + "!", visibility="unlisted")
                        api.status_reply(n['status'], 'Tu muestra de aprecio ha sido enviada ❤️ ' + new_status['url'], visibility="direct")
        elif first_mention == "@apreciabot" and n['status']['in_reply_to_id'] == None:
            api.status_reply(n['status'], mensaje_aviso, visibility='direct')

list_write(bot_name, new_last_ids)
