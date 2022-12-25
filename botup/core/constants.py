class StringConstant(str):
    def __new__(cls, *args, **kw):
        return str.__new__(cls, *args, **kw)


class ApiMethod(StringConstant):
    pass


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


class InlineQueryChatType(StringConstant):
    pass


class InlineQueryResultType(StringConstant):
    pass


class EncryptedPassportElementType(StringConstant):
    pass


class PassportElementErrorSource(StringConstant):
    pass


class ChatAction(StringConstant):
    pass


API_METHOD_GET_UPDATES = ApiMethod('getUpdates')
API_METHOD_SET_WEBHOOK = ApiMethod('setWebhook')
API_METHOD_DELETE_WEBHOOK = ApiMethod('deleteWebhook')
API_METHOD_GET_WEBHOOK_INFO = ApiMethod('getWebhookInfo')
API_METHOD_GET_ME = ApiMethod('getMe')
API_METHOD_LOGOUT = ApiMethod('logOut')
API_METHOD_CLOSE = ApiMethod('close')
API_METHOD_SEND_MESSAGE = ApiMethod('sendMessage')
API_METHOD_FORWARD_MESSAGE = ApiMethod('forwardMessage')
API_METHOD_COPY_MESSAGE = ApiMethod('copyMessage')
API_METHOD_SEND_LOCATION = ApiMethod('sendLocation')
API_METHOD_SEND_PHOTO = ApiMethod('sendPhoto')
API_METHOD_SEND_AUDIO = ApiMethod('sendAudio')
API_METHOD_SEND_DOCUMENT = ApiMethod('sendDocument')
API_METHOD_SEND_VIDEO = ApiMethod('sendVideo')
API_METHOD_SEND_ANIMATION = ApiMethod('sendAnimation')
API_METHOD_SEND_VOICE = ApiMethod('sendVoice')
API_METHOD_SEND_VIDEO_NOTE = ApiMethod('sendVideoNote')
API_METHOD_SEND_MEDIA_GROUP = ApiMethod('sendMediaGroup')
API_METHOD_EDIT_MESSAGE_LIVE_LOCATION = ApiMethod('editMessageLiveLocation')
API_METHOD_STOP_MESSAGE_LIVE_LOCATION = ApiMethod('stopMessageLiveLocation')
API_METHOD_SEND_VENUE = ApiMethod('sendVenue')
API_METHOD_SEND_CONTACT = ApiMethod('sendContact')
API_METHOD_SEND_POLL = ApiMethod('sendPoll')
API_METHOD_SEND_DICE = ApiMethod('sendDice')
API_METHOD_SEND_CHAT_ACTION = ApiMethod('sendChatAction')
API_METHOD_GET_USER_PROFILE_PHOTOS = ApiMethod('getUserProfilePhotos')
API_METHOD_GET_FILE = ApiMethod('getFile')
API_METHOD_BAN_CHAT_MEMBER = ApiMethod('banChatMember')
API_METHOD_UNBAN_CHAT_MEMBER = ApiMethod('unbanChatMember')
API_METHOD_RESTRICT_CHAT_MEMBER = ApiMethod('restrictChatMember')
API_METHOD_PROMOTE_CHAT_MEMBER = ApiMethod('promoteChatMember')
API_METHOD_SET_CHAT_ADMINISTRATOR_CUSTOM_TITLE = ApiMethod('setChatAdministratorCustomTitle')
API_METHOD_BAN_CHAT_SENDER_CHAT = ApiMethod('banChatSenderChat')
API_METHOD_UNBAN_CHAT_SENDER_CHAT = ApiMethod('unbanChatSenderChat')
API_METHOD_SET_CHAT_PERMISSIONS = ApiMethod('setChatPermissions')
API_METHOD_EXPORT_CHAT_INVITE_LINK = ApiMethod('exportChatInviteLink')
API_METHOD_CREATE_CHAT_INVITE_LINK = ApiMethod('createChatInviteLink')
API_METHOD_EDIT_CHAT_INVITE_LINK = ApiMethod('editChatInviteLink')
API_METHOD_REVOKE_CHAT_INVITE_LINK = ApiMethod('revokeChatInviteLink')
API_METHOD_APPROVE_CHAT_JOIN_REQUEST = ApiMethod('approveChatJoinRequest')
API_METHOD_DECLINE_CHAT_JOIN_REQUEST = ApiMethod('decline_chat_join_request')
API_METHOD_SET_CHAT_PHOTO = ApiMethod('setChatPhoto')
API_METHOD_DELETE_CHAT_PHOTO = ApiMethod('deleteChatPhoto')
API_METHOD_SET_CHAT_TITLE = ApiMethod('setChatTitle')
API_METHOD_SET_CHAT_DESCRIPTION = ApiMethod('setChatDescription')
API_METHOD_PIN_CHAT_MESSAGE = ApiMethod('pinChatMessage')
API_METHOD_UNPIN_CHAT_MESSAGE = ApiMethod('unpinChatMessage')
API_METHOD_UNPIN_ALL_CHAT_MESSAGES = ApiMethod('unpinAllChatMessages')
API_METHOD_LEAVE_CHAT = ApiMethod('leaveChat')
API_METHOD_GET_CHAT = ApiMethod('getChat')
API_METHOD_GET_CHAT_ADMINISTRATORS = ApiMethod('getChatAdministrators')
API_METHOD_GET_CHAT_MEMBER_COUNT = ApiMethod('getChatMemberCount')
API_METHOD_GET_CHAT_MEMBER = ApiMethod('getChatMember')
API_METHOD_SET_CHAT_STICKER_SET = ApiMethod('setChatStickerSet')
API_METHOD_DELETE_CHAT_STICKER_SET = ApiMethod('deleteChatStickerSet')
API_METHOD_GET_FORUM_TOPIC_ICON_STICKERS = ApiMethod('getForumTopicIconStickers')
API_METHOD_CREATE_FORUM_TOPIC = ApiMethod('createForumTopic')
API_METHOD_EDIT_FORUM_TOPIC = ApiMethod('editForumTopic')
API_METHOD_CLOSE_FORUM_TOPIC = ApiMethod('closeForumTopic')
API_METHOD_REOPEN_FORUM_TOPIC = ApiMethod('reopenForumTopic')
API_METHOD_DELETE_FORUM_TOPIC = ApiMethod('deleteForumTopic')
API_METHOD_UNPIN_ALL_FORUM_TOPIC_MESSAGES = ApiMethod('unpinAllForumTopicMessages')
API_METHOD_ANSWER_CALLBACK_QUERY = ApiMethod('answerCallbackQuery')
API_METHOD_SET_MY_COMMANDS = ApiMethod('setMyCommands')
API_METHOD_DELETE_MY_COMMANDS = ApiMethod('deleteMyCommands')
API_METHOD_GET_MY_COMMANDS = ApiMethod('getMyCommands')
API_METHOD_SET_CHAT_MENU_BUTTON = ApiMethod('setChatMenuButton')
API_METHOD_GET_CHAT_MENU_BUTTON = ApiMethod('getChatMenuButton')
API_METHOD_SET_MY_DEFAULT_ADMINISTRATOR_RIGHTS = ApiMethod('setMyDefaultAdministratorRights')
API_METHOD_GET_MY_DEFAULT_ADMINISTRATOR_RIGHTS = ApiMethod('getMyDefaultAdministratorRights')
API_METHOD_EDIT_MESSAGE_TEXT = ApiMethod('editMessageText')
API_METHOD_EDIT_MESSAGE_CAPTION = ApiMethod('editMessageCaption')
API_METHOD_EDIT_MESSAGE_MEDIA = ApiMethod('editMessageMedia')
API_METHOD_EDIT_MESSAGE_REPLY_MARKUP = ApiMethod('editMessageReplyMarkup')
API_METHOD_STOP_POLL = ApiMethod('stopPoll')
API_METHOD_DELETE_MESSAGE = ApiMethod('deleteMessage')
API_METHOD_SEND_STICKER = ApiMethod('sendSticker')
API_METHOD_GET_STICKER_SET = ApiMethod('getStickerSet')
API_METHOD_GET_CUSTOM_EMOJI_STICKERS = ApiMethod('getCustomEmojiStickers')
API_METHOD_UPLOAD_STICKER_FILE = ApiMethod('uploadStickerFile')
API_METHOD_CREATE_NEW_STICKER_SET = ApiMethod('createNewStickerSet')
API_METHOD_ADD_STICKER_TO_SET = ApiMethod('addStickerToSet')
API_METHOD_SET_STICKER_POSITION_IN_SET = ApiMethod('setStickerPositionInSet')
API_METHOD_DELETE_STICKER_FROM_SET = ApiMethod('deleteStickerFromSet')
API_METHOD_SET_STICKER_SET_THUMB = ApiMethod('setStickerSetThumb')


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

INLINE_QUERY_CHAT_TYPE_SENDER = InlineQueryChatType('sender')
INLINE_QUERY_CHAT_TYPE_PRIVATE = InlineQueryChatType('private')
INLINE_QUERY_CHAT_TYPE_GROUP = InlineQueryChatType('group')
INLINE_QUERY_CHAT_TYPE_SUPERGROUP = InlineQueryChatType('supergroup')
INLINE_QUERY_CHAT_TYPE_CHANNEL = InlineQueryChatType('channel')

INLINE_QUERY_RESULT_TYPE_ARTICLE = InlineQueryResultType('article')
INLINE_QUERY_RESULT_TYPE_PHOTO = InlineQueryResultType('photo')
INLINE_QUERY_RESULT_TYPE_GIF = InlineQueryResultType('gif')
INLINE_QUERY_RESULT_TYPE_MPEG4_GIF = InlineQueryResultType('mpeg4_gif')
INLINE_QUERY_RESULT_TYPE_VIDEO = InlineQueryResultType('video')
INLINE_QUERY_RESULT_TYPE_AUDIO = InlineQueryResultType('audio')
INLINE_QUERY_RESULT_TYPE_VOICE = InlineQueryResultType('voice')
INLINE_QUERY_RESULT_TYPE_DOCUMENT = InlineQueryResultType('document')
INLINE_QUERY_RESULT_TYPE_LOCATION = InlineQueryResultType('location')
INLINE_QUERY_RESULT_TYPE_VENUE = InlineQueryResultType('venue')
INLINE_QUERY_RESULT_TYPE_CONTACT = InlineQueryResultType('contact')
INLINE_QUERY_RESULT_TYPE_GAME = InlineQueryResultType('game')
INLINE_QUERY_RESULT_TYPE_STICKER = InlineQueryResultType('sticker')

ENCRYPTED_PASSPORT_ELEMENT_TYPE_PERSONAL_DETAILS = EncryptedPassportElementType('personal_details')
ENCRYPTED_PASSPORT_ELEMENT_TYPE_PASSPORT = EncryptedPassportElementType('passport')
ENCRYPTED_PASSPORT_ELEMENT_TYPE_DRIVER_LICENSE = EncryptedPassportElementType('driver_license')
ENCRYPTED_PASSPORT_ELEMENT_TYPE_IDENTITY_CARD = EncryptedPassportElementType('identity_card')
ENCRYPTED_PASSPORT_ELEMENT_TYPE_INTERNAL_PASSPORT = EncryptedPassportElementType('internal_passport')
ENCRYPTED_PASSPORT_ELEMENT_TYPE_ADDRESS = EncryptedPassportElementType('address')
ENCRYPTED_PASSPORT_ELEMENT_TYPE_UTILITY_BILL = EncryptedPassportElementType('utility_bill')
ENCRYPTED_PASSPORT_ELEMENT_TYPE_BANK_STATEMENT = EncryptedPassportElementType('bank_statement')
ENCRYPTED_PASSPORT_ELEMENT_TYPE_RENTAL_AGREEMENT = EncryptedPassportElementType('rental_agreement')
ENCRYPTED_PASSPORT_ELEMENT_TYPE_PASSPORT_REGISTRATION = EncryptedPassportElementType('passport_registration')
ENCRYPTED_PASSPORT_ELEMENT_TYPE_TEMPORARY_REGISTRATION = EncryptedPassportElementType('temporary_registration')
ENCRYPTED_PASSPORT_ELEMENT_TYPE_PHONE_NUMBER = EncryptedPassportElementType('phone_number')
ENCRYPTED_PASSPORT_ELEMENT_TYPE_EMAIL = EncryptedPassportElementType('email')

PASSPORT_ELEMENT_ERROR_SOURCE_DATA = PassportElementErrorSource('data')
PASSPORT_ELEMENT_ERROR_SOURCE_FRONT_SIDE = PassportElementErrorSource('front_side')
PASSPORT_ELEMENT_ERROR_SOURCE_REVERSE_SIDE = PassportElementErrorSource('reverse_side')
PASSPORT_ELEMENT_ERROR_SOURCE_SELFIE = PassportElementErrorSource('selfie')
PASSPORT_ELEMENT_ERROR_SOURCE_FILE = PassportElementErrorSource('file')
PASSPORT_ELEMENT_ERROR_SOURCE_FILES = PassportElementErrorSource('files')
PASSPORT_ELEMENT_ERROR_SOURCE_TRANSLATION_FILE = PassportElementErrorSource('translation_file')
PASSPORT_ELEMENT_ERROR_SOURCE_TRANSLATION_FILES = PassportElementErrorSource('translation_files')
PASSPORT_ELEMENT_ERROR_SOURCE_UNSPECIFIED = PassportElementErrorSource('unspecified')

CHAT_ACTION_TYPING = ChatAction('typing')
CHAT_ACTION_UPLOAD_PHOTO = ChatAction('upload_photo')
CHAT_ACTION_RECORD_VIDEO = ChatAction('record_video')
CHAT_ACTION_UPLOAD_VIDEO = ChatAction('upload_video')
CHAT_ACTION_RECORD_VOICE = ChatAction('record_voice')
CHAT_ACTION_UPLOAD_VOICE = ChatAction('upload_voice')
CHAT_ACTION_UPLOAD_DOCUMENT = ChatAction('upload_document')
CHAT_ACTION_CHOOSE_STICKER = ChatAction('choose_sticker')
CHAT_ACTION_FIND_LOCATION = ChatAction('find_location')
CHAT_ACTION_RECORD_VIDEO_NOTE = ChatAction('record_video_note')
CHAT_ACTION_UPLOAD_VIDEO_NOTE = ChatAction('upload_video_note')
