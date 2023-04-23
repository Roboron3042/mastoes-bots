from mastodon import Mastodon
from sys import exit

def get_api(url, token_name = ""):
    if token_name:
        try:
            file = open('token/' + token_name, 'r')
        except FileNotFoundError:
            sys.exit()
        else:
            token = file.read().splitlines()[0]
            file.close()
    else:
        token = ""

    return Mastodon(access_token = token, api_base_url = url)

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

