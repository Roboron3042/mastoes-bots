from common import get_api
from common import list_append
from common import list_read
from common import list_write
from common import get_new_notifications
import json
import os
import click
import click_config_file


class load_custom_messages():
    def __init__(self, custom_message_file):
        if os.path.exists(custom_message_file):
            with open(custom_message_file, 'r') as messages_pointer:
                custom_messages = json.load(messages_pointer)
                return custom_messages

class describot():
    def __init__(self, **kwargs):
        # Initialization
        self.kwargs = kwargs
        self.custom_messages = load_custom_messages(self.kwargs['custom_message_file']).custom_messages
        messages = self.custom_messages[self.kwargs['language']]['describot']
        bot_name = messages['describot']['bot_name']
        

        api_internal = get_api(self.kwargs['instance_name'], bot_name)
        max_posts=20
        warned=[]

        following = list_read(bot_name + "_following")

        def check_timeline(domain, api_external, timeline_name = 'local'):
            last_ids = list_read(bot_name + "_" + domain + "_last_ids")
            warned.extend(list_read(bot_name + "_" + domain))
            timeline = api_external.timeline(timeline=timeline_name, limit=max_posts)
            new_last_ids=[]
            for post in timeline:
                new_last_ids.append(post['id'])
            for i in range(0, len(timeline) - 2):
                post = timeline[i]
                if str(post['id']) not in last_ids and (str(post['account']['acct']) not in warned or (timeline_name == 'home' and post['account']['acct'] in following)): 
                    for media in post['media_attachments']:
                        if media['description'] is None:
                            print('Warning ' + post['account']['acct'])
                            api_internal.status_reply(post, messages['describot']['mensaje'], visibility="unlisted")
                            warned.append(post['account']['acct'])
                            if domain != 'home':
                                list_append(bot_name + "_" + domain, post['account']['acct'])
                            break
            list_write(bot_name + "_" + domain + "_last_ids", new_last_ids)

        notifications = get_new_notifications(api_internal, bot_name, types=['follow'])
        for n in notifications:
            if n['account']['acct'] not in following:
                print("Following: " + n['account']['acct'])
                api_internal.account_follow(n['account']['id'])
                following.append(n['account']['acct'])
                list_append(bot_name + "_following", n['account']['acct'])


        check_timeline(self.kwargs['instance_name'], api_internal)
        check_timeline('home', api_internal, timeline_name='home')

@click.command()
@click.option('--language', '-l', default='es', help="Language.")
@click.option('--custom-message-file', '-j', default='custom_messages.json', help='JSON file containing the messages.')
@click.option('--instance-name', '-i', default='masto.es', help='Instance FQDN')
@click_config_file.configuration_option()
def __main__(**kwargs):
    return describot(**kwargs)

if __name__ == "__main__":
    __main__()

