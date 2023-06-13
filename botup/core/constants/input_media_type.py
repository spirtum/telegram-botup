from .base import StringConstant


class InputMediaType(StringConstant):
    pass


PHOTO = InputMediaType('photo')
VIDEO = InputMediaType('video')
ANIMATION = InputMediaType('animation')
AUDIO = InputMediaType('audio')
DOCUMENT = InputMediaType('document')
