from .chat_photo import ChatPhoto
from .pinned_message import PinnedMessage


class Chat:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.type = kwargs.get('type')
        self.title = kwargs.get('title')
        self.username = kwargs.get('username')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.all_members_are_administrators = kwargs.get('all_members_are_administrators')
        self.photo = ChatPhoto(**kwargs['photo']) if 'photo' in kwargs else None
        self.description = kwargs.get('description')
        self.invite_link = kwargs.get('invite_link')
        self.pinned_message = PinnedMessage(**kwargs.get('pinned_message')) if 'pinned_message' in kwargs else None
        self.sticker_set_name = kwargs.get('sticker_set_name')
        self.can_set_sticker_set = kwargs.get('can_set_sticker_set')
