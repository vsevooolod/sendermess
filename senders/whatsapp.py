from time import time, sleep
from json import JSONDecodeError
from typing import Dict, List, Optional

from requests import Response
from .utils import send_request, get_datetime, Method


class SenderWA:
    def __init__(self, api_url: str, api_token: str):
        self.api_url, self.api_token = api_url, api_token

    @staticmethod
    def get_jo(entity: str, response: Optional[Response] = None,
               message: str = '') -> Optional[Dict]:
        """Parsing response from api and generate response-dictionary"""
        jo = {'done': False, 'message': message, 'entity': entity,
              'when': get_datetime(), 'response_from_api': None}
        try:
            response_from_api = response.json()
            if response.status_code == 200:
                jo['done'] = True
                response_from_api.pop('sent', None)
            jo['response_from_api'] = response_from_api
        except (JSONDecodeError, AttributeError):
            jo['message'] = '[ERROR] BAD RESPONSE FROM API'
        return jo

    def send_message(self, entity: str, message: str) -> Dict:
        """Sending message to user by entity"""
        if '@' not in entity:
            entity += '@c.us'
        res = send_request(url=f'{self.api_url}sendMessage', method=Method.POST,
                           query={'token': self.api_token, 'body': message, 'chatId': entity})
        return self.get_jo(entity, res)

    def send_messages(self, entities: List[str], message: str, **kwargs) -> Dict:
        """Sending message to users by entities"""
        timeout = kwargs.get('timeout', 2)
        result = {'works': [], 'start': get_datetime(), 'errors': 0, 'timeout': timeout}
        for entity in entities:
            work = self.send_message(entity, message)
            if not work['done']:
                result['errors'] += 1
            result['works'].append(work)
            sleep(timeout)
        result['end'] = get_datetime()
        return result

    def get_chat(self, entity: str) -> Dict:
        """Getting available chat information"""
        if '@' not in entity:
            return self.get_jo(entity, message='[ERROR] INCORRECT CHAT ID')
        res = send_request(url=f'{self.api_url}dialog', query={'token': self.api_token, 'chatId': entity})
        return self.get_jo(entity, res)

    def get_users_entities_from_chats(self, chats_entities: List[str], unique: bool = True) -> Dict:
        """Getting list entities of chats participants"""
        result = {'works': [], 'start': get_datetime(), 'errors': 0, 'users_entities': [], 'unique': unique}

        for chat_entity in chats_entities:
            work = self.get_chat(chat_entity)
            if work['done']:
                for user_entity in work['response_from_api']['metadata']['participants']:
                    if user_entity not in result['users_entities'] or not unique:
                        result['users_entities'].append(user_entity)
            else:
                result['errors'] += 1
            result['works'].append(work)

        result['count_accepted_users_entities'] = len(result['users_entities'])
        result['end'] = get_datetime()
        return result
