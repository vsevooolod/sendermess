import time
from typing import Dict, List, Optional

from telethon.sync import TelegramClient

from senders.utils import get_datetime


def sessionmaker(func):
    def wrapper(*args, **kwargs):
        with TelegramClient('anon', args[0].api_id, args[0].api_hash) as session:
            kwargs['session'] = session
            kwargs['titles'] = kwargs.pop('titles', None)
            return func(*args, **kwargs)
    return wrapper


class SenderTG:
    def __init__(self, api_id: int, api_hash: str):
        self.api_id, self.api_hash = api_id, api_hash

    @sessionmaker
    def get_groups(self, session, titles: Optional[List[str]] = None) -> List[Optional[Dict]]:
        groups = []
        for dialog in session.get_dialogs():
            if (not any([dialog.is_channel, dialog.is_group]) or
                    (titles and not list(filter(lambda t: t.lower() in dialog.entity.title.lower(), titles)))):
                continue
            groups.append({'entity': dialog.entity.id, 'title': dialog.entity.title,
                          'participants_count': dialog.entity.participants_count})
        return groups
