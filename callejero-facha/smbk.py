# Simple Mastodon Bot Kit
# by @ElPamplina@masto.es
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program. If not,
# see <https://www.gnu.org/licenses/>.

import os
import random
import sys
from datetime import datetime
from mastodon import Mastodon
import params

print(f"Starting {params.APP_NAME}: {datetime.now()}")

if (len(sys.argv) == 1 or sys.argv[1] != '--force') and random.random() > params.FREQ:
    print("Random exit.")
    sys.exit()

if os.path.isfile(params.APP_FILE) and os.path.isfile(params.USER_FILE):
    mastodon = Mastodon(client_secret=params.APP_FILE, access_token=params.USER_FILE)
else:
    Mastodon.create_app(params.APP_NAME, api_base_url=params.SERVER, to_file=params.APP_FILE)
    mastodon = Mastodon(client_id=params.APP_FILE)
    print('Go to auth page and copy auth code:')
    print(mastodon.auth_request_url())
    pwd = input("Input auth code: ")
    mastodon.log_in(code=pwd, to_file=params.USER_FILE)

content = params.CALLABLE()
last_post = None
for c in content:
    text = c['text']
    media_ids = []
    count = 0
    for f in c.get('media', []):
        count += 1
        if count > params.MAX_IMAGES:
            print('Media exceeds number of items. Skipping.')
        else:
            img = f['img']
            mime = f['mime']
            alt = f.get('alt')
            if 'image' not in mime and count > 1:
                print('Only one non-image media. Skipping.')
            else:
                if len(img) <= params.IMG_MAX:
                    print(f'Sending media: {len(img)} bytes.')
                    media = mastodon.media_post(img, mime_type=mime, description=alt)
                    media_ids.append(media)
                else:
                    print('Media exceeds max file size. Skipping.')

    if not c.get('reply', True):
        last_post = None
    post = mastodon.status_post(
        text,
        language=params.LANGUAGE,
        visibility='unlisted',
        media_ids=media_ids,
        in_reply_to_id=last_post
    )
    print(f"Sent post: {post.url}")
    last_post = post.id

print(f"Ending {params.APP_NAME}: {datetime.now()}")
