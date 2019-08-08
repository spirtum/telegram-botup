from ..base_object import BaseObject


class InputMedia(BaseObject):

    def __init__(self, **kwargs):
        self.type = kwargs.get('type')
        self.media = kwargs.get('media')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
