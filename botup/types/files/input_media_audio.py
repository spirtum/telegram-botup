from .input_file import InputFile
from .input_media import InputMedia


class InputMediaAudio(InputMedia):
    NESTED_KEYS = ['thumb', ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'audio'
        self.thumb = InputFile(**kwargs['thumb']) if 'thumb' in kwargs else None
        self.duration = kwargs.get('duration')
        self.performer = kwargs.get('performer')
        self.title = kwargs.get('title')
