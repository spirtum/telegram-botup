from .input_media import InputMedia


class InputMediaPhoto(InputMedia):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'photo'
