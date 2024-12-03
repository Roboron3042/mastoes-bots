from common import get_api, get_gender, list_read
from random import choice
from insultabot import get_insulto_inclusivo
    
bot_name = 'insultabot'
api = get_api('masto.es', bot_name)

followers = api.account_followers(api.me().id, limit=80)
followers = api.fetch_remaining(followers)
insultos = list_read(bot_name + "_insultos")
choosen_insulto = choice(insultos)
choosen_user = choice(followers)
gender = get_gender(choosen_user)
insulto = get_insulto_inclusivo(choosen_insulto, gender)
api.status_post("@" + choosen_user.username + " ¡" + insulto + "!", visibility="unlisted" )
