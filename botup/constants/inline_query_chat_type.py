from .base import StringConstant


class InlineQueryChatType(StringConstant):
    pass


SENDER = InlineQueryChatType('sender')
PRIVATE = InlineQueryChatType('private')
GROUP = InlineQueryChatType('group')
SUPERGROUP = InlineQueryChatType('supergroup')
CHANNEL = InlineQueryChatType('channel')
