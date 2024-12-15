from PIL import Image
from common import get_api, get_new_notifications, list_read, list_append
import datetime
import gettext
import requests
import traceback

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

def get_ordered_accounts_ids(account_id, _api):
    current_year = datetime.date.today().year
    accounts = {}
    stop = False
    max_id=None
    loops = 0
    while stop == False:
        statuses = _api.account_statuses(account_id, exclude_reblogs=True, max_id=max_id, limit=80)
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

def get_accounts(accounts_ids, _api):
    accounts = []
    for i in range(len(accounts_ids)):
        account = _api.account(accounts_ids[i])
        if "nobot" not in account.note.lower() and account not in accounts: 
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
        account = accounts[i]
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
domain = "masto.es"
api = get_api(domain, bot_name)
notifications = get_new_notifications(api, bot_name, ["mention"])
previous_ids = list_read(bot_name + "_previous_ids")

for notification in notifications:
    lang = notification.status.language
    if lang is None:
        lang = "en"
    try:
        i18n = gettext.translation(bot_name, localedir, fallback=True, languages=[lang])
        i18n.install()
        if str(notification.account.id) in previous_ids:
            print("Skipping generation, a tree was already generated for: " + notification.account.acct)
            status = "@" + notification.account.acct + " "
            status += _("I have already generated a feditree for you this year. Try again next year!")
            # Currently disabled due to API limits
            #api.status_post(status, visibility="direct", in_reply_to_id=notification.status.id)
            continue
        try:
            print("Generating a tree for: " + notification.account.acct)
            external_domain = notification.account.acct.split("@")[1]
            external_api = get_api(external_domain)
            external_account = external_api.account_lookup(notification.account.acct)
            accounts_ids = get_ordered_accounts_ids(external_account.id, external_api)
            accounts = get_accounts(accounts_ids, external_api)
        except:
            print(traceback.format_exc())
            print("External api failed, using internal api instead.")
            accounts_ids = get_ordered_accounts_ids(notification.account.id, api)
            accounts = get_accounts(accounts_ids, api)
        image = create_image(accounts)
        status = _("These are the people who have adorned the #FediTree of") + " @" + notification.account.acct + ":"
        for account in accounts:
            if account.username == notification.account.username: 
                continue
            status += " \n- " + account.acct
            if len(account.acct.split("@")) == 1:
                status += "@" + domain
        api.status_post(status, media_ids=image, visibility="unlisted", in_reply_to_id=notification.status.id, language=lang)
        previous_ids.append(notification.account.id)
        list_append(bot_name + "_previous_ids", str(notification.account.id))
    except:
        print(traceback.format_exc())
        status = "@" + notification.acct + " "
        status += _("An error ocurred. I have probably reached my posting limit. Please try again in an hour or contact my creator if I keep failing.")
        try:
            api.status_post(status, visibility="direct", in_reply_to_id=notification.status.id, language=lang)
        except:
            continue
