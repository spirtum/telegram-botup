try:
    import ujson as json
except ImportError:
    import json


def _simple_object(kwargs, key, t):
    raw = kwargs.get(key)
    return t(**raw) if raw is not None else None


def _objects_list(kwargs, key, t):
    raw = kwargs.get(key)
    return [t(**v) for v in raw] if raw is not None else list()


def _objects_matrix(kwargs, key, t):
    raw = kwargs.get(key)
    return [[t(**v) for v in line] for line in raw] if raw is not None else list()


def _raw_representation(kwargs, key, t):
    return kwargs


class BaseObject:
    __slots__ = list()
    NESTED = dict()

    def __init__(self, **kwargs):
        for field_name in self.__slots__:
            if field_name not in self.NESTED:
                setattr(self, field_name, kwargs.get(field_name))
            else:
                cfg = self.NESTED[field_name]
                func = cfg[0]
                _class = cfg[1]
                key = cfg[2] if len(cfg) == 3 else field_name
                setattr(self, field_name, func(kwargs, key, _class))

    def as_dict(self):
        result = dict()
        for field_name in self.__slots__:
            value = getattr(self, field_name, None)
            if value is None:
                continue
            if field_name not in self.NESTED:
                result[field_name] = value
                continue
            cfg = self.NESTED[field_name]
            alias = cfg[2] if len(cfg) == 3 else field_name
            if isinstance(value, list):
                if value:
                    result[alias] = [v.as_dict() for v in value]
                continue
            if cfg[0] is _raw_representation:
                result[alias] = value
                continue
            result[alias] = value.as_dict()
        return result

    def is_error(self):
        return isinstance(self, ErrorResponse)


class RawResponse(BaseObject):
    __slots__ = [
        'raw_data',
        'ok',
        'result',
        'description'
    ]
    NESTED = {
        'raw_data': (_raw_representation, None)
    }


class PhotoSize(BaseObject):
    __slots__ = [
        'file_id',
        'file_unique_id',
        'width',
        'height',
        'file_size'
    ]


class ChatPhoto(BaseObject):
    __slots__ = [
        'small_file_id',
        'small_file_unique_id',
        'big_file_id',
        'big_file_unique_id'
    ]


class Contact(BaseObject):
    __slots__ = [
        'phone_number',
        'first_name',
        'last_name',
        'user_id',
        'vcard'
    ]


class ErrorResponse(BaseObject):
    __slots__ = [
        'raw_data',
        'ok',
        'error_code',
        'description'
    ]
    NESTED = {
        'raw_data': (_raw_representation, None)
    }


class ForceReply(BaseObject):
    __slots__ = [
        'force_reply',
        'input_field_placeholder',
        'selective'
    ]


class LoginUrl(BaseObject):
    __slots__ = [
        'url',
        'forward_text',
        'bot_username',
        'request_write_access'
    ]


class InlineKeyboardButton(BaseObject):
    __slots__ = [
        'text',
        'url',
        'login_url',
        'callback_data',
        'switch_inline_query',
        'switch_inline_query_current_chat',
        'callback_game',
        'pay'
    ]
    NESTED = {
        'login_url': (_simple_object, LoginUrl)
    }


class InlineKeyboardMarkup(BaseObject):
    __slots__ = ['inline_keyboard']
    NESTED = {
        'inline_keyboard': (_objects_matrix, InlineKeyboardButton)
    }

    def line(self, *args):
        self.inline_keyboard.append(args)

    @staticmethod
    def callback_data(text, callback_data):
        return InlineKeyboardButton(text=text, callback_data=callback_data)

    @staticmethod
    def login_url(text, login_url):
        return InlineKeyboardButton(text=text, login_url=login_url)

    @staticmethod
    def switch_inline_query(text, switch_inline_query):
        return InlineKeyboardButton(text=text, switch_inline_query=switch_inline_query)

    @staticmethod
    def switch_inline_query_current_chat(text, switch_inline_query_current_chat):
        return InlineKeyboardButton(text=text, switch_inline_query_current_chat=switch_inline_query_current_chat)

    @staticmethod
    def pay(text, pay=True):
        return InlineKeyboardButton(text=text, pay=pay)

    @staticmethod
    def url(text, url):
        return InlineKeyboardButton(text=text, url=url)

    def clear(self):
        self.inline_keyboard.clear()

    def as_dict(self):
        return {'inline_keyboard': [[b.as_dict() for b in line] for line in self.inline_keyboard]}

    def as_json(self):
        return json.dumps(self.as_dict())


class KeyboardButtonPollType(BaseObject):
    __slots__ = ['type']
    REGULAR = {'type': 'regular'}
    QUIZ = {'type': 'quiz'}


class KeyboardButton(BaseObject):
    __slots__ = ['text', 'request_contact', 'request_location', 'request_poll']
    NESTED = {
        'request_poll': (_simple_object, KeyboardButtonPollType)
    }


class ReplyKeyboardMarkup(BaseObject):
    __slots__ = [
        'keyboard',
        'resize_keyboard',
        'one_time_keyboard',
        'input_field_placeholder',
        'selective'
    ]
    NESTED = {
        'keyboard': (_objects_matrix, KeyboardButton)
    }

    def line(self, *args):
        self.keyboard.append(args)

    @staticmethod
    def button(text, request_contact=False, request_location=False, request_poll=None):
        kwargs = dict(text=text, request_contact=request_contact, request_location=request_location)
        if request_poll:
            kwargs['request_poll'] = request_poll
        return KeyboardButton(**kwargs)

    def as_dict(self):
        result = dict()
        for key in self.__slots__:
            value = getattr(self, key, None)
            if value is None:
                continue
            if key == 'keyboard':
                result[key] = [[b.as_dict() for b in line] for line in value]
                continue
            result[key] = value
        return result

    def as_json(self):
        return json.dumps(self.as_dict())


class ReplyKeyboardRemove(BaseObject):
    __slots__ = [
        'remove_keyboard',
        'selective'
    ]

    def as_dict(self):
        result = dict()
        for key in self.__slots__:
            value = getattr(self, key, None)
            if value is None:
                continue
            result[key] = value
        return result

    def as_json(self):
        return json.dumps(self.as_dict())


class Location(BaseObject):
    __slots__ = [
        'longitude',
        'latitude',
        'horizontal_accuracy',
        'live_period',
        'heading',
        'proximity_alert_radius'
    ]


class ChatLocation(BaseObject):
    __slots__ = [
        'location',
        'address'
    ]
    NESTED = {
        'location': (_simple_object, Location)
    }


class PollOption(BaseObject):
    __slots__ = [
        'text',
        'voter_count'
    ]


class User(BaseObject):
    __slots__ = [
        'id',
        'is_bot',
        'first_name',
        'last_name',
        'username',
        'language_code',
        'can_join_groups',
        'can_read_all_group_messages',
        'supports_inline_queries'
    ]


class ChatInviteLink(BaseObject):
    __slots__ = [
        'invite_link',
        'creator',
        'creates_join_request',
        'is_primary',
        'is_revoked',
        'name',
        'expire_date',
        'member_limit',
        'pending_join_request_count'
    ]
    NESTED = {
        'creator': (_simple_object, User)
    }


class MessageEntity(BaseObject):
    __slots__ = [
        'type',
        'offset',
        'length',
        'url',
        'user',
        'language'
    ]
    NESTED = {
        'user': (_simple_object, User)
    }


class PollAnswer(BaseObject):
    __slots__ = [
        'poll_id',
        'user',
        'option_ids'
    ]
    NESTED = {
        'user': (_simple_object, User)
    }


class Poll(BaseObject):
    __slots__ = [
        'id',
        'question',
        'options',
        'total_voter_count',
        'is_closed',
        'is_anonymous',
        'type',
        'allows_multiple_answers',
        'correct_option_id',
        'explanation',
        'explanation_entities',
        'open_period',
        'close_date'
    ]
    NESTED = {
        'options': (_objects_list, PollOption),
        'explanation_entities': (_objects_list, MessageEntity)
    }


class Dice(BaseObject):
    __slots__ = [
        'emoji',
        'value'
    ]


class ResponseParameters(BaseObject):
    __slots__ = [
        'migrate_to_chat_id',
        'retry_after'
    ]


class ProximityAlertTriggered(BaseObject):
    __slots__ = [
        'traveler',
        'watcher',
        'distance'
    ]
    NESTED = {
        'traveler': (_simple_object, User),
        'watcher': (_simple_object, User)
    }


class MessageAutoDeleteTimerChanged(BaseObject):
    __slots__ = [
        'message_auto_delete_time'
    ]


class VoiceChatScheduled(BaseObject):
    __slots__ = [
        'start_date'
    ]


class VoiceChatStarted(BaseObject):
    pass


class VoiceChatEnded(BaseObject):
    __slots__ = [
        'duration'
    ]


class VoiceChatParticipantsInvited(BaseObject):
    __slots__ = [
        'users'
    ]
    NESTED = {
        'users': (_objects_list, User)
    }


class UserProfilePhotos(BaseObject):
    __slots__ = [
        'total_count',
        'photos'
    ]
    NESTED = {
        'photos': (_objects_list, PhotoSize)
    }


class Venue(BaseObject):
    __slots__ = [
        'location',
        'title',
        'address',
        'foursquare_id',
        'foursquare_type',
        'google_place_id',
        'google_place_type'
    ]
    NESTED = {
        'location': (_simple_object, Location)
    }


class Video(BaseObject):
    __slots__ = [
        'file_id',
        'file_unique_id',
        'width',
        'height',
        'duration',
        'thumb',
        'file_name',
        'mime_type',
        'file_size'
    ]
    NESTED = {
        'thumb': (_simple_object, PhotoSize)
    }


class VideoNote(BaseObject):
    __slots__ = [
        'file_id',
        'file_unique_id',
        'length',
        'duration',
        'thumb',
        'file_size'
    ]
    NESTED = {
        'thumb': (_simple_object, PhotoSize)
    }


class Voice(BaseObject):
    __slots__ = [
        'file_id',
        'file_unique_id',
        'duration',
        'mime_type',
        'file_size'
    ]


class WebhookInfo(BaseObject):
    __slots__ = [
        'url',
        'has_custom_certificate',
        'pending_update_count',
        'ip_address',
        'last_error_date',
        'last_error_message',
        'max_connections',
        'allowed_updates'
    ]


class Animation(BaseObject):
    __slots__ = [
        'file_id',
        'file_unique_id',
        'width',
        'height',
        'duration',
        'thumb',
        'file_name',
        'mime_type',
        'file_size'
    ]
    NESTED = {
        'thumb': (_simple_object, PhotoSize)
    }


class Audio(BaseObject):
    __slots__ = [
        'file_id',
        'file_unique_id',
        'duration',
        'performer',
        'title',
        'file_name',
        'mime_type',
        'file_size',
        'thumb'
    ]
    NESTED = {
        'thumb': (_simple_object, PhotoSize)
    }


class ChatMemberOwner(BaseObject):
    __slots__ = [
        'status',
        'user',
        'is_anonymous',
        'custom_title'
    ]
    NESTED = {
        'user': (_simple_object, User)
    }


class ChatMemberAdministrator(BaseObject):
    __slots__ = [
        'status',
        'user',
        'can_be_edited',
        'is_anonymous',
        'can_manage_chat',
        'can_delete_messages',
        'can_manage_voice_chats',
        'can_restrict_members',
        'can_promote_members',
        'can_change_info',
        'can_invite_users',
        'can_post_messages',
        'can_edit_messages',
        'can_pin_messages',
        'custom_title'
    ]
    NESTED = {
        'user': (_simple_object, User)
    }


class ChatMemberMember(BaseObject):
    __slots__ = [
        'status',
        'user'
    ]
    NESTED = {
        'user': (_simple_object, User)
    }


class ChatMemberRestricted(BaseObject):
    __slots__ = [
        'status',
        'user',
        'is_member',
        'can_change_info',
        'can_invite_users',
        'can_pin_messages',
        'can_send_messages',
        'can_send_media_messages',
        'can_send_polls',
        'can_send_other_messages',
        'can_add_web_page_previews',
        'until_date'
    ]
    NESTED = {
        'user': (_simple_object, User)
    }


class ChatMemberLeft(BaseObject):
    __slots__ = [
        'status',
        'user'
    ]
    NESTED = {
        'user': (_simple_object, User)
    }


class ChatMemberBanned(BaseObject):
    __slots__ = [
        'status',
        'user',
        'until_date'
    ]
    NESTED = {
        'user': (_simple_object, User)
    }


class ChatMember:

    _dispatch_map = {
        'creator': ChatMemberOwner,
        'administrator': ChatMemberAdministrator,
        'member': ChatMemberMember,
        'restricted': ChatMemberRestricted,
        'left': ChatMemberLeft,
        'kicked': ChatMemberBanned
    }

    def __new__(cls, **kwargs):
        _class = cls._dispatch_map[kwargs['status']]
        return _class(**kwargs)


class Document(BaseObject):
    __slots__ = [
        'file_id',
        'file_unique_id',
        'thumb',
        'file_name',
        'mime_type',
        'file_size'
    ]
    NESTED = {
        'thumb': (_simple_object, PhotoSize)
    }


class File(BaseObject):
    __slots__ = [
        'file_id',
        'file_unique_id',
        'file_size',
        'file_path'
    ]


class InputFile(BaseObject):
    __slots__ = [
        'file_id',
        'url',
        'path',
        'caption',
        'parse_mode'
    ]


class InputMedia(BaseObject):
    pass


class InputMediaAnimation(InputMedia):
    __slots__ = [
        'type',
        'media',
        'caption',
        'parse_mode',
        'caption_entities',
        'thumb',
        'width',
        'height',
        'duration'
    ]
    NESTED = {
        'thumb': (_simple_object, InputFile),
        'caption_entities': (_objects_list, MessageEntity)
    }


class InputMediaAudio(InputMedia):
    __slots__ = [
        'type',
        'media',
        'caption',
        'parse_mode',
        'caption_entities',
        'thumb',
        'duration',
        'performer',
        'title'
    ]
    NESTED = {
        'thumb': (_simple_object, InputFile),
        'caption_entities': (_objects_list, MessageEntity)
    }


class InputMediaDocument(InputMedia):
    __slots__ = [
        'type',
        'media',
        'caption',
        'parse_mode',
        'caption_entities',
        'thumb',
        'disable_content_type_detection'
    ]
    NESTED = {
        'thumb': (_simple_object, InputFile),
        'caption_entities': (_objects_list, MessageEntity)
    }


class InputMediaPhoto(InputMedia):
    __slots__ = [
        'type',
        'media',
        'caption',
        'parse_mode',
        'caption_entities'
    ]
    NESTED = {
        'caption_entities': (_objects_list, MessageEntity)
    }


class InputMediaVideo(InputMedia):
    __slots__ = [
        'type',
        'media',
        'caption',
        'parse_mode',
        'caption_entities',
        'thumb',
        'width',
        'height',
        'duration',
        'supports_streaming'
    ]
    NESTED = {
        'thumb': (_simple_object, InputFile),
        'caption_entities': (_objects_list, MessageEntity)
    }


class Game(BaseObject):
    __slots__ = [
        'title',
        'description',
        'photo',
        'text',
        'text_entities',
        'animation'
    ]
    NESTED = {
        'photo': (_objects_list, PhotoSize),
        'text_entities': (_objects_list, MessageEntity),
        'animation': (_simple_object, Animation)
    }


class GameHighScore(BaseObject):
    __slots__ = [
        'position',
        'user',
        'score'
    ]
    NESTED = {
        'user': (_simple_object, User)
    }


class LabeledPrice(BaseObject):
    __slots__ = [
        'label',
        'amount'
    ]


class InputMessageContent:

    def __new__(cls, **kwargs):
        if not kwargs:
            return
        if 'phone_number' in kwargs:
            return InputContactMessageContent(**kwargs)
        elif 'latitude' in kwargs and 'address' in kwargs:
            return InputVenueMessageContent(**kwargs)
        elif 'latitude' in kwargs:
            return InputLocationMessageContent(**kwargs)
        elif 'message_text' in kwargs:
            return InputTextMessageContent(**kwargs)
        elif 'currency' in kwargs:
            return InputInvoiceMessageContent(**kwargs)


class InputContactMessageContent(BaseObject):
    __slots__ = [
        'phone_number',
        'first_name',
        'last_name',
        'vcard'
    ]


class InputLocationMessageContent(BaseObject):
    __slots__ = [
        'latitude',
        'longitude',
        'live_period',
        'horizontal_accuracy',
        'heading',
        'proximity_alert_radius'
    ]


class InputTextMessageContent(BaseObject):
    __slots__ = [
        'message_text',
        'parse_mode',
        'disable_web_page_preview'
    ]


class InputVenueMessageContent(BaseObject):
    __slots__ = [
        'latitude',
        'longitude',
        'title',
        'address',
        'foursquare_id',
        'foursquare_type',
        'google_place_id',
        'google_place_type'
    ]


class InputInvoiceMessageContent(BaseObject):
    __slots__ = [
        'title',
        'description',
        'payload',
        'provider_token',
        'currency',
        'prices',
        'max_tip_amount',
        'suggested_tip_amounts',
        'provider_data',
        'photo_url',
        'photo_size',
        'photo_width',
        'photo_height',
        'need_name',
        'need_phone_number',
        'need_email',
        'need_shipping_address',
        'send_phone_number_to_provider',
        'send_email_to_provider',
        'is_flexible'
    ]
    NESTED = {
        'prices': (_objects_list, LabeledPrice)
    }


class ChosenInlineResult(BaseObject):
    __slots__ = [
        'result_id',
        'from_',
        'location',
        'inline_message_id',
        'query'
    ]
    NESTED = {
        'from_': (_simple_object, User, 'from'),
        'location': (_simple_object, Location)
    }


class InlineQuery(BaseObject):
    __slots__ = [
        'id',
        'from_',
        'location',
        'query',
        'offset',
        'chat_type'
    ]
    NESTED = {
        'from_': (_simple_object, User, 'from'),
        'location': (_simple_object, Location)
    }


class InlineQueryResult(BaseObject):
    pass


class InlineQueryResultArticle(InlineQueryResult):
    __slots__ = [
        'type',
        'id',
        'reply_markup',
        'input_message_content',
        'title',
        'url',
        'hide_url',
        'description',
        'thumb_url',
        'thumb_width',
        'thumb_height'
    ]
    NESTED = {
        'reply_markup': (_simple_object, InlineKeyboardMarkup),
        'input_message_content': (_simple_object, InputMessageContent)
    }


class InlineQueryResultAudio(InlineQueryResult):
    __slots__ = [
        'type',
        'id',
        'reply_markup',
        'input_message_content',
        'audio_url',
        'parse_mode',
        'title',
        'caption',
        'performer',
        'audio_duration',
        'caption_entities'
    ]
    NESTED = {
        'reply_markup': (_simple_object, InlineKeyboardMarkup),
        'input_message_content': (_simple_object, InputMessageContent),
        'caption_entities': (_objects_list, MessageEntity)
    }


class InlineQueryResultCachedAudio(InlineQueryResult):
    __slots__ = [
        'type',
        'id',
        'reply_markup',
        'input_message_content',
        'audio_file_id',
        'caption',
        'parse_mode',
        'caption_entities'
    ]
    NESTED = {
        'reply_markup': (_simple_object, InlineKeyboardMarkup),
        'input_message_content': (_simple_object, InputMessageContent),
        'caption_entities': (_objects_list, MessageEntity)
    }


class InlineQueryResultCachedDocument(InlineQueryResult):
    __slots__ = [
        'type',
        'id',
        'reply_markup',
        'input_message_content',
        'caption_entities',
        'title',
        'document_file_id',
        'description',
        'caption',
        'parse_mode'
    ]
    NESTED = {
        'reply_markup': (_simple_object, InlineKeyboardMarkup),
        'input_message_content': (_simple_object, InputMessageContent),
        'caption_entities': (_objects_list, MessageEntity)
    }


class InlineQueryResultCachedGif(InlineQueryResult):
    __slots__ = [
        'type',
        'id',
        'reply_markup',
        'input_message_content',
        'gif_file_id',
        'title', 'caption',
        'parse_mode',
        'caption_entities'
    ]
    NESTED = {
        'reply_markup': (_simple_object, InlineKeyboardMarkup),
        'input_message_content': (_simple_object, InputMessageContent),
        'caption_entities': (_objects_list, MessageEntity)
    }


class InlineQueryResultCachedMpeg4Gif(InlineQueryResult):
    __slots__ = [
        'type',
        'id',
        'reply_markup',
        'input_message_content',
        'mpeg4_file_id',
        'title',
        'caption',
        'parse_mode',
        'caption_entities'
    ]
    NESTED = {
        'reply_markup': (_simple_object, InlineKeyboardMarkup),
        'input_message_content': (_simple_object, InputMessageContent),
        'caption_entities': (_objects_list, MessageEntity)
    }


class InlineQueryResultCachedPhoto(InlineQueryResult):
    __slots__ = [
        'type',
        'id',
        'reply_markup',
        'input_message_content',
        'caption_entities',
        'photo_file_id',
        'title',
        'description',
        'caption',
        'parse_mode'
    ]
    NESTED = {
        'reply_markup': (_simple_object, InlineKeyboardMarkup),
        'input_message_content': (_simple_object, InputMessageContent),
        'caption_entities': (_objects_list, MessageEntity)
    }


class InlineQueryResultCachedSticker(InlineQueryResult):
    __slots__ = [
        'type',
        'id',
        'reply_markup',
        'input_message_content',
        'sticker_file_id'
    ]
    NESTED = {
        'reply_markup': (_simple_object, InlineKeyboardMarkup),
        'input_message_content': (_simple_object, InputMessageContent)
    }


class InlineQueryResultCachedVideo(InlineQueryResult):
    __slots__ = [
        'type',
        'id',
        'reply_markup',
        'input_message_content',
        'video_file_id',
        'title',
        'description',
        'caption',
        'parse_mode',
        'caption_entities'
    ]
    NESTED = {
        'reply_markup': (_simple_object, InlineKeyboardMarkup),
        'input_message_content': (_simple_object, InputMessageContent),
        'caption_entities': (_objects_list, MessageEntity)
    }


class InlineQueryResultCachedVoice(InlineQueryResult):
    __slots__ = [
        'type',
        'id',
        'reply_markup',
        'input_message_content',
        'voice_file_id',
        'title',
        'caption',
        'parse_mode',
        'caption_entities'
    ]
    NESTED = {
        'reply_markup': (_simple_object, InlineKeyboardMarkup),
        'input_message_content': (_simple_object, InputMessageContent),
        'caption_entities': (_objects_list, MessageEntity)
    }


class InlineQueryResultContact(InlineQueryResult):
    __slots__ = [
        'type',
        'id',
        'reply_markup',
        'input_message_content',
        'phone_number',
        'first_name',
        'last_name',
        'vcard',
        'thumb_url',
        'thumb_width',
        'thumb_height'
    ]
    NESTED = {
        'reply_markup': (_simple_object, InlineKeyboardMarkup),
        'input_message_content': (_simple_object, InputMessageContent)
    }


class InlineQueryResultDocument(InlineQueryResult):
    __slots__ = [
        'type',
        'id',
        'reply_markup',
        'input_message_content',
        'title',
        'caption',
        'parse_mode',
        'document_url',
        'mime_type',
        'description',
        'thumb_url',
        'thumb_width',
        'thumb_height',
        'caption_entities'
    ]
    NESTED = {
        'reply_markup': (_simple_object, InlineKeyboardMarkup),
        'input_message_content': (_simple_object, InputMessageContent),
        'caption_entities': (_objects_list, MessageEntity)
    }


class InlineQueryResultGame(InlineQueryResult):
    __slots__ = [
        'type',
        'id',
        'reply_markup',
        'game_short_name'
    ]
    NESTED = {
        'reply_markup': (_simple_object, InlineKeyboardMarkup)
    }


class InlineQueryResultGif(InlineQueryResult):
    __slots__ = [
        'type',
        'id',
        'reply_markup',
        'input_message_content',
        'gif_url',
        'gif_width',
        'gif_height',
        'gif_duration',
        'thumb_url',
        'thumb_mime_type',
        'title',
        'caption',
        'parse_mode',
        'caption_entities'
    ]
    NESTED = {
        'reply_markup': (_simple_object, InlineKeyboardMarkup),
        'input_message_content': (_simple_object, InputMessageContent),
        'caption_entities': (_objects_list, MessageEntity)
    }


class InlineQueryResultLocation(InlineQueryResult):
    __slots__ = [
        'type',
        'id',
        'reply_markup',
        'input_message_content',
        'latitude',
        'longitude',
        'title',
        'live_period',
        'thumb_url',
        'thumb_width',
        'thumb_height',
        'horizontal_accuracy',
        'heading',
        'proximity_alert_radius'
    ]
    NESTED = {
        'reply_markup': (_simple_object, InlineKeyboardMarkup),
        'input_message_content': (_simple_object, InputMessageContent)
    }


class InlineQueryResultMpeg4Gif(InlineQueryResult):
    __slots__ = [
        'type',
        'id',
        'reply_markup',
        'input_message_content',
        'mpeg4_url',
        'mpeg4_width',
        'mpeg4_height',
        'mpeg4_duration',
        'thumb_url',
        'thumb_mime_type',
        'title',
        'caption',
        'parse_mode',
        'caption_entities'
    ]
    NESTED = {
        'reply_markup': (_simple_object, InlineKeyboardMarkup),
        'input_message_content': (_simple_object, InputMessageContent),
        'caption_entities': (_objects_list, MessageEntity)
    }


class InlineQueryResultPhoto(InlineQueryResult):
    __slots__ = [
        'type',
        'id',
        'reply_markup',
        'input_message_content',
        'photo_url',
        'thumb_url',
        'photo_width',
        'photo_height',
        'title',
        'description',
        'caption',
        'parse_mode',
        'caption_entities'
    ]
    NESTED = {
        'reply_markup': (_simple_object, InlineKeyboardMarkup),
        'input_message_content': (_simple_object, InputMessageContent),
        'caption_entities': (_objects_list, MessageEntity)
    }


class InlineQueryResultVenue(InlineQueryResult):
    __slots__ = [
        'type',
        'id',
        'reply_markup',
        'input_message_content',
        'latitude',
        'longitude',
        'title',
        'address',
        'foursquare_id',
        'foursquare_type',
        'thumb_url',
        'thumb_width',
        'thumb_height',
        'google_place_id',
        'google_place_type'
    ]
    NESTED = {
        'reply_markup': (_simple_object, InlineKeyboardMarkup),
        'input_message_content': (_simple_object, InputMessageContent)
    }


class InlineQueryResultVideo(InlineQueryResult):
    __slots__ = [
        'type',
        'id',
        'reply_markup',
        'input_message_content',
        'video_url',
        'mime_type',
        'thumb_url',
        'title',
        'caption',
        'parse_mode',
        'video_width',
        'video_height',
        'video_duration',
        'description',
        'caption_entities'
    ]
    NESTED = {
        'reply_markup': (_simple_object, InlineKeyboardMarkup),
        'input_message_content': (_simple_object, InputMessageContent),
        'caption_entities': (_objects_list, MessageEntity)
    }


class InlineQueryResultVoice(InlineQueryResult):
    __slots__ = [
        'type',
        'id',
        'reply_markup',
        'input_message_content',
        'voice_url',
        'title',
        'caption',
        'parse_mode',
        'voice_duration',
        'caption_entities'
    ]
    NESTED = {
        'reply_markup': (_simple_object, InlineKeyboardMarkup),
        'input_message_content': (_simple_object, InputMessageContent),
        'caption_entities': (_objects_list, MessageEntity)
    }


class PassportElementError(BaseObject):
    pass


class PassportElementErrorDataField(PassportElementError):
    __slots__ = [
        'source',
        'type',
        'message',
        'field_name',
        'data_hash'
    ]


class PassportElementErrorFile(PassportElementError):
    __slots__ = [
        'source',
        'type',
        'message',
        'file_hash'
    ]


class PassportElementErrorFiles(PassportElementError):
    __slots__ = [
        'source',
        'type',
        'message',
        'file_hashes'
    ]


class PassportElementErrorFrontSide(PassportElementError):
    __slots__ = [
        'source',
        'type',
        'message',
        'file_hash'
    ]


class PassportElementErrorReverseSide(PassportElementError):
    __slots__ = [
        'source',
        'type',
        'message',
        'file_hash'
    ]


class PassportElementErrorSelfie(PassportElementError):
    __slots__ = [
        'source',
        'type',
        'message',
        'file_hash'
    ]


class PassportElementErrorTranslationFile(PassportElementError):
    __slots__ = [
        'source',
        'type',
        'message',
        'file_hash'
    ]


class PassportElementErrorTranslationFiles(PassportElementError):
    __slots__ = [
        'source',
        'type',
        'message',
        'file_hashes'
    ]


class PassportElementErrorUnspecified(PassportElementError):
    __slots__ = [
        'source',
        'type',
        'message',
        'element_hash'
    ]


class EncryptedCredentials(BaseObject):
    __slots__ = [
        'data',
        'hash',
        'secret'
    ]


class PassportFile(BaseObject):
    __slots__ = [
        'file_id',
        'file_unique_id',
        'file_size',
        'file_date'
    ]


class EncryptedPassportElement(BaseObject):
    __slots__ = [
        'type',
        'data',
        'phone_number',
        'email',
        'files',
        'front_side',
        'reverse_side',
        'selfie',
        'translation',
        'hash'
    ]
    NESTED = {
        'files': (_objects_list, PassportFile),
        'front_side': (_simple_object, PassportFile),
        'reverse_side': (_simple_object, PassportFile),
        'selfie': (_simple_object, PassportFile),
        'translation': (_objects_list, PassportFile)
    }


class PassportData(BaseObject):
    __slots__ = [
        'data',
        'credentials'
    ]
    NESTED = {
        'data': (_objects_list, EncryptedPassportElement),
        'credentials': (_simple_object, EncryptedCredentials)
    }


class Invoice(BaseObject):
    __slots__ = [
        'title',
        'description',
        'start_parameter',
        'currency',
        'total_amount'
    ]


class ShippingAddress(BaseObject):
    __slots__ = [
        'country_code',
        'state',
        'city',
        'street_line1',
        'street_line2',
        'post_code'
    ]


class OrderInfo(BaseObject):
    __slots__ = [
        'name',
        'phone_number',
        'email',
        'shipping_address'
    ]
    NESTED = {
        'shipping_address': (_simple_object, ShippingAddress)
    }


class PreCheckoutQuery(BaseObject):
    __slots__ = [
        'id',
        'from_',
        'currency',
        'total_amount',
        'invoice_payload',
        'shipping_option_id',
        'order_info'
    ]
    NESTED = {
        'from_': (_simple_object, User, 'from'),
        'order_info': (_simple_object, OrderInfo)
    }


class ShippingOption(BaseObject):
    __slots__ = [
        'id',
        'title',
        'prices'
    ]
    NESTED = {
        'prices': (_objects_list, LabeledPrice)
    }


class ShippingQuery(BaseObject):
    __slots__ = [
        'id',
        'from_',
        'invoice_payload',
        'shipping_address'
    ]
    NESTED = {
        'from_': (_simple_object, User, 'from'),
        'shipping_address': (_simple_object, ShippingAddress)
    }


class SuccessfulPayment(BaseObject):
    __slots__ = [
        'currency',
        'total_amount',
        'invoice_payload',
        'shipping_option_id',
        'order_info',
        'telegram_payment_charge_id',
        'provider_payment_charge_id'
    ]
    NESTED = {
        'order_info': (_simple_object, OrderInfo)
    }


class MaskPosition(BaseObject):
    __slots__ = [
        'point',
        'x_shift',
        'y_shift',
        'scale'
    ]


class Sticker(BaseObject):
    __slots__ = [
        'file_id',
        'file_unique_id',
        'width',
        'height',
        'is_animated',
        'thumb',
        'emoji',
        'set_name',
        'mask_position',
        'file_size'
    ]
    NESTED = {
        'thumb': (_simple_object, PhotoSize),
        'mask_position': (_simple_object, MaskPosition)
    }


class StickerSet(BaseObject):
    __slots__ = [
        'name',
        'title',
        'is_animated',
        'contains_masks',
        'stickers',
        'thumb'
    ]
    NESTED = {
        'stickers': (_objects_list, Sticker),
        'thumb': (_simple_object, PhotoSize)
    }


class ChatPermissions(BaseObject):
    __slots__ = [
        'can_send_messages',
        'can_send_media_messages',
        'can_send_polls',
        'can_send_other_messages',
        'can_add_web_page_previews',
        'can_change_info',
        'can_invite_users',
        'can_pin_messages'
    ]


class BotCommand(BaseObject):
    __slots__ = [
        'command',
        'description'
    ]





class BotCommandScopeDefault(BaseObject):
    __slots__ = [
        'type'
    ]


class BotCommandScopeAllPrivateChats(BaseObject):
    __slots__ = [
        'type'
    ]


class BotCommandScopeAllGroupChats(BaseObject):
    __slots__ = [
        'type'
    ]


class BotCommandScopeAllChatAdministrators(BaseObject):
    __slots__ = [
        'type'
    ]


class BotCommandScopeChat(BaseObject):
    __slots__ = [
        'type',
        'chat_id'
    ]


class BotCommandScopeChatAdministrators(BaseObject):
    __slots__ = [
        'type',
        'chat_id'
    ]


class BotCommandScopeChatMember(BaseObject):
    __slots__ = [
        'type',
        'chat_id',
        'user_id'
    ]


class BotCommandScope:

    _dispatch_map = {
        'default': BotCommandScopeDefault,
        'all_private_chats': BotCommandScopeAllPrivateChats,
        'all_group_chats': BotCommandScopeAllGroupChats,
        'all_chat_administrators': BotCommandScopeAllChatAdministrators,
        'chat': BotCommandScopeChat,
        'chat_administrators': BotCommandScopeChatAdministrators,
        'chat_member': BotCommandScopeChatMember
    }

    def __new__(cls, **kwargs):
        _class = cls._dispatch_map[kwargs['type']]
        return _class(**kwargs)


class Chat(BaseObject):
    __slots__ = [
        'id',
        'type',
        'title',
        'username',
        'first_name',
        'last_name',
        'photo',
        'description',
        'invite_link',
        'pinned_message',
        'permissions',
        'slow_mode_delay',
        'sticker_set_name',
        'can_set_sticker_set',
        'location'
    ]
    NESTED = {
        'photo': (_simple_object, ChatPhoto),
        'pinned_message': (_raw_representation, None),
        'permissions': (_simple_object, ChatPermissions),
        'location': (_simple_object, ChatLocation)
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pinned_message = Message(**kwargs['pinned_message']) if 'pinned_message' in kwargs else None


class ChatMemberUpdated(BaseObject):
    __slots__ = [
        'chat',
        'from_',
        'date',
        'old_chat_member',
        'new_chat_member',
        'invite_link'
    ]
    NESTED = {
        'chat': (_simple_object, Chat),
        'from_': (_simple_object, User, 'from'),
        'old_chat_member': (_simple_object, ChatMember),
        'new_chat_member': (_simple_object, ChatMember),
        'invite_link': (_simple_object, ChatInviteLink)
    }


class ChatJoinRequest(BaseObject):
    __slots__ = [
        'chat',
        'from_',
        'date',
        'bio',
        'invite_link'
    ]
    NESTED = {
        'chat': (_simple_object, Chat),
        'from_': (_simple_object, User, 'from'),
        'invite_link': (_simple_object, ChatInviteLink)
    }


class Message(BaseObject):
    __slots__ = [
        'message_id',
        'from_',
        'sender_chat',
        'date',
        'chat',
        'forward_from_chat',
        'forward_from',
        'forward_signature',
        'forward_sender_name',
        'forward_date',
        'reply_to_message',
        'via_bot',
        'edit_date',
        'media_group_id',
        'author_signature',
        'text',
        'entities',
        'caption_entities',
        'audio',
        'document',
        'animation',
        'game',
        'photo',
        'sticker',
        'video',
        'voice',
        'video_note',
        'caption',
        'contact',
        'location',
        'venue',
        'poll',
        'dice',
        'new_chat_members',
        'left_chat_member',
        'new_chat_title',
        'new_chat_photo',
        'delete_chat_photo',
        'group_chat_created',
        'supergroup_chat_created',
        'channel_chat_created',
        'message_auto_delete_timer_changed',
        'migrate_to_chat_id',
        'migrate_from_chat_id',
        'pinned_message',
        'invoice',
        'successful_payment',
        'connected_website',
        'passport_data',
        'proximity_alert_triggered',
        'voice_chat_scheduled',
        'voice_chat_started',
        'voice_chat_ended',
        'voice_chat_participants_invited',
        'reply_markup'
    ]
    NESTED = {
        'from_': (_simple_object, User, 'from'),
        'sender_chat': (_simple_object, Chat),
        'chat': (_simple_object, Chat),
        'forward_from_chat': (_simple_object, Chat),
        'forward_from': (_simple_object, User),
        'reply_to_message': (_raw_representation, None),
        'via_bot': (_simple_object, User),
        'entities': (_objects_list, MessageEntity),
        'caption_entities': (_objects_list, MessageEntity),
        'audio': (_simple_object, Audio),
        'document': (_simple_object, Document),
        'animation': (_simple_object, Animation),
        'game': (_simple_object, Game),
        'photo': (_objects_list, PhotoSize),
        'sticker': (_simple_object, Sticker),
        'video': (_simple_object, Video),
        'voice': (_simple_object, Voice),
        'video_note': (_simple_object, VideoNote),
        'contact': (_simple_object, Contact),
        'location': (_simple_object, Location),
        'venue': (_simple_object, Venue),
        'poll': (_simple_object, Poll),
        'dice': (_simple_object, Dice),
        'new_chat_members': (_objects_list, User),
        'left_chat_member': (_simple_object, User),
        'new_chat_photo': (_objects_list, PhotoSize),
        'message_auto_delete_timer_changed': (_simple_object, MessageAutoDeleteTimerChanged),
        'pinned_message': (_raw_representation, None),
        'invoice': (_simple_object, Invoice),
        'successful_payment': (_simple_object, SuccessfulPayment),
        'passport_data': (_simple_object, PassportData),
        'proximity_alert_triggered': (_simple_object, ProximityAlertTriggered),
        'voice_chat_scheduled': (_simple_object, VoiceChatScheduled),
        'voice_chat_started': (_simple_object, VoiceChatStarted),
        'voice_chat_ended': (_simple_object, VoiceChatEnded),
        'voice_chat_participants_invited': (_simple_object, VoiceChatParticipantsInvited),
        'reply_markup': (_simple_object, InlineKeyboardMarkup)
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reply_to_message = Message(**kwargs['reply_to_message']) if 'reply_to_message' in kwargs else None
        self.pinned_message = Message(**kwargs['pinned_message']) if 'pinned_message' in kwargs else None


class CallbackQuery(BaseObject):
    __slots__ = [
        'id',
        'from_',
        'message',
        'inline_message_id',
        'chat_instance',
        'data',
        'game_short_name'
    ]
    NESTED = {
        'from_': (_simple_object, User, 'from'),
        'message': (_simple_object, Message)
    }


class Update(BaseObject):
    __slots__ = [
        'update_id',
        'message',
        'edited_message',
        'channel_post',
        'edited_channel_post',
        'inline_query',
        'chosen_inline_result',
        'callback_query',
        'shipping_query',
        'pre_checkout_query',
        'poll',
        'poll_answer',
        'my_chat_member',
        'chat_member',
        'chat_join_request'
    ]
    NESTED = {
        'message': (_simple_object, Message),
        'edited_message': (_simple_object, Message),
        'channel_post': (_simple_object, Message),
        'edited_channel_post': (_simple_object, Message),
        'inline_query': (_simple_object, InlineQuery),
        'chosen_inline_result': (_simple_object, ChosenInlineResult),
        'callback_query': (_simple_object, CallbackQuery),
        'shipping_query': (_simple_object, ShippingQuery),
        'pre_checkout_query': (_simple_object, PreCheckoutQuery),
        'poll': (_simple_object, Poll),
        'poll_answer': (_simple_object, PollAnswer),
        'my_chat_member': (_simple_object, ChatMemberUpdated),
        'chat_member': (_simple_object, ChatMemberUpdated),
        'chat_join_request': (_simple_object, ChatJoinRequest)
    }


class TelegramResponse:

    def __new__(cls, data):
        if not isinstance(data, dict):
            data = json.loads(data)
        status = data.get('ok')
        result = data.get('result')
        if not status:
            return ErrorResponse(**data)
        elif isinstance(result, bool) or isinstance(result, str):
            return RawResponse(**data)
        elif isinstance(result, list):
            parsed_result = []
            for item in result:
                if 'update_id' in item:
                    parsed_result.append(Update(**item))
                elif 'command' in item:
                    parsed_result.append(BotCommand(**item))
                elif 'user' in item and 'status' in item:
                    parsed_result.append(ChatMember(**item))
                elif 'user' in item and 'score' in item:
                    parsed_result.append(GameHighScore(**item))
            return parsed_result
        elif 'update_id' in result:
            return Update(**result)
        elif 'message_id' in result:
            return Message(**result)
        elif 'is_bot' in result:
            return User(**result)
        elif 'total_count' in result and 'photos' in result:
            return UserProfilePhotos(**result)
        elif 'file_id' in result and 'file_size' in result and 'file_path' in result:
            return File(**result)
        elif 'type' in result and result['type'] in ('private', 'group', 'supergroup', 'channel'):
            return Chat(**result)
        elif 'user' in result and 'status' in result:
            return ChatMember(**result)
        elif 'question' in result and 'options' in result:
            return Poll(**result)
        elif 'contains_masks' in result and 'stickers' in result:
            return StickerSet(**result)
        elif 'has_custom_certificate' in result:
            return WebhookInfo(**result)
        else:
            return result
