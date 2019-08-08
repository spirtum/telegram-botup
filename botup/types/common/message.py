from .chat import Chat
from .pinned_message import PinnedMessage


class Message(PinnedMessage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chat = Chat(**kwargs.get('chat'))
        self.forward_from_chat = Chat(**kwargs['forward_from_chat']) if 'forward_from_chat' in kwargs else None
