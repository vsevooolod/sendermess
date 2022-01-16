from typing import Optional, Dict, Union
from datetime import datetime

import pytz
import requests
from requests import Response

from .types_ import MethodType


def send_request(url: str, method: MethodType = MethodType.GET,
                 query: Optional[Dict] = None, data: Optional[Dict] = None) -> Response:
    if method.value == MethodType.POST.value:
        r = requests.post(url, params=query, data=data)
    else:
        r = requests.get(url, params=query)
    return r


def get_datetime(beauty: bool = True) -> Union[str, datetime]:
    tz = pytz.timezone('Europe/Moscow')
    dt = tz.localize(datetime.now())
    return dt.strftime('%H:%M:%S %d/%m/%Y') if beauty else dt


def get_timestamp() -> int:
    return int(get_datetime(beauty=False).timestamp())
