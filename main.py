import os

from dotenv import load_dotenv

from senders.whatsapp import SenderWA


load_dotenv()


WA_API_TOKEN = os.getenv('WA_API_TOKEN')
WA_API_URL = os.getenv('WA_API_URL')

if not WA_API_TOKEN or not WA_API_URL:
    print('You need to set environment variables: WA_API_URL, WA_API_TOKEN\n'
          'You need to get them here: https://app.chat-api.com/')
    exit(0)


def main():
    sender = SenderWA(api_url=WA_API_URL, api_token=WA_API_TOKEN)
    result = sender.get_users_entities_from_chats(
        ['79231502227-1583296173@g.us', '79231502227-1583296173@g.us'],
        unique=False
    )


if __name__ == '__main__':
    main()
