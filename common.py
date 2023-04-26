import mastodon
from sys import exit
import re

def get_api(url, token_name = ""):
    if token_name:
        try:
            file = open('token/' + token_name, 'r')
        except FileNotFoundError:
            print('Token not found for ' + token_name + ' in "token/'+ token_name + '"')
            exit()
        else:
            token = file.read().splitlines()[0].strip()
            file.close()
    else:
        token = ""

    return mastodon.Mastodon(access_token = token, api_base_url = url)

def list_read(name):
    try:
        file = open('list/' + name, 'r')
    except FileNotFoundError:
        file = open('list/' + name, 'x')
        file.close()
        return [""]
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

    for i in range(0, len(notifications) // 2):
        if str(notifications[i]['id']) not in last_notifications:
            new_notifications.append(notifications[i])

    for n in notifications:
        new_notifications_ids.append(n['id'])

    list_write(bot_name + "_last_notifications", new_notifications_ids)
    return new_notifications

def status_reply(api, post, message, visibility):
    try:
        api.status_reply(post, message, visibility=visibility)
    except mastodon.errors.MastodonAPIError as error:
        match_len_limit = re.search(r'Text character limit of ([0-9]*) exceeded', str(error))
        if match_len_limit:
            max_post_size = int(match_len_limit.group(1)) - 10
            #split_message = [message[i:i+max_post_size] for i in range(0, len(message), max_post_size)]
            split_message = message.split('\n\n')
            counter = 1
            for chunk_message in split_message:
                try:
                    api.status_reply(post, f"{chunk_message} {counter}/{len(split_message)}", visibility=visibility)
                    counter += 1
                except mastodon.errors.MastodonAPIError as error:
                    print(f"Error posting: {error}")
                    exit(1)
        else:
            print(f"Error posting: {error}")
            exit(1)
