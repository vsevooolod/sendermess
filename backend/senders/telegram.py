import time
from typing import Dict, List, Optional

from telethon.sync import TelegramClient

from .types_ import MessangerType, DataType
from .utils import get_datetime


def sessionmaker(func):
    def wrapper(*args, **kwargs):
        with TelegramClient('./backend/anon', args[0].api_id, args[0].api_hash) as session:
            return func(session=session, *args, **kwargs)
    return wrapper


class SenderTG:
    def __init__(self, api_id: int, api_hash: str):
        self.api_id, self.api_hash = api_id, api_hash

    @sessionmaker
    def get_groups(self, session, key_words: Optional[List[str]] = None) -> List[Optional[Dict]]:
        groups = []
        for dialog in session.get_dialogs():
            if (not any([dialog.is_channel, dialog.is_group]) or
                    (key_words and not list(filter(lambda w: w.lower() in dialog.entity.title.lower(), key_words)))):
                continue
            groups.append({
                'type': DataType.GROUP.value,
                'entity': str(dialog.entity.id),
                'title': dialog.entity.title,
                'participants_count': dialog.entity.participants_count,
                'messanger': MessangerType.TG.value,
            })
        return groups

    @sessionmaker
    def get_groups_participants(self, session, groups: List[Dict], unique: bool = True) -> List[Dict]:
        participants, viewed_entities = [], []
        for group in groups:
            for participant in session.get_participants(int(group['entity'])):
                if unique and participant.id in viewed_entities:
                    continue
                viewed_entities.append(participant.id)
                participants.append({
                    'type': DataType.PARTICIPANT.value,
                    'phone': participant.phone or '',
                    'entity': str(participant.id),
                    'name': f'{participant.first_name or ""} {participant.last_name or ""}'.strip(),
                    'messanger': MessangerType.TG.value,
                })
        return participants

    @sessionmaker
    def send_messages(self, session, participants: List[Dict], message: str, timeout_sec: int = 300) -> Dict:
        work = {'type': DataType.WORK.value, 'start': get_datetime(beauty=False), 'errors': 0,
                'timeout_sec': timeout_sec, 'subworks': [], 'messanger': MessangerType.TG.value}
        for subwork in participants:
            try:
                session.send_message(int(subwork['entity']), message)
                done, err_message = True, ''
            except Exception as ex:
                done, err_message = False, ex
                work['errors'] += 1
            subwork.update({'done': done, 'datetime': get_datetime(beauty=False), 'err_message': err_message})
            work['subworks'].append(subwork)
            time.sleep(timeout_sec)
        work['end'] = get_datetime(beauty=False)
        return work
