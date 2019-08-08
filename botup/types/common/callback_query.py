from .message import Message
from .user import User


class CallbackQuery:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.from_ = User(**kwargs.get('from'))
        self.message = Message(**kwargs['message']) if 'message' in kwargs else None
        self.inline_message_id = kwargs.get('inline_message_id')
        self.chat_instance = kwargs.get('chat_instance')
        self.data = kwargs.get('data')
        self.game_short_name = kwargs.get('game_short_name')
