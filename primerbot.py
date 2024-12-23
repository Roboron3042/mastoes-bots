
from common import get_api, get_new_notifications

# Initialization
bot_name = 'primerbot'
api = get_api('masto.es', bot_name)
notifications = get_new_notifications(api, bot_name, types=["mention"])

for n in notifications:
    user = n['account']['acct']
    user_id = n['account']['id']
    statuses = []
    if len(user.split('@')) > 1:
        user_domain = user.split("@")[1]
        api_external = get_api(user_domain)
        result = api_external.search_v2(user, result_type="accounts", resolve=False)
        user_id = result['accounts'][0]['id']
        statuses = api_external.account_statuses(id=user_id, min_id=1, limit=1, exclude_reblogs=True)
    else:
        user_id = n['account']['id']
        statuses = api.account_statuses(id=user_id, min_id=1, limit=1, exclude_reblogs=True)

    if len(statuses):
        api.status_reply(n['status'], "Tu primera publicación (o la más antigua que he podido encontrar) es: " + statuses[0]['url'])
