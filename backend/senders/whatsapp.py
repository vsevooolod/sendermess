import time
from json import JSONDecodeError
from typing import Dict, List, Optional

from requests import Response

from .types_ import MethodType, MessangerType, DataType
from .utils import send_request, get_datetime


class SenderWA:
    def __init__(self, api_url: str, api_token: str):
        self.api_url, self.api_token = api_url, api_token

    @staticmethod
    def _get_jo(response: Optional[Response] = None) -> Optional[Dict]:
        """ Getting JSON from API response """
        try:
            if response.status_code != 200:
                raise TypeError
            jo = response.json()
        except (JSONDecodeError, TypeError):
            jo = dict()
        return jo

    def get_groups(self, key_words: Optional[List[str]] = None) -> List[Optional[Dict]]:
        groups = []
        jo = self._get_jo(send_request(url=f'{self.api_url}dialogs', query={'token': self.api_token}))
        for dialog in jo.get('dialogs', []):
            if (not dialog['metadata']['isGroup'] or
                    (key_words and not list(filter(lambda w: w.lower() in dialog['name'].lower(), key_words)))):
                continue
            groups.append({
                'type': DataType.GROUP.value,
                'entity': str(dialog['id']),
                'title': dialog['name'],
                'participants_count': len(dialog['metadata']['participants']),
                'participants_entities': dialog['metadata']['participants'],
                'messanger': MessangerType.WA.value,
            })
        return groups

    def get_groups_participants(self, groups: List[Dict], unique: bool = True) -> List[Dict]:
        participants, viewed_entities = [], []
        for group in groups:
            for participant_entity in group['participants_entities']:
                if unique and participant_entity in viewed_entities:
                    continue
                viewed_entities.append(participant_entity)
                participants.append({
                    'type': DataType.PARTICIPANT.value,
                    'phone': participant_entity.split('@')[0],
                    'entity': participant_entity,
                    'name': '',
                    'messanger': MessangerType.WA.value,
                })
        return participants

    def send_messages(self, participants: List[Dict], message: str, timeout_sec: int = 300) -> Dict:
        work = {'type': DataType.WORK.value, 'start': get_datetime(beauty=False), 'errors': 0,
                'timeout_sec': timeout_sec, 'subworks': [], 'messanger': MessangerType.WA.value}
        for subwork in participants:
            try:
                jo = self._get_jo(send_request(url=f'{self.api_url}sendMessage', method=MethodType.POST,
                                              query={'token': self.api_token, 'chatId': subwork['entity'],
                                                     'body': message}))
                if not jo or not jo['sent']:
                    raise Exception(jo.get('message') or 'Bad response from whatsapp api...')
                done, err_message = True, ''
            except Exception as ex:
                done, err_message = False, ex
                work['errors'] += 1
            subwork.update({'done': done, 'datetime': get_datetime(beauty=False), 'err_message': err_message})
            work['subworks'].append(subwork)
            time.sleep(timeout_sec)
        work['end'] = get_datetime(beauty=False)
        return work
