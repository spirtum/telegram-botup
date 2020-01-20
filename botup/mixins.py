import time

try:
    import ujson as json
except ImportError:
    import json


class DBMixin:
    FORM_MESSAGE_ID = 'botup:user:{}:form_message_id'
    LAST_TIME = 'botup:user:{}:last_time'
    RESULT = 'botup:result:{}'

    def __init__(self, connection):
        self.connection = connection
        if not self.connection:
            self._patch_methods()

    def _patch_methods(self):
        def dummy(*args, **kwargs):
            pass

        self._get_form_message_id = dummy
        self._set_form_message_id = dummy
        self._delete_form_message_id = dummy
        self._set_last_time = dummy
        self._get_last_time = dummy
        self._save_result = dummy
        self._get_result = dummy

    def get_form_message_id(self, chat_id):
        return self.connection.get(self.FORM_MESSAGE_ID.format(chat_id))

    def _set_form_message_id(self, chat_id, value):
        self.connection.set(self.FORM_MESSAGE_ID.format(chat_id), value)

    def _delete_form_message_id(self, chat_id):
        return self.connection.delete(self.FORM_MESSAGE_ID.format(chat_id))

    def _set_last_time(self, chat_id):
        self.connection.set(self.LAST_TIME.format(chat_id), str(time.time()), 10)

    def _get_last_time(self, chat_id):
        return self.connection.get(self.LAST_TIME.format(chat_id))

    def _save_result(self, correlation_id, value):
        self.connection.set(self.RESULT.format(correlation_id), value, 10)

    def _get_result(self, correlation_id):
        value = self.connection.get(self.RESULT.format(correlation_id))
        if not value:
            return
        self.connection.delete(self.RESULT.format(correlation_id))
        return json.loads(value)


class HandlerPatternMixin:

    def __init__(self, update, user_handlers):
        self.update = update
        self.handlers = user_handlers

    def get_handler(self, command):
        handler = self.handlers.get(command)
        if not handler:
            for pattern in (c for c in self.handlers.keys() if hasattr(c, 'match')):
                if pattern.match(command):
                    handler = self.handlers[pattern]
                    break
        return handler


class HandlerSimpleMixin:

    def __init__(self, update, user_handler):
        self.update = update
        self.user_handler = user_handler

    def handle(self):
        if not self.user_handler:
            return
        self.user_handler(self.update.message.chat.id, self.update)
