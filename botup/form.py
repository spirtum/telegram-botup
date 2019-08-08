import uuid

try:
    import ujson as json
except ImportError:
    import json

from .mixins import DBMixin
from .sender import Sender
from .utils import ResultGetter


class Form(DBMixin):

    def __init__(
            self,
            token,
            connection=None,
            bot_name=None,
            queue='botup-sender-queue',
            simple_mode=False,
            fake_mode=False,
            proxy_url=None,
            basic_auth_string=None,
            socks_proxy_string=None
    ):
        super().__init__(connection)
        self.queue = queue
        self.simple_mode = simple_mode
        self.fake_mode = fake_mode
        self.bot_name = bot_name
        self._sender = Sender(
            token=token,
            connection=connection,
            queue=queue,
            proxy_url=proxy_url,
            basic_auth_string=basic_auth_string,
            socks_proxy_string=socks_proxy_string)
        if not connection:
            self.simple_mode = True

    def __getattr__(self, item):
        return getattr(self._sender, item)

    @property
    def start_group_link(self):
        assert self.bot_name, 'Form.bot_name not set'
        return f'https://telegram.me/{self.bot_name}?startgroup='

    def push(self, func, save_id=False, **kwargs):
        correlation_id = str(uuid.uuid4())
        payload = dict(
            func=func.__name__,
            kwargs=kwargs,
            correlation_id=correlation_id,
            save_id=save_id
        )
        if self.fake_mode:
            print(f'Run {func.__name__} with {kwargs}')
            return
        if self.simple_mode:
            print(f'Run {func.__name__} with {kwargs}')
            self._sender.start_task(**payload)
        else:
            self.rdb.publish(self.queue, json.dumps(payload))
        return ResultGetter(self.rdb, correlation_id)

    def clear(self, chat_id):
        message_id = self.get_form_message_id(chat_id)
        if message_id:
            self.push(self.delete_message, chat_id=chat_id, message_id=message_id)
            self._delete_form_message_id(chat_id)
            return True

    def quick_callback_answer(self, update):
        assert update.callback_query, 'Update do not have a CallbackQuery'
        self.push(
            func=self.answer_callback_query,
            callback_query_id=update.callback_query.id
        )
