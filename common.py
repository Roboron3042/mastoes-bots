from mastodon import Mastodon
from sys import exit

def get_api(url, token_name = ""):
    if token_name:
        try:
            file = open('token/' + token_name, 'r')
        except FileNotFoundError:
            print('Token not found for ' + token_name)
            exit()
        else:
            token = file.read().splitlines()[0]
            file.close()
    else:
        token = ""

    return Mastodon(access_token = token, api_base_url = url, ratelimit_method='throw', version_check_mode='none')

def list_read(name):
    try:
        file = open('list/' + name, 'r')
    except FileNotFoundError:
        file = open('list/' + name, 'x')
        file.close()
        return []
    else:
        list = file.read().splitlines()
        file.close()
        return list

def list_write(name, values):
    file = open('list/' + name, 'w')
    for value in values:
        file.write(str(value) + '\n')
    file.close()

def list_append(name, value):
    file = open('list/' + name, 'a')
    file.write(value + '\n')
    file.close()

# It is not safe to get notifications from "last_id" because some may have been deleted
def get_new_notifications(api, bot_name, types=None):
    last_notifications=list_read(bot_name + '_last_notifications')
    notifications = api.notifications(types=types)
    new_notifications = []
    new_notifications_ids = []
    max_notification = 0
    if len(notifications) < 2:
        max_notification = len(notifications)
    else:
        max_notification = len(notifications) // 2

    for i in range(0, max_notification):
        if str(notifications[i]['id']) not in last_notifications:
            new_notifications.append(notifications[i])

    for n in notifications:
        new_notifications_ids.append(n['id'])

    list_write(bot_name + "_last_notifications", new_notifications_ids)
    return new_notifications

women_pronouns = ["she","her","ella","illa"]
nb_pronouns = ["they","them","elle", "ille"]

def is_gender(pronouns, account):
    for pronoun in pronouns:
        if(pronoun in account.display_name.lower()):
            return True
        for field in account.fields:
            if(pronoun in field.value.lower()):
                return True
        if(pronoun in account.note.lower()):
            return True
    return False

def get_gender(account):
    if(is_gender(nb_pronouns, account)):
        return 2
    if(is_gender(women_pronouns,account)):
        return 1
    return 0
