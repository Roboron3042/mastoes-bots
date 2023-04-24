import time
from common import get_api
from common import list_read

api = get_api('masto.es', 'temp')
mi_id = api.me()['id']
following = list_read('federabot')

accounts = api.account_followers(mi_id)
size = len(accounts)

while(size == 40):
    for account in accounts:
        if account['acct'] not in following:
            print('Siguiendo a ' + account['acct'])
            try: 
                api.account_follow(account['id'])
            except Exception:
                pass
    accounts = api.fetch_next(accounts)
    size = len(accounts)
    time.sleep(10)
