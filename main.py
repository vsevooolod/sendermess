import os

from dotenv import load_dotenv

from senders.whatsapp import SenderWA
from senders.telegram import SenderTG


load_dotenv()


WA_API_TOKEN = os.getenv('WA_API_TOKEN')
WA_API_URL = os.getenv('WA_API_URL')

TG_API_ID = int(os.getenv('TG_API_ID', 0))
TG_API_HASH = os.getenv('TG_API_HASH')

# if not WA_API_TOKEN or not WA_API_URL:
#     print('You need to set environment variables: WA_API_URL, WA_API_TOKEN\n'
#           'You need to get them here: https://app.chat-api.com/')
#     exit(0)


def main():
    sender = SenderTG(api_id=TG_API_ID, api_hash=TG_API_HASH)
    groups = sender.get_groups(key_words=['краснодар'])
    participants = sender.get_groups_participants(groups=groups)


if __name__ == '__main__':
    main()
