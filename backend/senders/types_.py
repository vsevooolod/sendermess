from enum import Enum


class MethodType(str, Enum):
    GET = 'GET'
    POST = 'POST'


class MessangerType(str, Enum):
    WA = 'WHATSAPP'
    TG = 'TELEGRAM'


class DataType(str, Enum):
    GROUP = 'GROUP'
    PARTICIPANT = 'PARTICIPANT'
    WORK = 'WORK'
