import threading

try:
    import ujson as json
except ImportError:
    import json

from .mixins import DBMixin
from .types import (
    User,
    Chat,
    Poll,
    File,
    Update,
    Message,
    ChatMember,
    StickerSet,
    WebhookInfo,
    ErrorResponse,
    GameHighScore,
    UserProfilePhotos
)


def parse_response(response):
    if not isinstance(response, dict):
        response = json.loads(response)
    status = response.get('ok')
    result = response.get('result')
    if not status:
        return ErrorResponse(**response)
    elif isinstance(result, bool) or isinstance(result, str):
        return result
    elif isinstance(result, list):
        parsed_result = []
        for item in result:
            if 'update_id' in item:
                parsed_result.append(Update(**item))
            if 'user' in item and 'status' in item:
                parsed_result.append(ChatMember(**item))
            elif 'user' in item and 'score' in item:
                parsed_result.append(GameHighScore(**item))
        return parsed_result
    elif 'update_id' in result:
        return Update(**result)
    elif 'message_id' in result:
        return Message(**result)
    elif 'is_bot' in result:
        return User(**result)
    elif 'total_count' in result and 'photos' in result:
        return UserProfilePhotos(**result)
    elif 'file_id' in result and 'file_size' in result and 'file_path' in result:
        return File(**result)
    elif 'type' in result and result['type'] in ('private', 'group', 'supergroup', 'channel'):
        return Chat(**result)
    elif 'user' in result and 'status' in result:
        return ChatMember(**result)
    elif 'question' in result and 'options' in result:
        return Poll(**result)
    elif 'contains_masks' in result and 'stickers' in result:
        return StickerSet(**result)
    elif 'has_custom_certificate' in result:
        return WebhookInfo(**result)
    else:
        return result


def error_response(text):
    return json.dumps({'ok': False, 'error_code': 502, 'description': text})


class ResultGetter(DBMixin):
    __slots__ = ['rdb', 'correlation_id', '_value']

    def __init__(self, connection, correlation_id):
        assert connection, 'No connect to redis'
        super().__init__(connection)
        self.correlation_id = correlation_id
        self._value = None

    def _get_value(self):
        self._value = self._get_result(self.correlation_id)

    def wait(self, timeout=5, parse=True, tick=0.05):
        attempts = timeout // tick
        self._get_value()
        while not self._value and attempts != 0:
            attempts -= 1
            timer = threading.Timer(tick, self._get_value)
            timer.start()
            timer.join()
        if not self._value:
            self._value = {'ok': False, 'error_code': 502, 'description': 'No result'}
        return parse_response(self._value) if parse else self._value
