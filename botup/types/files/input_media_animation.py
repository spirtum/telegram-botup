from .input_file import InputFile
from .input_media import InputMedia


class InputMediaAnimation(InputMedia):
    NESTED_KEYS = ['thumb', ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'animation'
        self.thumb = InputFile(**kwargs['thumb']) if 'thumb' in kwargs else None
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.duration = kwargs.get('duration')
