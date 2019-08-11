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


def is_error(instance):
    return isinstance(instance, ErrorResponse)


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


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class State:
    __slots__ = ['value', 'setup', 'teardown']

    def __init__(self, value):
        self.value = value
        self.setup = None
        self.teardown = None

    def __repr__(self):
        return self.value


class FSM(metaclass=Singleton):

    KEY = 'botup:user:{}:state'
    STATES = []

    def __init__(self, connection, initial='initial'):
        self._rdb = connection
        assert isinstance(initial, str), '"initial" must be a type str'
        for value in self.__class__.STATES:
            assert isinstance(value, str), '"state" must be a type "str"'
            setattr(self, value, State(value))
        self.initial = State(initial)
        self.state = self.initial

    def __getattr__(self, item):
        setattr(self, item, State(item))
        return getattr(self, item)

    def set(self, chat_id, state, expire=None):
        assert isinstance(state, State), '"state" is not a type "State"'
        self.state.teardown() if self.state.teardown else None
        self._rdb.set(self.KEY.format(chat_id), state.value, ex=expire)
        self.state = state
        self.state.setup() if self.state.setup else None

    def fetch(self, chat_id):
        value = self._rdb.get(self.KEY.format(chat_id))
        if value:
            self.state = getattr(self, value)
            return self.state
        else:
            return self.initial
