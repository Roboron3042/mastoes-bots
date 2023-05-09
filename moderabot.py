from common import get_api
from common import list_read
from common import list_append

bot_name = 'moderabot'
api = get_api('masto.es', bot_name)
notifications = api.notifications(types=["admin.sign_up"], limit=5)

# Vietnamese accounts
for n in notifications:
    if "Việt Nam" in n['account']['note'] or "chuẩn" in n['account']['note']:
        api.admin_account_moderate(n['account']['id'], action='suspend', send_email_notification=False)
        list_append(botname + "_banned", n['account']['acct'])

# Known spam accounts with similar names
names = list_read('moderabot_forbidden_names')
for name in names:
    result = api.search_v2(name, result_type='accounts', resolve=False)
    for account in result['accounts']:
        api.admin_account_moderate(account['id'], action='suspend', send_email_notification=False)
        list_append(bot_name + "_banned", account['acct'])

