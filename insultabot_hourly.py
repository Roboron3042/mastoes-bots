from common import get_api, get_gender, list_read
from random import choice
from insultabot import get_insulto_inclusivo

mensaje_sufjos = [
    "Solo para uso de personal autorizado, como el que tengo aquí colgado.",
    "Todos los derechos reservados. Y todos los izquierdos también.",
    "Puede ejercer su derecho a desestimiento si contrata un abogado que me la agarre con la mano.",
    "Prohibida su comercialización, salvo si me hace millonario.",
    "Aproveche nuestro descuento de temporada para suscribirse a más injurias.",
    "Se admiten devoluciones en caliente.",
    "Rellene nuestra encuesta de calidad solo si lo ha disfrutado.",
    "Contacte con nuestro servicio de soporte en uve doble uve doble uve doble me gusta que me ignoren punto com."
]
    
bot_name = 'insultabot'
api = get_api('masto.es', bot_name)

followers = api.account_followers(api.me().id, limit=80)
followers = api.fetch_remaining(followers)
insultos = list_read(bot_name + "_insultos")
choosen_insulto = choice(insultos)
choosen_user = choice(followers)
gender = get_gender(choosen_user)
insulto = get_insulto_inclusivo(choosen_insulto, gender).capitalize()
mensaje = "@" + choosen_user.acct + " ¡" + insulto + "!\n\n"
mensaje = mensaje + "Insulto gratuito periódico patrocinado por Insultabot para sus seguidores."
mensaje = mensaje + " " + choice(mensaje_sufjos)
api.status_post(mensaje, visibility="unlisted")
