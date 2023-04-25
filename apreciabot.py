from bs4 import BeautifulSoup
from common import get_api
from common import list_append
from common import list_read
from common import list_write
import json
import os
import click
import click_config_file


class load_custom_messages():
    def __init__(self, custom_message_file):
        if os.path.exists(custom_message_file):
            with open(custom_message_file, 'r') as messages_pointer:
                custom_messages = json.load(messages_pointer)
                self.custom_messages = custom_messages

class apreciabot():
    def __init__(self, **kwargs):
        # Initialization
        self.kwargs = kwargs
        self.custom_messages = load_custom_messages(self.kwargs['custom_message_file']).custom_messages
        bot_name = self.custom_messages[self.kwargs['language']]['apreciabot']['bot_name']

        # Messages
        mensaje = self.custom_messages[self.kwargs['language']]['apreciabot']['mensaje']
        mensaje_croqueta = self.custom_messages[self.kwargs['language']]['apreciabot']['mensaje_croqueta']
        mensaje_mismo = self.custom_messages[self.kwargs['language']]['apreciabot']['mensaje_mismo']
        mensaje_nobot = self.custom_messages[self.kwargs['language']]['apreciabot']['mensaje_nobot']
        mensaje_aviso = self.custom_messages[self.kwargs['language']]['apreciabot']['mensaje_aviso']
        mensaje_error = self.custom_messages[self.kwargs['language']]['apreciabot']['mensaje_error']
        mensaje_no_encontrado = self.custom_messages[self.kwargs['language']]['apreciabot']['mensaje_no_encontrado']
        mensaje_muestra_aprecio_enviada = self.custom_messages[self.kwargs['language']]['apreciabot']['mensaje_muestra_aprecio_enviada']

        api = get_api(self.kwargs['instance_name'], bot_name)
        last_ids = list_read(bot_name)
        max_notifications=10
        new_last_ids=[]
        notifications = api.notifications(types=["mention"],limit=max_notifications)
        for n in notifications:
            new_last_ids.append(n['id'])

        # Some notifications may have been deleted since last fetch
        # Therefore, it is better to check less than the maximum number of notifications
        if len(notifications) < 1:
            print(self.custom_messages[self.kwargs['language']]['apreciabot']['no_notifications'])
        else:
#            for i in range(0, max_notifications - 5):
# # (adelgado) I'm not sure why this previous loop, but if there are less than 5 notifications,
# there is an exception since there are not enought items in the list to fetch one. So I changed
# it to go throw all notifications and do only those before the last 5.
            i = 0
            for n in notifications:
                i += 1
                if i < max_notifications - 5:
                    if str(n['id']) not in last_ids:
                        # Mentions data are HTML paragraphs so we delete everything between <> to clean it up
                        content = BeautifulSoup(n['status']['content'], "html.parser").get_text().split(" ")
                        try:
                            first_mention = content[0]
                            target = "@" + content[1]
                            user = "@" + n['account']['acct']
                        except:
                            api.status_reply(n['status'], mensaje_error)
                            continue
                        # The bot is meant to be anonymous so only allow directs
                        if n['status']['visibility'] == "direct":
                            if user == target:
                                api.status_reply(n['status'], mensaje_mismo, visibility="unlisted")
                            else:
                                # Find account if it is not known by the server
                                api.search(target, result_type="accounts")
                                try:
                                    bio = api.account_lookup(target)
                                except:
                                    api.status_post(user + mensaje_no_encontrado, in_reply_to_id=n['status']['id'], visibility="direct" )
                                else:
                                    if "nobot" in bio['note']:
                                        api.status_reply(n['status'], mensaje_nobot)
                                    else:
                                        #api.status_post(mensaje + target + "!", in_reply_to_id=n['status']['id'], visibility="unlisted")
                                        if ("croqueta" in content 
                                            or "croquetas" in content 
                                            or '"croqueta"' in content 
                                            or '"croquetas"' in content
                                        ):
                                            new_status = api.status_post(target + " " + mensaje_croqueta, visibility="unlisted")
                                        else: 
                                            new_status = api.status_post(mensaje + target + "!", visibility="unlisted")
                                        api.status_reply(n['status'], mensaje_muestra_aprecio_enviada + new_status['url'], visibility="direct")
                        elif first_mention == "@" + bot_name and n['status']['in_reply_to_id'] == None:
                            api.status_reply(n['status'], mensaje_aviso, visibility='direct')

        list_write(bot_name, new_last_ids)

@click.command()
@click.option('--language', '-l', default='es', help="Language.")
@click.option('--custom-message-file', '-j', default='custom_messages.json', help='JSON file containing the messages.')
@click.option('--instance-name', '-i', default='masto.es', help='Instance FQDN')
@click_config_file.configuration_option()
def __main__(**kwargs):
    return apreciabot(**kwargs)

if __name__ == "__main__":
    __main__()

