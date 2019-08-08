from ..base_object import BaseObject


class InputFile(BaseObject):

    def __init__(self, **kwargs):
        self.file_id = kwargs.get('file_id')
        self.url = kwargs.get('url')
        self.path = kwargs.get('path')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
