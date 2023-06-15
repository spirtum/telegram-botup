from .base import StringConstant


class ChatType(StringConstant):
    pass


PRIVATE = ChatType('private')
GROUP = ChatType('group')
SUPERGROUP = ChatType('supergroup')
CHANNEL = ChatType('channel')
