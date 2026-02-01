import memoriabot

FREQ = 3/72  # 3 posts in 72 tries per day (cron: 20 minutes)
APP_NAME = 'memoriabot'  # App name to register in server
APP_FILE = '/home/mastodon/mastoes-bots/callejero-facha/memoriabot-app.secret'  # Application secret file
USER_FILE = '/home/mastodon/mastoes-bots/callejero-facha/memoriabot-user.secret'  # User secret file
SERVER = 'https://masto.es'  # Mastodon server
MSG_MAX = 2000  # Message max size
IMG_MAX = 10000000  # Image max size
MAX_IMAGES = 4
LANGUAGE = 'es'
CALLABLE = memoriabot.generate_posts  # Python function to call to generate post contents
