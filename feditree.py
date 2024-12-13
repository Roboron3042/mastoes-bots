from PIL import Image
from common import get_api, get_new_notifications, list_read, list_append
import datetime
import gettext
import requests

coordinates = [
    (350,200),
    (275,350),
    (425,350),
    (200,500),
    (350,500),
    (500,500),
    (125,650),
    (275,650),
    (425,650),
    (575,650),
]

def get_ordered_accounts_ids(account_id):
    current_year = datetime.date.today().year
    accounts = {}
    stop = False
    max_id=None
    loops = 0
    while stop == False:
        statuses = api.account_statuses(account_id, exclude_reblogs=True, max_id=max_id, limit=80)
        for status in statuses:
            if(status.created_at.year < current_year):
                stop = True
                break
            for mention in status.mentions:
                if mention.id not in accounts:
                    accounts[mention.id] = 1
                else:
                    accounts[mention.id] = accounts[mention.id] + 1
            max_id=status.id
        loops = loops + 1
        if loops > 10 :
            stop = True
    accounts_list = sorted(accounts, key=accounts.get, reverse=True)
    accounts_list.insert(0,account_id)
    accounts_list.pop
    return accounts_list

def get_accounts(accounts_ids):
    accounts = []
    for i in range(len(accounts_ids)):
        account = api.account(accounts_ids[i])
        if "nobot" not in account.note: 
            accounts.append(account)
        if len(accounts) == len(coordinates): 
            break
    return accounts


def create_image(accounts):
    with Image.open("feditree/fediverse-christmas-tree.png") as feditree:
        feditree.load()
    with Image.open("feditree/bola_radio.png") as bola_radio:
        bola_radio.load()
    with Image.open("feditree/bola_mask.png") as bola_mask:
        bola_mask.load()
    for i in range(min(len(accounts),len(coordinates))):
        account = api.account(accounts[i])
        avatar_url = account.avatar_static
        avatar_data = requests.get(avatar_url).content
        with open('feditree/avatar.png', 'wb') as handler:
            handler.write(avatar_data)
        with Image.open('feditree/avatar.png') as avatar:
            avatar.load()
        avatar = avatar.resize((100,100)).convert("RGB")
        avatar.paste(bola_radio, (0,0), bola_radio)
        feditree.paste(avatar, coordinates[i], bola_mask)
    feditree.save("feditree/feditree.png")
    bola_radio.close()
    bola_mask.close()
    avatar.close()
    feditree.close()
    description = _("A simple drawing of a fir tree, crowned with the pentagon symbolizing the Fediverse.")
    description = description + " " + _("There are some christmas bulbs hanging in the tree, which have the avatars of the mentioned accounts inside.")
    description = description + " " + _("The accounts appear in the tree in the same order as the mentions, from top to bottom and from left to right.")
    description = description + " " + _("The order symbolizes the number of interactions, from most to least.")
    description = description + "\n\n" + _("The Fediverse logo was created by @eudaimon@fe.disroot.org and the tree design was obtained from https://freesvgdesigns.com")
    return api.media_post("feditree/feditree.png", description=description)


bot_name = "feditree"
localedir = './locales'
api = get_api('masto.es', "test")
notifications = get_new_notifications(api, bot_name, ["mention"])
previous_ids = list_read(bot_name + "_previous_ids")

for notification in notifications:
    i18n = gettext.translation(bot_name, localedir, fallback=True, languages=[notification.status.language])
    i18n.install()
    if str(notification.account.id) in previous_ids:
        status = "@" + notification.account.acct + " "
        status += _("I have already generated a feditree for you this year. Try again next year!")
        api.status_post(status, visibility="direct", in_reply_to_id=notification.status.id)
        continue
    else:
        list_append(bot_name + "_previous_ids", previous_ids)
    accounts_ids = get_ordered_accounts_ids(notification.account.id)
    accounts = get_accounts(accounts_ids)
    image = create_image(accounts)
    status = _("These are the people who have adorned the #FediTree of") + " @" + notification.account.acct + ":"
    for account in accounts:
        if account.acct == notification.account.acct: 
            continue
        status += " @/" + account.acct
    api.status_post(status, media_ids=image, visibility="unlisted", in_reply_to_id=notification.status.id)
    previous_ids.append(notification.account.id)
