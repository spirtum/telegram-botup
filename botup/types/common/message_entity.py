from .user import User


class MessageEntity:

    def __init__(self, **kwargs):
        self.type = kwargs.get('type')
        self.offset = kwargs.get('offset')
        self.length = kwargs.get('length')
        self.url = kwargs.get('url')
        self.user = User(**kwargs['user']) if 'user' in kwargs else None
