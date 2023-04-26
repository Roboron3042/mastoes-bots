#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from common import get_api
from common import list_append
from common import list_read
from common import list_write
from common import get_new_notifications
from common import status_reply
import mastodon
import json
import os
import click
import click_config_file
import mastodon
import re
import logging
from logging.handlers import SysLogHandler
import sys


class load_custom_messages():
    def __init__(self, custom_message_file):
        if os.path.exists(custom_message_file):
            with open(custom_message_file, 'r') as messages_pointer:
                custom_messages = json.load(messages_pointer)
                self.custom_messages = custom_messages

class describot():
    def __init__(self, **kwargs):
        # Initialization
        self.kwargs = kwargs
        if 'log_file' not in kwargs or kwargs['log_file'] is None:
            log_file = os.path.join(os.environ.get('HOME', os.environ.get('USERPROFILE', os.getcwd())), 'log', 'describot.log')
        self.kwargs['log_file'] = log_file
        self._init_log()

        self.custom_messages = load_custom_messages(self.kwargs['custom_message_file']).custom_messages
        self.messages = self.custom_messages[self.kwargs['language']]['describot']
        self.bot_name = self.messages['bot_name']

        self.api_internal = get_api(self.kwargs['instance_name'], self.bot_name)
        self.max_posts=20
        self.warned=[]

        self._log.debug('Getting list of followed...')
        self.following = list_read(self.bot_name + "_following")
        self._log.debug('Getting new notifications...')
        notifications = get_new_notifications(self.api_internal, self.bot_name, types=['follow'])
        self._log.debug(f"Gotten {len(notifications)} notifications")
        for n in notifications:
            self._log.debug(n)
            if n['account']['acct'] not in self.following:
                self._log.info("Following: " + n['account']['acct'])
                api_internal.account_follow(n['account']['id'])
                self.following.append(n['account']['acct'])
                list_append(self.bot_name + "_following", n['account']['acct'])
            else:
                self._log.debug(f"Already following {n['account']['acct']}.")

        self.check_timeline(self.kwargs['instance_name'], self.api_internal)
        self.check_timeline('home', self.api_internal, timeline_name='home')


    def check_timeline(self, domain, api_external, timeline_name = 'local'):
        self._log.debug(f"Checking timeline of domain '{domain}' with name '{timeline_name}'...")
        last_ids = list_read(self.bot_name + "_" + domain + "_last_ids")
        self.warned.extend(list_read(self.bot_name + "_" + domain))
        timeline = api_external.timeline(timeline=timeline_name, limit=self.max_posts)
        new_last_ids=[]
        self._log.debug(f"Gotten {len(timeline)} posts in the timeline")
        for post in timeline:
            new_last_ids.append(post['id'])
        for i in range(0, len(timeline) - 2):
            post = timeline[i]
            if str(post['id']) not in last_ids and (
                str(post['account']['acct']) not in self.warned or (
                    timeline_name == 'home' and post['account']['acct'] in self.following
                    )
                ):
                for media in post['media_attachments']:
                    if media['description'] is None:
                        self._log.warning('Warning ' + post['account']['acct'])
                        status_reply(self.api_internal, post, self.messages['mensaje'], visibility="unlisted")
                        self.warned.append(post['account']['acct'])
                        if domain != 'home':
                            list_append(self.bot_name + "_" + domain, post['account']['acct'])
                        break
                    else:
                        self._log.debug(f"Post {post['id']} has media with description")
            else:
                self._log.debug(f"Ignoring post {post['id']}")
        list_write(self.bot_name + "_" + domain + "_last_ids", new_last_ids)

    def _init_log(self):
        ''' Initialize log object '''
        self._log = logging.getLogger("describot")
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
            log_file = os.path.join(log_folder, "describot.log")

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
    return describot(**kwargs)

if __name__ == "__main__":
    __main__()

