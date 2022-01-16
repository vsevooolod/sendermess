import os
from typing import Union

from .whatsapp import SenderWA
from .telegram import SenderTG
from .types_ import MessangerType


def sender(messanger: MessangerType) -> Union[SenderWA, SenderTG]:
    if messanger.value == MessangerType.WA.value:
        api_token, api_url = os.getenv('WA_API_TOKEN'), os.getenv('WA_API_URL')
        if not api_token or not api_url:
            print('You need to set environment variables: WA_API_URL, WA_API_TOKEN\n'
                  'You need to get them here: https://app.chat-api.com/')
            exit(0)
        return SenderWA(api_url=api_url, api_token=api_token)
    elif messanger.value == MessangerType.TG.value:
        api_id, api_hash = int(os.getenv('TG_API_ID', 0)), os.getenv('TG_API_HASH')
        if not api_id or not api_hash:
            print('You need to set environment variables: TG_API_ID, TG_API_HASH\n'
                  'You need to get them here: https://my.telegram.org/')
            exit(0)
        return SenderTG(api_id=api_id, api_hash=api_hash)
