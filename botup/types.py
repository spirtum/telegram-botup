try:
    import ujson as json
except ImportError:
    import json

import pprint


class BaseObject:
    __slots__ = list()
    NESTED = list()

    def as_dict(self):
        result = dict()
        for key in self.__slots__:
            value = getattr(self, key, None)
            if value is None:
                continue
            if key not in self.NESTED:
                result[key] = value
                continue
            if isinstance(value, list):
                if value:
                    result[key] = [v.as_dict() for v in value]
                continue
            result[key] = value.as_dict()
        return result

    def is_error(self):
        return isinstance(self, ErrorResponse)

    def pprint(self):
        pprint.pprint(self.as_dict())

    def pformat(self):
        return pprint.pformat(self.as_dict())


class RawResponse(BaseObject):
    __slots__ = ['raw_data', 'ok', 'result', 'description']

    def __init__(self, **kwargs):
        self.raw_data = kwargs
        self.ok = kwargs.get('ok')
        self.result = kwargs.get('result')
        self.description = kwargs.get('description')


class PhotoSize(BaseObject):
    __slots__ = ['file_id', 'file_unique_id', 'width', 'height', 'file_size']

    def __init__(self, **kwargs):
        self.file_id = kwargs.get('file_id')
        self.file_unique_id = kwargs.get('file_unique_id')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.file_size = kwargs.get('file_size')


class ChatPhoto(BaseObject):
    __slots__ = ['small_file_id', 'small_file_unique_id', 'big_file_id', 'big_file_unique_id']

    def __init__(self, **kwargs):
        self.small_file_id = kwargs.get('small_file_id')
        self.small_file_unique_id = kwargs.get('small_file_unique_id')
        self.big_file_id = kwargs.get('big_file_id')
        self.big_file_unique_id = kwargs.get('big_file_unique_id')


class Contact(BaseObject):
    __slots__ = ['phone_number', 'first_name', 'last_name', 'user_id', 'vcard']

    def __init__(self, **kwargs):
        self.phone_number = kwargs.get('phone_number')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.user_id = kwargs.get('user_id')
        self.vcard = kwargs.get('vcard')


class ErrorResponse(BaseObject):
    __slots__ = ['raw_data', 'ok', 'error_code', 'description']

    def __init__(self, **kwargs):
        self.raw_data = kwargs
        self.ok = kwargs.get('ok')
        self.error_code = kwargs.get('error_code')
        self.description = kwargs.get('description')


class ForceReply(BaseObject):
    __slots__ = ['force_reply', 'selective']

    def __init__(self, **kwargs):
        self.force_reply = kwargs.get('force_reply')
        self.selective = kwargs.get('selective')


class LoginUrl(BaseObject):
    __slots__ = ['url', 'forward_text', 'bot_username', 'request_write_access']

    def __init__(self, **kwargs):
        self.url = kwargs.get('url')
        self.forward_text = kwargs.get('forward_text')
        self.bot_username = kwargs.get('bot_username')
        self.request_write_access = kwargs.get('request_write_access')


class InlineKeyboardButton(BaseObject):
    __slots__ = ['text', 'url', 'login_url', 'callback_data', 'switch_inline_query',
                 'switch_inline_query_current_chat', 'callback_game', 'pay']
    NESTED = ['login_url', ]

    def __init__(self, **kwargs):
        self.text = kwargs.get('text')
        self.url = kwargs.get('url')
        self.login_url = LoginUrl(**kwargs['login_url']) if 'login_url' in kwargs else None
        self.callback_data = kwargs.get('callback_data')
        self.switch_inline_query = kwargs.get('switch_inline_query')
        self.switch_inline_query_current_chat = kwargs.get('switch_inline_query_current_chat')
        self.callback_game = None  # CallbackGame. A placeholder, currently holds no information.
        self.pay = kwargs.get('pay')


class InlineKeyboardMarkup(BaseObject):
    __slots__ = ['inline_keyboard']

    def __init__(self, **kwargs):
        self.inline_keyboard = [
            [InlineKeyboardButton(**v) for v in line] for line in kwargs.get('inline_keyboard', list())
        ]

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


class KeyboardButton(BaseObject):
    __slots__ = ['text', 'request_contact', 'request_location', 'request_poll']
    NESTED = ['request_poll']

    def __init__(self, **kwargs):
        self.text = kwargs.get('text')
        self.request_contact = kwargs.get('request_contact')
        self.request_location = kwargs.get('request_location')
        self.request_poll = KeyboardButtonPollType(**kwargs['request_poll']) if 'request_poll' in kwargs else None


class KeyboardButtonPollType(BaseObject):
    __slots__ = ['type']
    REGULAR = {'type': 'regular'}
    QUIZ = {'type': 'quiz'}

    def __init__(self, **kwargs):
        self.type = kwargs.get('type')


class ReplyKeyboardMarkup(BaseObject):
    __slots__ = ['keyboard', 'resize_keyboard', 'one_time_keyboard', 'selective']

    def __init__(self, **kwargs):
        self.keyboard = [[KeyboardButton(**v) for v in line] for line in kwargs.get('keyboard', list())]
        self.resize_keyboard = kwargs.get('resize_keyboard')
        self.one_time_keyboard = kwargs.get('one_time_keyboard')
        self.selective = kwargs.get('selective')

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
    __slots__ = ['remove_keyboard', 'selective']

    def __init__(self, **kwargs):
        self.remove_keyboard = kwargs.get('remove_keyboard', True)
        self.selective = kwargs.get('selective')

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
    __slots__ = ['longitude', 'latitude', 'horizontal_accuracy', 'live_period', 'heading', 'proximity_alert_radius']

    def __init__(self, **kwargs):
        self.longitude = kwargs.get('longitude')
        self.latitude = kwargs.get('latitude')
        self.horizontal_accuracy = kwargs.get('horizontal_accuracy')
        self.live_period = kwargs.get('live_period')
        self.heading = kwargs.get('heading')
        self.proximity_alert_radius = kwargs.get('proximity_alert_radius')


class ChatLocation(BaseObject):
    __slots__ = ['location', 'address']
    NESTED = ['location']

    def __init__(self, **kwargs):
        self.location = Location(**kwargs['location']) if 'location' in kwargs else None
        self.address = kwargs.get('address')


class PollOption(BaseObject):
    __slots__ = ['text', 'voter_count']

    def __init__(self, **kwargs):
        self.text = kwargs.get('text')
        self.voter_count = kwargs.get('voter_count')


class PollAnswer(BaseObject):
    __slots__ = ['poll_id', 'user', 'option_ids']
    NESTED = ['user']

    def __init__(self, **kwargs):
        self.poll_id = kwargs.get('poll_id')
        self.user = User(**kwargs['user']) if 'user' in kwargs else None
        self.option_ids = kwargs.get('option_ids')


class Poll(BaseObject):
    __slots__ = ['id', 'question', 'options', 'total_voter_count', 'is_closed', 'is_anonymous', 'type',
                 'allows_multiple_answers', 'correct_option_id', 'explanation', 'explanation_entities', 'open_period',
                 'close_date']
    NESTED = ['options', 'explanation_entities']

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.question = kwargs.get('question')
        self.options = [PollOption(**v) for v in kwargs['options']] if 'options' in kwargs else list()
        self.total_voter_count = kwargs.get('total_voter_count')
        self.is_closed = kwargs.get('is_closed')
        self.is_anonymous = kwargs.get('is_anonymous')
        self.type = kwargs.get('type')
        self.allows_multiple_answers = kwargs.get('allows_multiple_answers')
        self.correct_option_id = kwargs.get('correct_option_id')
        self.explanation = kwargs.get('explanation')
        self.explanation_entities = [
            MessageEntity(**v) for v in kwargs['explanation_entities']] if 'explanation_entities' in kwargs else list()
        self.open_period = kwargs.get('open_period')
        self.close_date = kwargs.get('close_date')


class Dice(BaseObject):
    __slots__ = ['emoji', 'value']

    def __init__(self, **kwargs):
        self.emoji = kwargs.get('emoji')
        self.value = kwargs.get('value')


class ResponseParameters(BaseObject):
    __slots__ = ['migrate_to_chat_id', 'retry_after']

    def __init__(self, **kwargs):
        self.migrate_to_chat_id = kwargs.get('migrate_to_chat_id')
        self.retry_after = kwargs.get('retry_after')


class ProximityAlertTriggered(BaseObject):
    __slots__ = ['traveler', 'watcher', 'distance']
    NESTED = ['traveler', 'watcher']

    def __init__(self, **kwargs):
        self.traveler = User(**kwargs['traveler']) if 'traveler' in kwargs else None
        self.watcher = User(**kwargs['watcher']) if 'watcher' in kwargs else None
        self.distance = kwargs.get('distance')


class UserProfilePhotos(BaseObject):
    __slots__ = ['total_count', 'photos']
    NESTED = ['photos', ]

    def __init__(self, **kwargs):
        self.total_count = kwargs.get('total_count')
        self.photos = [PhotoSize(**v) for v in kwargs['photos']] if 'photos' in kwargs else list()


class Venue(BaseObject):
    __slots__ = ['location', 'title', 'address', 'foursquare_id', 'foursquare_type',
                 'google_place_id', 'google_place_type']
    NESTED = ['location', ]

    def __init__(self, **kwargs):
        self.location = Location(**kwargs['location']) if 'location' in kwargs else None
        self.title = kwargs.get('title')
        self.address = kwargs.get('address')
        self.foursquare_id = kwargs.get('foursquare_id')
        self.foursquare_type = kwargs.get('foursquare_type')
        self.google_place_id = kwargs.get('google_place_id')
        self.google_place_type = kwargs.get('google_place_type')


class Video(BaseObject):
    __slots__ = ['file_id', 'file_unique_id', 'width', 'height', 'duration', 'thumb',
                 'file_name', 'mime_type', 'file_size']
    NESTED = ['thumb', ]

    def __init__(self, **kwargs):
        self.file_id = kwargs.get('file_id')
        self.file_unique_id = kwargs.get('file_unique_id')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.duration = kwargs.get('duration')
        self.thumb = PhotoSize(**kwargs['thumb']) if 'thumb' in kwargs else None
        self.file_name = kwargs.get('file_name')
        self.mime_type = kwargs.get('mime_type')
        self.file_size = kwargs.get('file_size')


class VideoNote(BaseObject):
    __slots__ = ['file_id', 'file_unique_id', 'length', 'duration', 'thumb', 'file_size']
    NESTED = ['thumb', ]

    def __init__(self, **kwargs):
        self.file_id = kwargs.get('file_id')
        self.file_unique_id = kwargs.get('file_unique_id')
        self.length = kwargs.get('length')
        self.duration = kwargs.get('duration')
        self.thumb = PhotoSize(**kwargs['thumb']) if 'thumb' in kwargs else None
        self.file_size = kwargs.get('file_size')


class Voice(BaseObject):
    __slots__ = ['file_id', 'file_unique_id', 'duration', 'mime_type', 'file_size']

    def __init__(self, **kwargs):
        self.file_id = kwargs.get('file_id')
        self.file_unique_id = kwargs.get('file_unique_id')
        self.duration = kwargs.get('duration')
        self.mime_type = kwargs.get('mime_type')
        self.file_size = kwargs.get('file_size')


class WebhookInfo(BaseObject):
    __slots__ = ['url', 'has_custom_certificate', 'pending_update_count', 'ip_address', 'last_error_date',
                 'last_error_message', 'max_connections', 'allowed_updates']

    def __init__(self, **kwargs):
        self.url = kwargs.get('url')
        self.has_custom_certificate = kwargs.get('has_custom_certificate')
        self.pending_update_count = kwargs.get('pending_update_count')
        self.ip_address = kwargs.get('ip_address')
        self.last_error_date = kwargs.get('last_error_date')
        self.last_error_message = kwargs.get('last_error_message')
        self.max_connections = kwargs.get('max_connections')
        self.allowed_updates = kwargs.get('allowed_updates', list())


class Animation(BaseObject):
    __slots__ = ['file_id', 'file_unique_id', 'width', 'height', 'duration',
                 'thumb', 'file_name', 'mime_type', 'file_size']
    NESTED = ['thumb', ]

    def __init__(self, **kwargs):
        self.file_id = kwargs.get('file_id')
        self.file_unique_id = kwargs.get('file_unique_id')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.duration = kwargs.get('duration')
        self.thumb = PhotoSize(**kwargs['thumb']) if 'thumb' in kwargs else None
        self.file_name = kwargs.get('file_name')
        self.mime_type = kwargs.get('mime_type')
        self.file_size = kwargs.get('file_size')


class Audio(BaseObject):
    __slots__ = ['file_id', 'file_unique_id', 'duration', 'performer', 'title', 'file_name',
                 'mime_type', 'file_size', 'thumb']
    NESTED = ['thumb', ]

    def __init__(self, **kwargs):
        self.file_id = kwargs.get('file_id')
        self.file_unique_id = kwargs.get('file_unique_id')
        self.duration = kwargs.get('duration')
        self.performer = kwargs.get('performer')
        self.title = kwargs.get('title')
        self.file_name = kwargs.get('file_name')
        self.mime_type = kwargs.get('mime_type')
        self.file_size = kwargs.get('file_size')
        self.thumb = PhotoSize(**kwargs['thumb']) if 'thumb' in kwargs else None


class User(BaseObject):
    __slots__ = ['id', 'is_bot', 'first_name', 'last_name', 'username', 'language_code', 'can_join_groups',
                 'can_read_all_group_messages', 'supports_inline_queries']

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.is_bot = kwargs.get('is_bot')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.username = kwargs.get('username')
        self.language_code = kwargs.get('language_code')
        self.can_join_groups = kwargs.get('can_join_groups')
        self.can_read_all_group_messages = kwargs.get('can_read_all_group_messages')
        self.supports_inline_queries = kwargs.get('supports_inline_queries')


class ChatMember(BaseObject):
    __slots__ = ['user', 'status', 'custom_title', 'is_anonymous' 'until_date', 'can_be_edited', 'can_change_info',
                 'can_post_messages', 'can_edit_messages', 'can_delete_messages', 'can_invite_users',
                 'can_restrict_members', 'can_pin_messages', 'can_promote_members', 'is_member', 'can_send_messages',
                 'can_send_media_messages', 'can_send_polls', 'can_send_other_messages', 'can_add_web_page_previews']
    NESTED = ['user', ]

    def __init__(self, **kwargs):
        self.user = User(**kwargs['user']) if 'user' in kwargs else None
        self.status = kwargs.get('status')
        self.custom_title = kwargs.get('custom_title')
        self.is_anonymous = kwargs.get('is_anonymous')
        self.until_date = kwargs.get('until_date')
        self.can_be_edited = kwargs.get('can_be_edited')
        self.can_change_info = kwargs.get('can_change_info')
        self.can_post_messages = kwargs.get('can_post_messages')
        self.can_edit_messages = kwargs.get('can_edit_messages')
        self.can_delete_messages = kwargs.get('can_delete_messages')
        self.can_invite_users = kwargs.get('can_invite_users')
        self.can_restrict_members = kwargs.get('can_restrict_members')
        self.can_pin_messages = kwargs.get('can_pin_messages')
        self.can_promote_members = kwargs.get('can_promote_members')
        self.is_member = kwargs.get('is_member')
        self.can_send_messages = kwargs.get('can_send_messages')
        self.can_send_media_messages = kwargs.get('can_send_media_messages')
        self.can_send_polls = kwargs.get('can_send_polls')
        self.can_send_other_messages = kwargs.get('can_send_other_messages')
        self.can_add_web_page_previews = kwargs.get('can_add_web_page_previews')


class Document(BaseObject):
    __slots__ = ['file_id', 'file_unique_id', 'thumb', 'file_name', 'mime_type', 'file_size']
    NESTED = ['thumb', ]

    def __init__(self, **kwargs):
        self.file_id = kwargs.get('file_id')
        self.file_unique_id = kwargs.get('file_unique_id')
        self.thumb = PhotoSize(**kwargs['thumb']) if 'thumb' in kwargs else None
        self.file_name = kwargs.get('file_name')
        self.mime_type = kwargs.get('mime_type')
        self.file_size = kwargs.get('file_size')


class MessageEntity(BaseObject):
    __slots__ = ['type', 'offset', 'length', 'url', 'user', 'language']
    NESTED = ['user', ]

    def __init__(self, **kwargs):
        self.type = kwargs.get('type')
        self.offset = kwargs.get('offset')
        self.length = kwargs.get('length')
        self.url = kwargs.get('url')
        self.user = User(**kwargs['user']) if 'user' in kwargs else None
        self.language = kwargs.get('language')


class File(BaseObject):
    __slots__ = ['file_id', 'file_unique_id', 'file_size', 'file_path']

    def __init__(self, **kwargs):
        self.file_id = kwargs.get('file_id')
        self.file_unique_id = kwargs.get('file_unique_id')
        self.file_size = kwargs.get('file_size')
        self.file_path = kwargs.get('file_path')


class InputFile(BaseObject):
    __slots__ = ['file_id', 'url', 'path', 'caption', 'parse_mode']

    def __init__(self, **kwargs):
        self.file_id = kwargs.get('file_id')
        self.url = kwargs.get('url')
        self.path = kwargs.get('path')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')


class InputMedia(BaseObject):
    __slots__ = ['type', 'media', 'caption', 'parse_mode', 'caption_entities']
    NESTED = ['caption_entities']

    def __init__(self, **kwargs):
        self.type = kwargs.get('type')
        self.media = kwargs.get('media')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
        self.caption_entities = [MessageEntity(**v) for v in
                                 kwargs['caption_entities']] if 'caption_entities' in kwargs else list()


class InputMediaAnimation(InputMedia):
    __slots__ = ['type', 'media', 'caption', 'parse_mode', 'caption_entities', 'thumb', 'width', 'height', 'duration']
    NESTED = ['thumb', 'caption_entities']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'animation'
        self.thumb = InputFile(**kwargs['thumb']) if 'thumb' in kwargs else None
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.duration = kwargs.get('duration')


class InputMediaAudio(InputMedia):
    __slots__ = ['type', 'media', 'caption', 'parse_mode', 'caption_entities', 'thumb', 'duration', 'performer',
                 'title']
    NESTED = ['thumb', 'caption_entities']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'audio'
        self.thumb = InputFile(**kwargs['thumb']) if 'thumb' in kwargs else None
        self.duration = kwargs.get('duration')
        self.performer = kwargs.get('performer')
        self.title = kwargs.get('title')


class InputMediaDocument(InputMedia):
    __slots__ = ['type', 'media', 'caption', 'parse_mode', 'caption_entities', 'thumb',
                 'disable_content_type_detection']
    NESTED = ['thumb', 'caption_entities']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'document'
        self.thumb = InputFile(**kwargs['thumb']) if 'thumb' in kwargs else None
        self.disable_content_type_detection = kwargs.get('disable_content_type_detection')


class InputMediaPhoto(InputMedia):
    __slots__ = ['type', 'media', 'caption', 'parse_mode', 'caption_entities']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'photo'


class InputMediaVideo(InputMedia):
    __slots__ = ['type', 'media', 'caption', 'parse_mode', 'caption_entities', 'thumb', 'width', 'height', 'duration',
                 'supports_streaming']
    NESTED = ['thumb', 'caption_entities']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'video'
        self.thumb = InputFile(**kwargs['thumb']) if 'thumb' in kwargs else None
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.duration = kwargs.get('duration')
        self.supports_streaming = kwargs.get('supports_streaming')


class Game(BaseObject):
    __slots__ = ['title', 'description', 'photo', 'text', 'text_entities', 'animation']
    NESTED = ['photo', 'text_entities', 'animation']

    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.photo = [PhotoSize(**v) for v in kwargs['photo']] if 'photo' in kwargs else list()
        self.text = kwargs.get('text')
        self.text_entities = [MessageEntity(**v) for v in
                              kwargs['text_entities']] if 'text_entities' in kwargs else list()
        self.animation = Animation(**kwargs['animation']) if 'animation' in kwargs else None


class GameHighScore(BaseObject):
    __slots__ = ['position', 'user', 'score']
    NESTED = ['user', ]

    def __init__(self, **kwargs):
        self.position = kwargs.get('position')
        self.user = User(**kwargs['user']) if 'user' in kwargs else None
        self.score = kwargs.get('score')


class InputMessageContent(BaseObject):
    pass


class InputContactMessageContent(InputMessageContent):
    __slots__ = ['phone_number', 'first_name', 'last_name', 'vcard']

    def __init__(self, **kwargs):
        self.phone_number = kwargs.get('phone_number')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.vcard = kwargs.get('vcard')


class InputLocationMessageContent(InputMessageContent):
    __slots__ = ['latitude', 'longitude', 'live_period', 'horizontal_accuracy', 'heading', 'proximity_alert_radius']

    def __init__(self, **kwargs):
        self.latitude = kwargs.get('latitude')
        self.longitude = kwargs.get('longitude')
        self.horizontal_accuracy = kwargs.get('horizontal_accuracy')
        self.live_period = kwargs.get('live_period')
        self.heading = kwargs.get('heading')
        self.proximity_alert_radius = kwargs.get('proximity_alert_radius')


class InputTextMessageContent(InputMessageContent):
    __slots__ = ['message_text', 'parse_mode', 'disable_web_page_preview']

    def __init__(self, **kwargs):
        self.message_text = kwargs.get('message_text')
        self.parse_mode = kwargs.get('parse_mode')
        self.disable_web_page_preview = kwargs.get('disable_web_page_preview')


class InputVenueMessageContent(InputMessageContent):
    __slots__ = ['latitude', 'longitude', 'title', 'address', 'foursquare_id', 'foursquare_type',
                 'google_place_id', 'google_place_type']

    def __init__(self, **kwargs):
        self.latitude = kwargs.get('latitude')
        self.longitude = kwargs.get('longitude')
        self.title = kwargs.get('title')
        self.address = kwargs.get('address')
        self.foursquare_id = kwargs.get('foursquare_id')
        self.foursquare_type = kwargs.get('foursquare_type')
        self.google_place_id = kwargs.get('google_place_id')
        self.google_place_type = kwargs.get('google_place_type')


class ChosenInlineResult(BaseObject):
    __slots__ = ['result_id', 'from_', 'location', 'inline_message_id', 'query']
    NESTED = ['from_', 'location']

    def __init__(self, **kwargs):
        self.result_id = kwargs.get('result_id')
        self.from_ = User(**kwargs['from']) if 'from' in kwargs else None
        self.location = Location(**kwargs['location']) if 'location' in kwargs else None
        self.inline_message_id = kwargs.get('inline_message_id')
        self.query = kwargs.get('query')


class InlineQuery(BaseObject):
    __slots__ = ['id', 'from_', 'location', 'query', 'offset']
    NESTED = ['from_', 'location']

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.from_ = User(**kwargs.get('from')) if 'from' in kwargs else None
        self.location = Location(**kwargs['location']) if 'location' in kwargs else None
        self.query = kwargs.get('query')
        self.offset = kwargs.get('offset')


class InlineQueryResult(BaseObject):
    __slots__ = ['type', 'id', 'reply_markup', 'input_message_content']
    NESTED = ['reply_markup', 'input_message_content']

    def __init__(self, **kwargs):
        self.type = kwargs.get('type')
        self.id = kwargs.get('id')
        self.reply_markup = InlineKeyboardMarkup(**kwargs['reply_markup']) if 'reply_markup' in kwargs else None
        self.input_message_content = None
        imc = kwargs.get('input_message_content')
        if imc:
            if 'phone_number' in imc:
                self.input_message_content = InputContactMessageContent(**imc)
            elif 'latitude' in imc and 'address' in imc:
                self.input_message_content = InputVenueMessageContent(**imc)
            elif 'latitude' in imc:
                self.input_message_content = InputLocationMessageContent(**imc)
            elif 'message_text' in imc:
                self.input_message_content = InputTextMessageContent(**imc)


class InlineQueryResultArticle(InlineQueryResult):
    __slots__ = ['type', 'id', 'reply_markup', 'input_message_content', 'title', 'url', 'hide_url', 'description',
                 'thumb_url', 'thumb_width', 'thumb_height']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'article'
        self.title = kwargs.get('title')
        self.url = kwargs.get('url')
        self.hide_url = kwargs.get('hide_url')
        self.description = kwargs.get('description')
        self.thumb_url = kwargs.get('thumb_url')
        self.thumb_width = kwargs.get('thumb_width')
        self.thumb_height = kwargs.get('thumb_height')


class InlineQueryResultAudio(InlineQueryResult):
    __slots__ = ['type', 'id', 'reply_markup', 'input_message_content', 'audio_url', 'parse_mode', 'title',
                 'caption', 'performer', 'audio_duration', 'caption_entities']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'audio'
        self.audio_url = kwargs.get('audio_url')
        self.parse_mode = kwargs.get('parse_mode')
        self.title = kwargs.get('title')
        self.caption = kwargs.get('caption')
        self.performer = kwargs.get('performer')
        self.audio_duration = kwargs.get('audio_duration')
        self.caption_entities = [MessageEntity(**v) for v in
                                 kwargs['caption_entities']] if 'caption_entities' in kwargs else list()


class InlineQueryResultCachedAudio(InlineQueryResult):
    __slots__ = ['type', 'id', 'reply_markup', 'input_message_content',
                 'audio_file_id', 'caption', 'parse_mode', 'caption_entities']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'audio'
        self.audio_file_id = kwargs.get('audio_file_id')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
        self.caption_entities = [MessageEntity(**v) for v in
                                 kwargs['caption_entities']] if 'caption_entities' in kwargs else list()


class InlineQueryResultCachedDocument(InlineQueryResult):
    __slots__ = ['type', 'id', 'reply_markup', 'input_message_content', 'caption_entities',
                 'title', 'document_file_id', 'description', 'caption', 'parse_mode']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'document'
        self.title = kwargs.get('title')
        self.document_file_id = kwargs.get('document_file_id')
        self.description = kwargs.get('description')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
        self.caption_entities = [MessageEntity(**v) for v in
                                 kwargs['caption_entities']] if 'caption_entities' in kwargs else list()


class InlineQueryResultCachedGif(InlineQueryResult):
    __slots__ = ['type', 'id', 'reply_markup', 'input_message_content', 'gif_file_id', 'title', 'caption', 'parse_mode',
                 'caption_entities']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'gif'
        self.gif_file_id = kwargs.get('gif_file_id')
        self.title = kwargs.get('title')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
        self.caption_entities = [MessageEntity(**v) for v in
                                 kwargs['caption_entities']] if 'caption_entities' in kwargs else list()


class InlineQueryResultCachedMpeg4Gif(InlineQueryResult):
    __slots__ = ['type', 'id', 'reply_markup', 'input_message_content',
                 'mpeg4_file_id', 'title', 'caption', 'parse_mode', 'caption_entities']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'mpeg4_gif'
        self.mpeg4_file_id = kwargs.get('mpeg4_file_id')
        self.title = kwargs.get('title')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
        self.caption_entities = [MessageEntity(**v) for v in
                                 kwargs['caption_entities']] if 'caption_entities' in kwargs else list()


class InlineQueryResultCachedPhoto(InlineQueryResult):
    __slots__ = ['type', 'id', 'reply_markup', 'input_message_content', 'caption_entities',
                 'photo_file_id', 'title', 'description', 'caption', 'parse_mode']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'photo'
        self.photo_file_id = kwargs.get('photo_file_id')
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
        self.caption_entities = [MessageEntity(**v) for v in
                                 kwargs['caption_entities']] if 'caption_entities' in kwargs else list()


class InlineQueryResultCachedSticker(InlineQueryResult):
    __slots__ = ['type', 'id', 'reply_markup', 'input_message_content', 'sticker_file_id']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'sticker'
        self.sticker_file_id = kwargs.get('sticker_file_id')


class InlineQueryResultCachedVideo(InlineQueryResult):
    __slots__ = ['type', 'id', 'reply_markup', 'input_message_content', 'video_file_id', 'title', 'description',
                 'caption', 'parse_mode', 'caption_entities']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'video'
        self.video_file_id = kwargs.get('video_file_id')
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
        self.caption_entities = [MessageEntity(**v) for v in
                                 kwargs['caption_entities']] if 'caption_entities' in kwargs else list()


class InlineQueryResultCachedVoice(InlineQueryResult):
    __slots__ = ['type', 'id', 'reply_markup', 'input_message_content', 'voice_file_id',
                 'title', 'caption', 'parse_mode', 'caption_entities']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'voice'
        self.voice_file_id = kwargs.get('voice_file_id')
        self.title = kwargs.get('title')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
        self.caption_entities = [MessageEntity(**v) for v in
                                 kwargs['caption_entities']] if 'caption_entities' in kwargs else list()


class InlineQueryResultContact(InlineQueryResult):
    __slots__ = ['type', 'id', 'reply_markup', 'input_message_content', 'phone_number', 'first_name',
                 'last_name', 'vcard', 'thumb_url', 'thumb_width', 'thumb_height']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'contact'
        self.phone_number = kwargs.get('phone_number')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.vcard = kwargs.get('vcard')
        self.thumb_url = kwargs.get('thumb_url')
        self.thumb_width = kwargs.get('thumb_width')
        self.thumb_height = kwargs.get('thumb_height')


class InlineQueryResultDocument(InlineQueryResult):
    __slots__ = ['type', 'id', 'reply_markup', 'input_message_content', 'title', 'caption', 'parse_mode',
                 'document_url', 'mime_type', 'description', 'thumb_url', 'thumb_width', 'thumb_height',
                 'caption_entities']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'document'
        self.title = kwargs.get('title')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
        self.document_url = kwargs.get('document_url')
        self.mime_type = kwargs.get('mime_type')
        self.description = kwargs.get('description')
        self.thumb_url = kwargs.get('thumb_url')
        self.thumb_width = kwargs.get('thumb_width')
        self.thumb_height = kwargs.get('thumb_height')
        self.caption_entities = [MessageEntity(**v) for v in
                                 kwargs['caption_entities']] if 'caption_entities' in kwargs else list()


class InlineQueryResultGame(InlineQueryResult):
    __slots__ = ['type', 'id', 'reply_markup', 'input_message_content', 'game_short_name']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'game'
        self.game_short_name = kwargs.get('game_short_name')
        del self.input_message_content


class InlineQueryResultGif(InlineQueryResult):
    __slots__ = ['type', 'id', 'reply_markup', 'input_message_content', 'gif_url', 'gif_width', 'gif_height',
                 'gif_duration', 'thumb_url', 'thumb_mime_type', 'title', 'caption', 'parse_mode', 'caption_entities']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'gif'
        self.gif_url = kwargs.get('gif_url')
        self.gif_width = kwargs.get('gif_width')
        self.gif_height = kwargs.get('gif_height')
        self.gif_duration = kwargs.get('gif_duration')
        self.thumb_url = kwargs.get('thumb_url')
        self.thumb_mime_type = kwargs.get('thumb_mime_type')
        self.title = kwargs.get('title')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
        self.caption_entities = [MessageEntity(**v) for v in
                                 kwargs['caption_entities']] if 'caption_entities' in kwargs else list()


class InlineQueryResultLocation(InlineQueryResult):
    __slots__ = ['type', 'id', 'reply_markup', 'input_message_content', 'latitude', 'longitude', 'title',
                 'live_period', 'thumb_url', 'thumb_width', 'thumb_height', 'horizontal_accuracy', 'heading',
                 'proximity_alert_radius']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'location'
        self.latitude = kwargs.get('latitude')
        self.longitude = kwargs.get('longitude')
        self.title = kwargs.get('title')
        self.horizontal_accuracy = kwargs.get('horizontal_accuracy')
        self.live_period = kwargs.get('live_period')
        self.heading = kwargs.get('heading')
        self.proximity_alert_radius = kwargs.get('proximity_alert_radius')
        self.thumb_url = kwargs.get('thumb_url')
        self.thumb_width = kwargs.get('thumb_width')
        self.thumb_height = kwargs.get('thumb_height')


class InlineQueryResultMpeg4Gif(InlineQueryResult):
    __slots__ = ['type', 'id', 'reply_markup', 'input_message_content', 'mpeg4_url', 'mpeg4_width', 'mpeg4_height',
                 'mpeg4_duration', 'thumb_url', 'thumb_mime_type', 'title', 'caption', 'parse_mode', 'caption_entities']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'mpeg4_gif'
        self.mpeg4_url = kwargs.get('mpeg4_url')
        self.mpeg4_width = kwargs.get('mpeg4_width')
        self.mpeg4_height = kwargs.get('mpeg4_height')
        self.mpeg4_duration = kwargs.get('mpeg4_duration')
        self.thumb_url = kwargs.get('thumb_url')
        self.thumb_mime_type = kwargs.get('thumb_mime_type')
        self.title = kwargs.get('title')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
        self.caption_entities = [MessageEntity(**v) for v in
                                 kwargs['caption_entities']] if 'caption_entities' in kwargs else list()


class InlineQueryResultPhoto(InlineQueryResult):
    __slots__ = ['type', 'id', 'reply_markup', 'input_message_content', 'photo_url', 'thumb_url',
                 'photo_width', 'photo_height', 'title', 'description', 'caption', 'parse_mode', 'caption_entities']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'photo'
        self.photo_url = kwargs.get('photo_url')
        self.thumb_url = kwargs.get('thumb_url')
        self.photo_width = kwargs.get('thumb_width')
        self.photo_height = kwargs.get('thumb_height')
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
        self.caption_entities = [MessageEntity(**v) for v in
                                 kwargs['caption_entities']] if 'caption_entities' in kwargs else list()


class InlineQueryResultVenue(InlineQueryResult):
    __slots__ = ['type', 'id', 'reply_markup', 'input_message_content', 'latitude', 'longitude', 'title',
                 'address', 'foursquare_id', 'foursquare_type', 'thumb_url', 'thumb_width', 'thumb_height',
                 'google_place_id', 'google_place_type']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'venue'
        self.latitude = kwargs.get('latitude')
        self.longitude = kwargs.get('longitude')
        self.title = kwargs.get('title')
        self.address = kwargs.get('address')
        self.foursquare_id = kwargs.get('foursquare_id')
        self.foursquare_type = kwargs.get('foursquare_type')
        self.google_place_id = kwargs.get('google_place_id')
        self.google_place_type = kwargs.get('google_place_type')
        self.thumb_url = kwargs.get('thumb_url')
        self.thumb_width = kwargs.get('thumb_width')
        self.thumb_height = kwargs.get('thumb_height')


class InlineQueryResultVideo(InlineQueryResult):
    __slots__ = ['type', 'id', 'reply_markup', 'input_message_content', 'video_url', 'mime_type', 'thumb_url',
                 'title', 'caption', 'parse_mode', 'video_width', 'video_height', 'video_duration', 'description',
                 'caption_entities']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'video'
        self.video_url = kwargs.get('video_url')
        self.mime_type = kwargs.get('mime_type')
        self.thumb_url = kwargs.get('thumb_url')
        self.title = kwargs.get('title')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
        self.video_width = kwargs.get('video_width')
        self.video_height = kwargs.get('video_height')
        self.video_duration = kwargs.get('video_duration')
        self.description = kwargs.get('description')
        self.caption_entities = [MessageEntity(**v) for v in
                                 kwargs['caption_entities']] if 'caption_entities' in kwargs else list()


class InlineQueryResultVoice(InlineQueryResult):
    __slots__ = ['type', 'id', 'reply_markup', 'input_message_content', 'voice_url', 'title', 'caption',
                 'parse_mode', 'voice_duration', 'caption_entities']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'voice'
        self.voice_url = kwargs.get('voice_url')
        self.title = kwargs.get('title')
        self.caption = kwargs.get('caption')
        self.parse_mode = kwargs.get('parse_mode')
        self.voice_duration = kwargs.get('voice_duration')
        self.caption_entities = [MessageEntity(**v) for v in
                                 kwargs['caption_entities']] if 'caption_entities' in kwargs else list()


class BaseElementError(BaseObject):
    __slots__ = ['source', 'type', 'message']

    def __init__(self, **kwargs):
        self.source = kwargs.get('source')
        self.type = kwargs.get('type')
        self.message = kwargs.get('message')


class PassportElementErrorDataField(BaseElementError):
    __slots__ = ['source', 'type', 'message', 'field_name', 'data_hash']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.field_name = kwargs.get('field_name')
        self.data_hash = kwargs.get('data_hash')


class PassportElementErrorFile(BaseElementError):
    __slots__ = ['source', 'type', 'message', 'file_hash']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_hash = kwargs.get('file_hash')


class PassportElementErrorFiles(BaseElementError):
    __slots__ = ['source', 'type', 'message', 'file_hashes']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_hashes = kwargs.get('file_hashes')


class PassportElementErrorFrontSide(BaseElementError):
    __slots__ = ['source', 'type', 'message', 'file_hash']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_hash = kwargs.get('file_hash')


class PassportElementErrorReverseSide(BaseElementError):
    __slots__ = ['source', 'type', 'message', 'file_hash']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_hash = kwargs.get('file_hash')


class PassportElementErrorSelfie(BaseElementError):
    __slots__ = ['source', 'type', 'message', 'file_hash']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_hash = kwargs.get('file_hash')


class PassportElementErrorTranslationFile(BaseElementError):
    __slots__ = ['source', 'type', 'message', 'file_hash']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_hash = kwargs.get('file_hash')


class PassportElementErrorTranslationFiles(BaseElementError):
    __slots__ = ['source', 'type', 'message', 'file_hashes']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_hashes = kwargs.get('file_hashes')


class PassportElementErrorUnspecified(BaseElementError):
    __slots__ = ['source', 'type', 'message', 'element_hash']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.element_hash = kwargs.get('element_hash')


class EncryptedCredentials(BaseObject):
    __slots__ = ['data', 'hash', 'secret']

    def __init__(self, **kwargs):
        self.data = kwargs.get('data')
        self.hash = kwargs.get('hash')
        self.secret = kwargs.get('secret')


class PassportFile(BaseObject):
    __slots__ = ['file_id', 'file_unique_id', 'file_size', 'file_date']

    def __init__(self, **kwargs):
        self.file_id = kwargs.get('file_id')
        self.file_unique_id = kwargs.get('file_unique_id')
        self.file_size = kwargs.get('file_size')
        self.file_date = kwargs.get('file_date')


class EncryptedPassportElement(BaseObject):
    __slots__ = ['type', 'data', 'phone_number', 'email', 'files', 'front_side',
                 'reverse_side', 'selfie', 'translation', 'hash']
    NESTED = ['files', 'front_side', 'reverse_side', 'selfie', 'translation']

    def __init__(self, **kwargs):
        self.type = kwargs.get('type')
        self.data = kwargs.get('data')
        self.phone_number = kwargs.get('phone_number')
        self.email = kwargs.get('email')
        self.files = [PassportFile(**v) for v in kwargs['files']] if 'files' in kwargs else list()
        self.front_side = PassportFile(**kwargs['front_side']) if 'front_side' in kwargs else None
        self.reverse_side = PassportFile(**kwargs['reverse_side']) if 'reverse_side' in kwargs else None
        self.selfie = PassportFile(**kwargs['selfie']) if 'selfie' in kwargs else None
        self.translation = [PassportFile(**v) for v in kwargs['translation']] if 'translation' in kwargs else list()
        self.hash = kwargs.get('hash')


class PassportData(BaseObject):
    __slots__ = ['data', 'credentials']
    NESTED = ['data', 'credentials']

    def __init__(self, **kwargs):
        self.data = [EncryptedPassportElement(**v) for v in kwargs['data']] if 'data' in kwargs else list()
        self.credentials = EncryptedCredentials(**kwargs['credentials']) if 'credentials' in kwargs else None


class Invoice(BaseObject):
    __slots__ = ['title', 'description', 'start_parameter', 'currency', 'total_amount']

    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.start_parameter = kwargs.get('start_parameter')
        self.currency = kwargs.get('currency')
        self.total_amount = kwargs.get('total_amount')


class LabeledPrice(BaseObject):
    __slots__ = ['label', 'amount']

    def __init__(self, **kwargs):
        self.label = kwargs.get('label')
        self.amount = kwargs.get('amount')


class ShippingAddress(BaseObject):
    __slots__ = ['country_code', 'state', 'city', 'street_line1', 'street_line2', 'post_code']

    def __init__(self, **kwargs):
        self.country_code = kwargs.get('country_code')
        self.state = kwargs.get('state')
        self.city = kwargs.get('city')
        self.street_line1 = kwargs.get('street_line1')
        self.street_line2 = kwargs.get('street_line2')
        self.post_code = kwargs.get('post_code')


class OrderInfo(BaseObject):
    __slots__ = ['name', 'phone_number', 'email', 'shipping_address']
    NESTED = ['shipping_address', ]

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.phone_number = kwargs.get('phone_number')
        self.email = kwargs.get('email')
        self.shipping_address = ShippingAddress(**kwargs['shipping_address']) if 'shipping_address' in kwargs else None


class PreCheckoutQuery(BaseObject):
    __slots__ = ['id', 'from_', 'currency', 'total_amount', 'invoice_payload', 'shipping_option_id', 'order_info']
    NESTED = ['from_', 'order_info']

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.from_ = User(**kwargs['from']) if 'from' in kwargs else None
        self.currency = kwargs.get('currency')
        self.total_amount = kwargs.get('total_amount')
        self.invoice_payload = kwargs.get('invoice_payload')
        self.shipping_option_id = kwargs.get('shipping_option_id')
        self.order_info = OrderInfo(**kwargs['order_info']) if 'order_info' in kwargs else None


class ShippingOption(BaseObject):
    __slots__ = ['id', 'title', 'prices']
    NESTED = ['prices', ]

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.title = kwargs.get('title')
        self.prices = [LabeledPrice(**v) for v in kwargs['prices']] if 'prices' in kwargs else None


class ShippingQuery(BaseObject):
    __slots__ = ['id', 'from_', 'invoice_payload', 'shipping_address']
    NESTED = ['from_', 'shipping_address']

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.from_ = User(**kwargs['from']) if 'from' in kwargs else None
        self.invoice_payload = kwargs.get('invoice_payload')
        self.shipping_address = ShippingAddress(**kwargs['shipping_address']) if 'shipping_address' in kwargs else None


class SuccessfulPayment(BaseObject):
    __slots__ = ['currency', 'total_amount', 'invoice_payload', 'shipping_option_id',
                 'order_info', 'telegram_payment_charge_id', 'provider_payment_charge_id']
    NESTED = ['order_info', ]

    def __init__(self, **kwargs):
        self.currency = kwargs.get('currency')
        self.total_amount = kwargs.get('total_amount')
        self.invoice_payload = kwargs.get('invoice_payload')
        self.shipping_option_id = kwargs.get('shipping_option_id')
        self.order_info = OrderInfo(**kwargs['order_info']) if 'order_info' in kwargs else None
        self.telegram_payment_charge_id = kwargs.get('telegram_payment_charge_id')
        self.provider_payment_charge_id = kwargs.get('provider_payment_charge_id')


class MaskPosition(BaseObject):
    __slots__ = ['point', 'x_shift', 'y_shift', 'scale']

    def __init__(self, **kwargs):
        self.point = kwargs.get('point')
        self.x_shift = kwargs.get('x_shift')
        self.y_shift = kwargs.get('y_shift')
        self.scale = kwargs.get('scale')


class Sticker(BaseObject):
    __slots__ = ['file_id', 'file_unique_id', 'width', 'height', 'is_animated', 'thumb', 'emoji',
                 'set_name', 'mask_position', 'file_size']
    NESTED = ['thumb', 'mask_position']

    def __init__(self, **kwargs):
        self.file_id = kwargs.get('file_id')
        self.file_unique_id = kwargs.get('file_unique_id')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.is_animated = kwargs.get('is_animated')
        self.thumb = PhotoSize(**kwargs['thumb']) if 'thumb' in kwargs else None
        self.emoji = kwargs.get('emoji')
        self.set_name = kwargs.get('set_name')
        self.mask_position = MaskPosition(**kwargs['mask_position']) if 'mask_position' in kwargs else None
        self.file_size = kwargs.get('file_size')


class StickerSet(BaseObject):
    __slots__ = ['name', 'title', 'is_animated', 'contains_masks', 'stickers', 'thumb']
    NESTED = ['stickers', 'thumb']

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.title = kwargs.get('title')
        self.is_animated = kwargs.get('is_animated')
        self.contains_masks = kwargs.get('contains_masks')
        self.stickers = [Sticker(**v) for v in kwargs['stickers']] if 'stickers' in kwargs else list()
        self.thumb = PhotoSize(**kwargs['thumb']) if 'thumb' in kwargs else None


class ChatPermissions(BaseObject):
    __slots__ = ['can_send_messages', 'can_send_media_messages', 'can_send_polls',
                 'can_send_other_messages', 'can_add_web_page_previews', 'can_change_info',
                 'can_invite_users', 'can_pin_messages']

    def __init__(self, **kwargs):
        self.can_send_messages = kwargs.get('can_send_messages')
        self.can_send_media_messages = kwargs.get('can_send_media_messages')
        self.can_send_polls = kwargs.get('can_send_polls')
        self.can_send_other_messages = kwargs.get('can_send_other_messages')
        self.can_add_web_page_previews = kwargs.get('can_add_web_page_previews')
        self.can_change_info = kwargs.get('can_change_info')
        self.can_invite_users = kwargs.get('can_invite_users')
        self.can_pin_messages = kwargs.get('can_pin_messages')


class BotCommand(BaseObject):
    __slots__ = ['command', 'description']

    def __init__(self, **kwargs):
        self.command = kwargs.get('command')
        self.description = kwargs.get('description')


class Chat(BaseObject):
    __slots__ = ['id', 'type', 'title', 'username', 'first_name', 'last_name', 'photo', 'description', 'invite_link',
                 'pinned_message', 'permissions', 'slow_mode_delay', 'sticker_set_name', 'can_set_sticker_set',
                 'location']
    NESTED = ['photo', 'pinned_message', 'permissions', 'location']

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.type = kwargs.get('type')
        self.title = kwargs.get('title')
        self.username = kwargs.get('username')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.photo = ChatPhoto(**kwargs['photo']) if 'photo' in kwargs else None
        self.description = kwargs.get('description')
        self.invite_link = kwargs.get('invite_link')
        self.pinned_message = Message(**kwargs['pinned_message']) if 'pinned_message' in kwargs else None
        self.permissions = ChatPermissions(**kwargs['permissions']) if 'permissions' in kwargs else None
        self.slow_mode_delay = kwargs.get('slow_mode_delay')
        self.sticker_set_name = kwargs.get('sticker_set_name')
        self.can_set_sticker_set = kwargs.get('can_set_sticker_set')
        self.location = ChatLocation(**kwargs['location']) if 'location' in kwargs else None


class Message(BaseObject):
    __slots__ = ['message_id', 'from_', 'sender_chat', 'date', 'chat', 'forward_from_chat', 'forward_from',
                 'forward_signature', 'forward_sender_name', 'forward_date', 'reply_to_message', 'via_bot',
                 'edit_date', 'media_group_id', 'author_signature', 'text', 'entities', 'caption_entities',
                 'audio', 'document', 'animation', 'game', 'photo', 'sticker', 'video', 'voice', 'video_note',
                 'caption', 'contact', 'location', 'venue', 'poll', 'dice', 'new_chat_members', 'left_chat_member',
                 'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created',
                 'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id',
                 'pinned_message', 'invoice', 'successful_payment', 'connected_website', 'passport_data',
                 'proximity_alert_triggered', 'reply_markup']
    NESTED = ['from_', 'sender_chat', 'chat', 'forward_from_chat', 'forward_from', 'reply_to_message', 'via_bot',
              'entities', 'caption_entities', 'audio', 'document', 'animation', 'game', 'photo', 'sticker', 'video',
              'voice', 'video_note', 'contact', 'location', 'venue', 'poll', 'dice', 'new_chat_members',
              'left_chat_member', 'new_chat_photo', 'pinned_message', 'invoice', 'successful_payment', 'passport_data',
              'proximity_alert_triggered', 'reply_markup']

    def __init__(self, **kwargs):
        self.message_id = kwargs.get('message_id')
        self.from_ = User(**kwargs['from']) if 'from' in kwargs else None
        self.sender_chat = Chat(**kwargs['sender_chat']) if 'sender_chat' in kwargs else None
        self.date = kwargs.get('date')
        self.chat = Chat(**kwargs['chat']) if 'chat' in kwargs else None
        self.forward_from_chat = Chat(**kwargs['forward_from_chat']) if 'forward_from_chat' in kwargs else None
        self.forward_from = User(**kwargs['forward_from']) if 'forward_from' in kwargs else None
        self.forward_signature = kwargs.get('forward_signature')
        self.forward_sender_name = kwargs.get('forward_sender_name')
        self.forward_date = kwargs.get('forward_date')
        self.reply_to_message = Message(**kwargs['reply_to_message']) if 'reply_to_message' in kwargs else None
        self.via_bot = User(**kwargs['via_bot']) if 'via_bot' in kwargs else None
        self.edit_date = kwargs.get('edit_date')
        self.media_group_id = kwargs.get('media_group_id')
        self.author_signature = kwargs.get('author_signature')
        self.text = kwargs.get('text')
        self.entities = [MessageEntity(**v) for v in kwargs['entities']] if 'entities' in kwargs else list()
        self.caption_entities = [MessageEntity(**v) for v in
                                 kwargs['caption_entities']] if 'caption_entities' in kwargs else list()
        self.audio = Audio(**kwargs['audio']) if 'audio' in kwargs else None
        self.document = Document(**kwargs['document']) if 'document' in kwargs else None
        self.animation = Animation(**kwargs['animation']) if 'animation' in kwargs else None
        self.game = Game(**kwargs['game']) if 'game' in kwargs else None
        self.photo = [PhotoSize(**v) for v in kwargs['photo']] if 'photo' in kwargs else list()
        self.sticker = Sticker(**kwargs['sticker']) if 'sticker' in kwargs else None
        self.video = Video(**kwargs['video']) if 'video' in kwargs else None
        self.voice = Voice(**kwargs['voice']) if 'voice' in kwargs else None
        self.video_note = VideoNote(**kwargs['video_note']) if 'video_note' in kwargs else None
        self.caption = kwargs.get('caption')
        self.contact = Contact(**kwargs['contact']) if 'contact' in kwargs else None
        self.location = Location(**kwargs['location']) if 'location' in kwargs else None
        self.venue = Venue(**kwargs['venue']) if 'venue' in kwargs else None
        self.poll = Poll(**kwargs['poll']) if 'poll' in kwargs else None
        self.dice = Dice(**kwargs['dice']) if 'dice' in kwargs else None
        self.new_chat_members = [User(**v) for v in
                                 kwargs['new_chat_members']] if 'new_chat_members' in kwargs else list()
        self.left_chat_member = User(**kwargs['left_chat_member']) if 'left_chat_member' in kwargs else None
        self.new_chat_title = kwargs.get('new_chat_title')
        self.new_chat_photo = [PhotoSize(**v) for v in
                               kwargs['new_chat_photo']] if 'new_chat_photo' in kwargs else list()
        self.delete_chat_photo = kwargs.get('delete_chat_photo')
        self.group_chat_created = kwargs.get('group_chat_created')
        self.supergroup_chat_created = kwargs.get('supergroup_chat_created')
        self.channel_chat_created = kwargs.get('channel_chat_created')
        self.migrate_to_chat_id = kwargs.get('migrate_to_chat_id')
        self.migrate_from_chat_id = kwargs.get('migrate_from_chat_id')
        self.pinned_message = Message(**kwargs['pinned_message']) if 'pinned_message' in kwargs else None
        self.invoice = Invoice(**kwargs['invoice']) if 'invoice' in kwargs else None
        self.successful_payment = SuccessfulPayment(
            **kwargs['successful_payment']) if 'successful_payment' in kwargs else None
        self.connected_website = kwargs.get('connected_website')
        self.passport_data = PassportData(**kwargs['passport_data']) if 'passport_data' in kwargs else None
        self.proximity_alert_triggered = ProximityAlertTriggered(
            **kwargs['proximity_alert_triggered']) if 'proximity_alert_triggered' in kwargs else None
        self.reply_markup = InlineKeyboardMarkup(**kwargs['reply_markup']) if 'reply_markup' in kwargs else None


class CallbackQuery(BaseObject):
    __slots__ = ['id', 'from_', 'message', 'inline_message_id', 'chat_instance', 'data', 'game_short_name']
    NESTED = ['from_', 'message']

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.from_ = User(**kwargs['from']) if 'from' in kwargs else None
        self.message = Message(**kwargs['message']) if 'message' in kwargs else None
        self.inline_message_id = kwargs.get('inline_message_id')
        self.chat_instance = kwargs.get('chat_instance')
        self.data = kwargs.get('data')
        self.game_short_name = kwargs.get('game_short_name')


class Update(BaseObject):
    __slots__ = ['update_id', 'message', 'edited_message', 'channel_post', 'edited_channel_post', 'inline_query',
                 'chosen_inline_result', 'callback_query', 'shipping_query', 'pre_checkout_query', 'poll',
                 'poll_answer']
    NESTED = ['message', 'edited_message', 'channel_post', 'edited_channel_post', 'inline_query',
              'chosen_inline_result', 'callback_query', 'shipping_query', 'pre_checkout_query', 'poll', 'poll_answer']

    def __init__(self, **kwargs):
        self.update_id = kwargs.get('update_id')
        self.message = Message(**kwargs['message']) if 'message' in kwargs else None
        self.edited_message = Message(**kwargs['edited_message']) if 'edited_message' in kwargs else None
        self.channel_post = Message(**kwargs['channel_post']) if 'channel_post' in kwargs else None
        self.edited_channel_post = Message(
            **kwargs['edited_channel_post']) if 'edited_channel_post' in kwargs else None
        self.inline_query = InlineQuery(**kwargs['inline_query']) if 'inline_query' in kwargs else None
        self.chosen_inline_result = ChosenInlineResult(
            **kwargs['chosen_inline_result']) if 'chosen_inline_result' in kwargs else None
        self.callback_query = CallbackQuery(**kwargs['callback_query']) if 'callback_query' in kwargs else None
        self.shipping_query = ShippingQuery(**kwargs['shipping_query']) if 'shipping_query' in kwargs else None
        self.pre_checkout_query = PreCheckoutQuery(
            **kwargs['pre_checkout_query']) if 'pre_checkout_query' in kwargs else None
        self.poll = Poll(**kwargs['poll']) if 'poll' in kwargs else None
        self.poll_answer = PollAnswer(**kwargs['poll_answer']) if 'poll_answer' in kwargs else None
