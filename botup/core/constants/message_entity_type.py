from .base import StringConstant


class MessageEntityType(StringConstant):
    pass


MENTION = MessageEntityType('mention')
HASHTAG = MessageEntityType('hashtag')
CASHTAG = MessageEntityType('cashtag')
BOT_COMMAND = MessageEntityType('bot_command')
URL = MessageEntityType('url')
EMAIL = MessageEntityType('email')
PHONE_NUMBER = MessageEntityType('phone_number')
BOLD = MessageEntityType('bold')
ITALIC = MessageEntityType('italic')
UNDERLINE = MessageEntityType('underline')
STRIKETHROUGH = MessageEntityType('strikethrough')
SPOILER = MessageEntityType('spoiler')
CODE = MessageEntityType('code')
PRE = MessageEntityType('pre')
TEXT_LINK = MessageEntityType('text_link')
TEXT_MENTION = MessageEntityType('text_mention')
CUSTOM_EMOJI = MessageEntityType('custom_emoji')
