from common import get_api, get_new_notifications

# Initialization
bot_name = 'primerbot'
api = get_api('masto.es', bot_name)

user = 'Roboron@im-in.space'
#user_id = '109352451286304753'
user_domain = user.split("@")[1]
print(user_domain)
api_external = get_api('im-in.space')
result = api_external.search_v2(user, result_type="accounts", resolve=False)
#print(accounts)
user_id = result['accounts'][0]['id']
statuses = api_external.account_statuses(id=user_id, min_id=1, limit=1, exclude_reblogs=True)
api.status_post(user + " Tu primera publicación (o la más antigua que he podido encontrar) es: " + statuses[0]['url'], visibility='direct')
