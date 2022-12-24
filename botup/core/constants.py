class StringConstant(str):
    def __new__(cls, *args, **kw):
        return str.__new__(cls, *args, **kw)


class ChatType(StringConstant):
    pass


class MessageEntityType(StringConstant):
    pass


class PollType(StringConstant):
    pass


class ChatMemberStatus(StringConstant):
    pass


class BotCommandScopeType(StringConstant):
    pass


class MenuButtonType(StringConstant):
    pass


class InputMediaType(StringConstant):
    pass


class InputFileType(StringConstant):
    pass


class StickerType(StringConstant):
    pass


class MaskPositionPoint(StringConstant):
    pass


CHAT_TYPE_PRIVATE = ChatType('private')
CHAT_TYPE_GROUP = ChatType('group')
CHAT_TYPE_SUPERGROUP = ChatType('supergroup')
CHAT_TYPE_CHANNEL = ChatType('channel')

MESSAGE_ENTITY_TYPE_MENTION = MessageEntityType('mention')
MESSAGE_ENTITY_TYPE_HASHTAG = MessageEntityType('hashtag')
MESSAGE_ENTITY_TYPE_CASHTAG = MessageEntityType('cashtag')
MESSAGE_ENTITY_TYPE_BOT_COMMAND = MessageEntityType('bot_command')
MESSAGE_ENTITY_TYPE_URL = MessageEntityType('url')
MESSAGE_ENTITY_TYPE_EMAIL = MessageEntityType('email')
MESSAGE_ENTITY_TYPE_PHONE_NUMBER = MessageEntityType('phone_number')
MESSAGE_ENTITY_TYPE_BOLD = MessageEntityType('bold')
MESSAGE_ENTITY_TYPE_ITALIC = MessageEntityType('italic')
MESSAGE_ENTITY_TYPE_UNDERLINE = MessageEntityType('underline')
MESSAGE_ENTITY_TYPE_STRIKETHROUGH = MessageEntityType('strikethrough')
MESSAGE_ENTITY_TYPE_SPOILER = MessageEntityType('spoiler')
MESSAGE_ENTITY_TYPE_CODE = MessageEntityType('code')
MESSAGE_ENTITY_TYPE_PRE = MessageEntityType('pre')
MESSAGE_ENTITY_TYPE_TEXT_LINK = MessageEntityType('text_link')
MESSAGE_ENTITY_TYPE_TEXT_MENTION = MessageEntityType('text_mention')
MESSAGE_ENTITY_TYPE_CUSTOM_EMOJI = MessageEntityType('custom_emoji')

POLL_TYPE_REGULAR = PollType('regular')
POLL_TYPE_QUIZ = PollType('quiz')

CHAT_MEMBER_STATUS_CREATOR = ChatMemberStatus('creator')
CHAT_MEMBER_STATUS_ADMINISTRATOR = ChatMemberStatus('administrator')
CHAT_MEMBER_STATUS_MEMBER = ChatMemberStatus('member')
CHAT_MEMBER_STATUS_RESTRICTED = ChatMemberStatus('restricted')
CHAT_MEMBER_STATUS_LEFT = ChatMemberStatus('left')
CHAT_MEMBER_STATUS_KICKED = ChatMemberStatus('kicked')

BOT_COMMAND_SCOPE_TYPE_DEFAULT = BotCommandScopeType('default')
BOT_COMMAND_SCOPE_TYPE_ALL_PRIVATE_CHATS = BotCommandScopeType('all_private_chats')
BOT_COMMAND_SCOPE_TYPE_ALL_GROUP_CHATS = BotCommandScopeType('all_group_chats')
BOT_COMMAND_SCOPE_TYPE_ALL_CHAT_ADMINISTRATORS = BotCommandScopeType('all_chat_administrators')
BOT_COMMAND_SCOPE_TYPE_CHAT = BotCommandScopeType('chat')
BOT_COMMAND_SCOPE_TYPE_CHAT_ADMINISTRATORS = BotCommandScopeType('chat_administrators')
BOT_COMMAND_SCOPE_TYPE_CHAT_MEMBER = BotCommandScopeType('chat_member')

MENU_BUTTON_TYPE_COMMANDS = MenuButtonType('commands')
MENU_BUTTON_TYPE_WEB_APP = MenuButtonType('web_app')
MENU_BUTTON_TYPE_DEFAULT = MenuButtonType('default')

INPUT_MEDIA_TYPE_PHOTO = InputMediaType('photo')
INPUT_MEDIA_TYPE_VIDEO = InputMediaType('video')
INPUT_MEDIA_TYPE_ANIMATION = InputMediaType('animation')
INPUT_MEDIA_TYPE_AUDIO = InputMediaType('audio')
INPUT_MEDIA_TYPE_DOCUMENT = InputMediaType('document')

INPUT_FILE_TYPE_STORED = InputFileType('stored')
INPUT_FILE_TYPE_URL = InputFileType('url')
INPUT_FILE_TYPE_PATH = InputFileType('path')

STICKER_TYPE_REGULAR = StickerType('regular')
STICKER_TYPE_MASK = StickerType('mask')
STICKER_TYPE_CUSTOM_EMOJI = StickerType('custom_emoji')

MASK_POSITION_POINT_FOREHEAD = MaskPositionPoint('forehead')
MASK_POSITION_POINT_EYES = MaskPositionPoint('eyes')
MASK_POSITION_POINT_MOUTH = MaskPositionPoint('mouth')
MASK_POSITION_POINT_CHIN = MaskPositionPoint('chin')
