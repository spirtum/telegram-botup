import redis

from .dispatcher import Dispatcher


class State:
    __slots__ = ['key', 'dispatcher']

    def __init__(self, key, dispatcher):
        assert isinstance(key, str), 'Key is not a str'
        assert isinstance(dispatcher, Dispatcher)
        self.key = key
        self.dispatcher = dispatcher

    def __repr__(self):
        return f'<botup.fsm.State> {self.key}'


class StateMachine:

    def __init__(self, connection, db_key='botup:{}:state'):
        assert isinstance(connection, redis.client.Redis), 'connection is not a redis.client.Redis type'
        assert isinstance(db_key, str), 'db_key is not a str type'
        if '{}' not in db_key:
            db_key += ':{}'
        self._rdb = connection
        self._db_key = db_key
        self.initial = State('initial', Dispatcher())
        self.state = self.initial
        self._keys = [self.initial.key, ]
        self._INVALID_KEYS = ['_rdb', '_keys', 'state', 'set', 'fetch', 'handle', 'register_dispatcher']

    def __getattr__(self, item):
        raise Exception(f'State {item} not found')

    def register_dispatcher(self, state_key, dispatcher):
        assert state_key not in self._INVALID_KEYS, 'Invalid key'
        assert state_key not in self._keys, 'Key already exists'
        setattr(self, state_key, State(state_key, dispatcher))
        self._keys.append(state_key)
        return True

    def set(self, chat_id, state, expire=None):
        assert isinstance(chat_id, (int, str)), 'chat_id is not a int or str type'
        assert isinstance(state, State), 'state is not a State type'
        if expire:
            assert isinstance(expire, int), 'expire is not a int type'
        self._rdb.set(self._db_key.format(chat_id), state.key, ex=expire)
        self.state = state
        return True

    def fetch(self, chat_id):
        assert isinstance(chat_id, (int, str)), 'chat_id is not a int or str type'
        value = self._rdb.get(self._db_key.format(chat_id))
        if value and value in self._keys:
            self.state = getattr(self, value)
            return True
        else:
            self.state = self.initial
            return False

    def handle(self, chat_id, update):
        assert isinstance(chat_id, (int, str)), 'chat_id is not a int or str type'
        self.fetch(chat_id)
        self.state.dispatcher.handle(update)

