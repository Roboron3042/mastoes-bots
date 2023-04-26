#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from bs4 import BeautifulSoup
from common import get_api
from common import list_append
from common import list_read
from common import list_write
from common import status_reply
import mastodon
import json
import os
import click
import click_config_file
import logging
from logging.handlers import SysLogHandler
import sys


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
        if 'log_file' not in kwargs or kwargs['log_file'] is None:
            log_file = os.path.join(os.environ.get('HOME', os.environ.get('USERPROFILE', os.getcwd())), 'log', 'apreciabot.log')
        self.kwargs['log_file'] = log_file
        self._init_log()

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
            self._log.info(self.custom_messages[self.kwargs['language']]['apreciabot']['no_notifications'])
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
                            status_reply(api, n['status'], mensaje_error)
                            continue
                        # The bot is meant to be anonymous so only allow directs
                        if n['status']['visibility'] == "direct":
                            if user == target:
                                status_reply(api, n['status'], mensaje_mismo, visibility="unlisted")
                            else:
                                # Find account if it is not known by the server
                                api.search(target, result_type="accounts")
                                try:
                                    bio = api.account_lookup(target)
                                except:
                                    api.status_post(user + mensaje_no_encontrado, in_reply_to_id=n['status']['id'], visibility="direct" )
                                else:
                                    if "nobot" in bio['note']:
                                        status_reply(api, n['status'], mensaje_nobot)
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
                                        status_reply(api, n['status'], mensaje_muestra_aprecio_enviada + new_status['url'], visibility="direct")
                        elif first_mention == "@" + bot_name and n['status']['in_reply_to_id'] == None:
                            status_reply(api, n['status'], mensaje_aviso, visibility='direct')

        list_write(bot_name, new_last_ids)

    def _init_log(self):
        ''' Initialize log object '''
        self._log = logging.getLogger("apreciabot")
        self._log.setLevel(logging.DEBUG)

        sysloghandler = SysLogHandler()
        sysloghandler.setLevel(logging.DEBUG)
        self._log.addHandler(sysloghandler)

        streamhandler = logging.StreamHandler(sys.stdout)
        streamhandler.setLevel(logging.getLevelName(self.kwargs.get("debug_level", 'INFO')))
        self._log.addHandler(streamhandler)

        if 'log_file' in self.kwargs:
            log_file = self.kwargs['log_file']
        else:
            home_folder = os.environ.get('HOME', os.environ.get('USERPROFILE', ''))
            log_folder = os.path.join(home_folder, "log")
            log_file = os.path.join(log_folder, "apreciabot.log")

        if not os.path.exists(os.path.dirname(log_file)):
            os.mkdir(os.path.dirname(log_file))

        filehandler = logging.handlers.RotatingFileHandler(log_file, maxBytes=102400000)
        # create formatter
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        filehandler.setFormatter(formatter)
        filehandler.setLevel(logging.DEBUG)
        self._log.addHandler(filehandler)
        return True

@click.command()
@click.option("--debug-level", "-d", default="INFO",
    type=click.Choice(
        ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"],
        case_sensitive=False,
    ), help='Set the debug level for the standard output.')
@click.option('--log-file', '-L', help="File to store all debug messages.")
@click.option('--language', '-l', default='es', help="Language.")
@click.option('--custom-message-file', '-j', default='custom_messages.json', help='JSON file containing the messages.')
@click.option('--instance-name', '-i', default='masto.es', help='Instance FQDN')
@click_config_file.configuration_option()
def __main__(**kwargs):
    return apreciabot(**kwargs)

if __name__ == "__main__":
    __main__()

