from .base import StringConstant


class InlineQueryResultType(StringConstant):
    pass


ARTICLE = InlineQueryResultType('article')
PHOTO = InlineQueryResultType('photo')
GIF = InlineQueryResultType('gif')
MPEG4_GIF = InlineQueryResultType('mpeg4_gif')
VIDEO = InlineQueryResultType('video')
AUDIO = InlineQueryResultType('audio')
VOICE = InlineQueryResultType('voice')
DOCUMENT = InlineQueryResultType('document')
LOCATION = InlineQueryResultType('location')
VENUE = InlineQueryResultType('venue')
CONTACT = InlineQueryResultType('contact')
GAME = InlineQueryResultType('game')
STICKER = InlineQueryResultType('sticker')
