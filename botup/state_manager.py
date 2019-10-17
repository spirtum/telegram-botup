class StateManager:

    def __init__(self, connection, name='botup:{}:state'):
        self.connection = connection
        self.name = name
        self.update = None

    def set(self, key, value):
        message = self.update.message or getattr(self.update.callback_query, 'message', None)
        if not message:
            raise('Cannot set state with', self.update)
        return self.connection.hset(self.name.format(message.chat.id), key, value)

    def get_all(self):
        message = self.update.message or getattr(self.update.callback_query, 'message', None)
        if not message:
            raise ('Cannot get state with', self.update)
        return self.connection.hgetall(self.name.format(message.chat.id))

    def get(self, key):
        message = self.update.message or getattr(self.update.callback_query, 'message', None)
        if not message:
            raise ('Cannot get state with', self.update)
        return self.connection.hgetall(self.name.format(message.chat.id), key)

    def reset(self, *keys):
        message = self.update.message or getattr(self.update.callback_query, 'message', None)
        if not message:
            raise ('Cannot delete state with', self.update)
        return self.connection.hdel(self.name.format(message.chat.id), *keys)

    @property
    def is_valid_update(self):
        return self.update.message or getattr(self.update.callback_query, 'message', None) is not None
