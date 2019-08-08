from .input_file import InputFile
from .input_media import InputMedia


class InputMediaDocument(InputMedia):
    NESTED_KEYS = ['thumb', ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'document'
        self.thumb = InputFile(**kwargs['thumb']) if 'thumb' in kwargs else None
