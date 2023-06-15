from __future__ import annotations

import copy
import pathlib
from dataclasses import dataclass, is_dataclass, fields
from typing import (
    Optional,
    Union,
    List,
    Any,
    Callable,
    Awaitable,
    get_type_hints,
    get_origin,
    get_args
)

from botup.constants import (
    chat_member_status,
    bot_command_scope_type,
    menu_button_type,
    input_media_type,
    input_file_type,
    inline_query_result_type,
    passport_element_error_source
)
from botup.constants.bot_command_scope_type import BotCommandScopeType
from botup.constants.chat_member_status import ChatMemberStatus
from botup.constants.chat_type import ChatType
from botup.constants.encrypted_passport_element_type import EncryptedPassportElementType
from botup.constants.inline_query_chat_type import InlineQueryChatType
from botup.constants.inline_query_result_type import InlineQueryResultType
from botup.constants.input_file_type import InputFileType
from botup.constants.input_media_type import InputMediaType
from botup.constants.mask_position_point import MaskPositionPoint
from botup.constants.menu_button_type import MenuButtonType
from botup.constants.message_entity_type import MessageEntityType
from botup.constants.passport_element_error_source import PassportElementErrorSource
from botup.constants.poll_type import PollType
from botup.constants.sticker_type import StickerType
from botup.constants.update_type import UpdateType

NoneType = type(None)
_rename_key_mapping = {
    'from_': 'from'
}


def asdict(obj, *, dict_factory=dict):
    if not _is_dataclass_instance(obj):
        raise TypeError("asdict() should be called on dataclass instances")
    return _asdict_inner(obj, dict_factory)


def _is_dataclass_instance(obj):
    return hasattr(type(obj), '__dataclass_fields__')


def _asdict_inner(obj, dict_factory):
    if _is_dataclass_instance(obj):
        result = []
        for f in fields(obj):
            value = _asdict_inner(getattr(obj, f.name), dict_factory)
            if value is None:
                continue
            result.append((f.name, value))
        return dict_factory(result)
    elif isinstance(obj, tuple) and hasattr(obj, '_fields'):
        return type(obj)(*[_asdict_inner(v, dict_factory) for v in obj])
    elif isinstance(obj, (list, tuple)):
        return type(obj)(_asdict_inner(v, dict_factory) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)((_asdict_inner(k, dict_factory),
                          _asdict_inner(v, dict_factory))
                         for k, v in obj.items())
    else:
        return copy.deepcopy(obj)


def _from_dict_inner(data: Any, class_: Any) -> Any:
    if is_dataclass(class_):
        assert isinstance(data, dict)
        return class_.from_dict(data)

    origin = get_origin(class_)
    args = get_args(class_)

    if origin is Union:
        return _from_dict_inner(data, args[0])

    if origin is list:
        assert isinstance(data, list)
        inner_type = get_args(class_)[0]
        return [_from_dict_inner(v, inner_type) for v in data]

    return data


@dataclass
class BaseObject:

    @classmethod
    def from_dict(cls, data: dict):
        kwargs = {}
        hints = get_type_hints(cls)

        for hint_key, hint_value in hints.items():
            value = data.get(_rename_key_mapping.get(hint_key) or hint_key)
            is_none_value = value is None
            is_optional = NoneType in get_args(hint_value)

            if is_none_value and is_optional:
                continue

            if not is_optional and is_none_value:
                raise Exception(f'{hint_key} is required')

            kwargs[hint_key] = _from_dict_inner(
                data=value,
                class_=hint_value
            )

        return cls(**kwargs)

    def as_dict(self):
        return asdict(self)


@dataclass
class Update(BaseObject):
    update_id: int
    message: Optional[Message] = None
    edited_message: Optional[Message] = None
    channel_post: Optional[Message] = None
    edited_channel_post: Optional[Message] = None
    inline_query: Optional[InlineQuery] = None
    chosen_inline_result: Optional[ChosenInlineResult] = None
    callback_query: Optional[CallbackQuery] = None
    shipping_query: Optional[ShippingQuery] = None
    pre_checkout_query: Optional[PreCheckoutQuery] = None
    poll: Optional[Poll] = None
    poll_answer: Optional[PollAnswer] = None
    my_chat_member: Optional[ChatMemberUpdated] = None
    chat_member: Optional[ChatMemberUpdated] = None
    chat_join_request: Optional[ChatJoinRequest] = None


@dataclass
class WebhookInfo(BaseObject):
    url: str
    has_custom_certificate: bool
    pending_update_count: int
    ip_address: Optional[str] = None
    last_error_date: Optional[int] = None
    last_error_message: Optional[str] = None
    last_synchronization_error_date: Optional[int] = None
    max_connections: Optional[int] = None
    allowed_updates: Optional[List[str]] = None


@dataclass
class User(BaseObject):
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    added_to_attachment_menu: Optional[bool] = None
    can_join_groups: Optional[bool] = None
    can_read_all_group_messages: Optional[bool] = None
    supports_inline_queries: Optional[bool] = None


@dataclass
class Chat(BaseObject):
    id: int
    type: ChatType
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_forum: Optional[bool] = None
    photo: Optional[ChatPhoto] = None
    active_usernames: Optional[List[str]] = None
    emoji_status_custom_emoji_id: Optional[str] = None
    bio: Optional[str] = None
    has_private_forwards: Optional[bool] = None
    has_restricted_voice_and_video_messages: Optional[bool] = None
    join_to_send_messages: Optional[bool] = None
    join_by_request: Optional[bool] = None
    description: Optional[str] = None
    invite_link: Optional[str] = None
    pinned_message: Optional[Message] = None
    permissions: Optional[ChatPermissions] = None
    slow_mode_delay: Optional[int] = None
    message_auto_delete_time: Optional[int] = None
    has_aggressive_anti_spam_enabled: Optional[bool] = None
    has_hidden_members: Optional[bool] = None
    has_protected_content: Optional[bool] = None
    sticker_set_name: Optional[str] = None
    can_set_sticker_set: Optional[bool] = None
    linked_chat_id: Optional[int] = None
    location: Optional[ChatLocation] = None


@dataclass
class Message(BaseObject):
    message_id: int
    date: int
    chat: Chat
    from_: Optional[User] = None
    message_thread_id: Optional[int] = None
    sender_chat: Optional[Chat] = None
    forward_from: Optional[User] = None
    forward_from_chat: Optional[Chat] = None
    forward_from_message_id: Optional[int] = None
    forward_signature: Optional[str] = None
    forward_sender_name: Optional[str] = None
    forward_date: Optional[int] = None
    is_topic_message: Optional[bool] = None
    is_automatic_forward: Optional[bool] = None
    reply_to_message: Optional[Message] = None
    via_bot: Optional[User] = None
    edit_date: Optional[int] = None
    has_protected_content: Optional[bool] = None
    media_group_id: Optional[str] = None
    author_signature: Optional[str] = None
    text: Optional[str] = None
    entities: Optional[List[MessageEntity]] = None
    animation: Optional[Animation] = None
    audio: Optional[Audio] = None
    document: Optional[Document] = None
    photo: Optional[List[PhotoSize]] = None
    sticker: Optional[Sticker] = None
    video: Optional[Video] = None
    video_note: Optional[VideoNote] = None
    voice: Optional[Voice] = None
    caption: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    has_media_spoiler: Optional[bool] = None
    contact: Optional[Contact] = None
    dice: Optional[Dice] = None
    game: Optional[Game] = None
    poll: Optional[Poll] = None
    venue: Optional[Venue] = None
    location: Optional[Location] = None
    new_chat_members: Optional[List[User]] = None
    left_chat_member: Optional[User] = None
    new_chat_title: Optional[str] = None
    new_chat_photo: Optional[List[PhotoSize]] = None
    delete_chat_photo: Optional[bool] = None
    group_chat_created: Optional[bool] = None
    supergroup_chat_created: Optional[bool] = None
    channel_chat_created: Optional[bool] = None
    message_auto_delete_timer_changed: Optional[MessageAutoDeleteTimerChanged] = None
    migrate_to_chat_id: Optional[int] = None
    migrate_from_chat_id: Optional[int] = None
    pinned_message: Optional[Message] = None
    invoice: Optional[Invoice] = None
    successful_payment: Optional[SuccessfulPayment] = None
    connected_website: Optional[str] = None
    write_access_allowed: Optional[WriteAccessAllowed] = None
    passport_data: Optional[PassportData] = None
    proximity_alert_triggered: Optional[ProximityAlertTriggered] = None
    forum_topic_created: Optional[ForumTopicCreated] = None
    forum_topic_edited: Optional[ForumTopicEdited] = None
    forum_topic_closed: Optional[ForumTopicClosed] = None
    forum_topic_reopened: Optional[ForumTopicReopened] = None
    general_forum_topic_hidden: Optional[GeneralForumTopicHidden] = None
    general_forum_topic_unhidden: Optional[GeneralForumTopicUnhidden] = None
    video_chat_scheduled: Optional[VideoChatScheduled] = None
    video_chat_started: Optional[VideoChatStarted] = None
    video_chat_ended: Optional[VideoChatEnded] = None
    video_chat_participants_invited: Optional[VideoChatParticipantsInvited] = None
    web_app_data: Optional[WebAppData] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None


@dataclass
class MessageId(BaseObject):
    message_id: int


@dataclass
class MessageEntity(BaseObject):
    type: MessageEntityType
    offset: int
    length: int
    url: Optional[str] = None
    user: Optional[User] = None
    language: Optional[str] = None
    custom_emoji_id: Optional[str] = None


@dataclass
class PhotoSize(BaseObject):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: Optional[int] = None


@dataclass
class Animation(BaseObject):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumb: Optional[PhotoSize] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


@dataclass
class Audio(BaseObject):
    file_id: str
    file_unique_id: str
    duration: int
    performer: Optional[str] = None
    title: Optional[str] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    thumb: Optional[PhotoSize] = None


@dataclass
class Document(BaseObject):
    file_id: str
    file_unique_id: str
    thumb: Optional[PhotoSize] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


@dataclass
class Video(BaseObject):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumb: Optional[PhotoSize] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


@dataclass
class VideoNote(BaseObject):
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumb: Optional[PhotoSize] = None
    file_size: Optional[int] = None


@dataclass
class Voice(BaseObject):
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


@dataclass
class Contact(BaseObject):
    phone_number: str
    first_name: str
    last_name: Optional[str] = None
    user_id: Optional[int] = None
    vcard: Optional[str] = None


@dataclass
class Dice(BaseObject):
    emoji: str
    value: int


@dataclass
class PollOption(BaseObject):
    text: str
    voter_count: int


@dataclass
class PollAnswer(BaseObject):
    poll_id: str
    user: User
    option_ids: List[int]


@dataclass
class Poll(BaseObject):
    id: str
    question: str
    options: List[PollOption]
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: PollType
    allows_multiple_answers: bool
    correct_option_id: Optional[bool] = None
    explanation: Optional[str] = None
    explanation_entities: Optional[List[MessageEntity]] = None
    open_period: Optional[int] = None
    close_date: Optional[int] = None


@dataclass
class Location(BaseObject):
    longitude: float
    latitude: float
    horizontal_accuracy: Optional[float] = None
    live_period: Optional[int] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None


@dataclass
class Venue(BaseObject):
    location: Location
    title: str
    address: str
    foursquare_id: Optional[str] = None
    foursquare_type: Optional[str] = None
    google_place_id: Optional[str] = None
    google_place_type: Optional[str] = None


@dataclass
class WebAppData(BaseObject):
    data: str
    button_text: str


@dataclass
class ProximityAlertTriggered(BaseObject):
    traveler: User
    watcher: User
    distance: int


@dataclass
class MessageAutoDeleteTimerChanged(BaseObject):
    message_auto_delete_time: int


@dataclass
class ForumTopicCreated(BaseObject):
    name: str
    icon_color: int
    icon_custom_emoji_id: Optional[str] = None


@dataclass
class ForumTopicClosed(BaseObject):
    pass


@dataclass
class ForumTopicEdited(BaseObject):
    name: Optional[str] = None
    icon_custom_emoji_id: Optional[str] = None


@dataclass
class ForumTopicReopened(BaseObject):
    pass


@dataclass
class GeneralForumTopicHidden(BaseObject):
    pass


@dataclass
class GeneralForumTopicUnhidden(BaseObject):
    pass


@dataclass
class WriteAccessAllowed(BaseObject):
    pass


@dataclass
class VideoChatScheduled(BaseObject):
    start_date: int


@dataclass
class VideoChatStarted(BaseObject):
    pass


@dataclass
class VideoChatEnded(BaseObject):
    duration: int


@dataclass
class VideoChatParticipantsInvited(BaseObject):
    users: List[User]


@dataclass
class UserProfilePhotos(BaseObject):
    total_count: int
    photos: List[List[PhotoSize]]


@dataclass
class File(BaseObject):
    file_id: str
    file_unique_id: str
    file_size: Optional[int] = None
    file_path: Optional[str] = None


@dataclass
class WebAppInfo(BaseObject):
    url: str


@dataclass
class Keyboard(BaseObject):
    pass


@dataclass
class ReplyKeyboardMarkup(Keyboard):
    keyboard: List[List[KeyboardButton]]
    is_persistent: Optional[bool] = None
    resize_keyboard: Optional[bool] = None
    one_time_keyboard: Optional[bool] = None
    input_field_placeholder: Optional[str] = None
    selective: Optional[bool] = None


@dataclass
class KeyboardButton(BaseObject):
    text: str
    request_contact: Optional[bool] = None
    request_location: Optional[bool] = None
    request_poll: Optional[KeyboardButtonPollType] = None
    web_app: Optional[WebAppInfo] = None


@dataclass
class KeyboardButtonPollType(BaseObject):
    type: PollType


@dataclass
class ReplyKeyboardRemove(Keyboard):
    remove_keyboard: bool = True
    selective: Optional[bool] = None


@dataclass
class InlineKeyboardMarkup(Keyboard):
    inline_keyboard: List[List[InlineKeyboardButton]]


@dataclass
class InlineKeyboardButton(BaseObject):
    text: str
    url: Optional[str] = None
    callback_data: Optional[str] = None
    web_app: Optional[WebAppInfo] = None
    login_url: Optional[LoginUrl] = None
    switch_inline_query: Optional[str] = None
    switch_inline_query_current_chat: Optional[str] = None
    callback_game: Optional[CallbackGame] = None
    pay: Optional[bool] = None


@dataclass
class LoginUrl(BaseObject):
    url: str
    forward_text: Optional[str] = None
    bot_username: Optional[str] = None
    request_write_access: Optional[bool] = None


@dataclass
class CallbackQuery(BaseObject):
    id: str
    from_: User
    message: Optional[Message] = None
    inline_message_id: Optional[str] = None
    chat_instance: Optional[str] = None
    data: Optional[str] = None
    game_short_name: Optional[str] = None


@dataclass
class ForceReply(Keyboard):
    force_reply: bool = True
    input_field_placeholder: Optional[str] = None
    selective: Optional[bool] = None


@dataclass
class ChatPhoto(BaseObject):
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str


@dataclass
class ChatInviteLink(BaseObject):
    invite_link: str
    creator: User
    creates_join_request: bool
    is_primary: bool
    is_revoked: bool
    name: Optional[str] = None
    expire_date: Optional[int] = None
    member_limit: Optional[int] = None
    pending_join_request_count: Optional[int] = None


@dataclass
class ChatAdministratorRights(BaseObject):
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_video_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_messages: Optional[bool] = None
    can_edit_messages: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    can_manage_topics: Optional[bool] = None


@dataclass
class ChatMember(BaseObject):

    @classmethod
    def from_dict(cls, data: dict):
        status = data['status']

        if status == chat_member_status.CREATOR:
            class_ = ChatMemberOwner
        elif status == chat_member_status.ADMINISTRATOR:
            class_ = ChatMemberAdministrator
        elif status == chat_member_status.MEMBER:
            class_ = ChatMemberMember
        elif status == chat_member_status.RESTRICTED:
            class_ = ChatMemberRestricted
        elif status == chat_member_status.LEFT:
            class_ = ChatMemberLeft
        elif status == chat_member_status.KICKED:
            class_ = ChatMemberBanned
        else:
            raise Exception('Undefined chat_member_status')  # TODO: specify exception

        return class_.from_dict(data)


@dataclass
class ChatMemberOwner(ChatMember):
    user: User
    is_anonymous: bool
    status: ChatMemberStatus = chat_member_status.CREATOR
    custom_title: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        return BaseObject.from_dict(data)


@dataclass
class ChatMemberAdministrator(ChatMember):
    user: User
    can_be_edited: bool
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_video_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    status: ChatMemberStatus = chat_member_status.ADMINISTRATOR
    can_post_messages: Optional[bool] = None
    can_edit_messages: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    can_manage_topics: Optional[bool] = None
    custom_title: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        return BaseObject.from_dict(data)


@dataclass
class ChatMemberMember(ChatMember):
    user: User
    status: ChatMemberStatus = chat_member_status.MEMBER

    @classmethod
    def from_dict(cls, data: dict):
        return BaseObject.from_dict(data)


@dataclass
class ChatMemberRestricted(ChatMember):
    user: User
    is_member: bool
    can_change_info: bool
    can_invite_users: bool
    can_pin_messages: bool
    can_manage_topics: bool
    can_send_messages: bool
    can_send_media_messages: bool
    can_send_polls: bool
    can_send_other_messages: bool
    can_add_web_page_previews: bool
    until_date: int
    status: ChatMemberStatus = chat_member_status.RESTRICTED

    @classmethod
    def from_dict(cls, data: dict):
        return BaseObject.from_dict(data)


@dataclass
class ChatMemberLeft(ChatMember):
    user: User
    status: ChatMemberStatus = chat_member_status.LEFT

    @classmethod
    def from_dict(cls, data: dict):
        return BaseObject.from_dict(data)


@dataclass
class ChatMemberBanned(ChatMember):
    user: User
    until_date: int
    status: ChatMemberStatus = chat_member_status.KICKED

    @classmethod
    def from_dict(cls, data: dict):
        return BaseObject.from_dict(data)


@dataclass
class ChatMemberUpdated(BaseObject):
    chat: Chat
    from_: User
    date: int
    old_chat_member: ChatMember
    new_chat_member: ChatMember
    invite_link: Optional[ChatInviteLink] = None
    via_chat_folder_invite_link: Optional[bool] = None


@dataclass
class ChatJoinRequest(BaseObject):
    chat: Chat
    from_: User
    date: int
    bio: Optional[str] = None
    invite_link: Optional[ChatInviteLink] = None


@dataclass
class ChatPermissions(BaseObject):
    can_send_messages: Optional[bool] = None
    can_send_media_messages: Optional[bool] = None
    can_send_polls: Optional[bool] = None
    can_send_other_messages: Optional[bool] = None
    can_add_web_page_previews: Optional[bool] = None
    can_change_info: Optional[bool] = None
    can_invite_users: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    can_manage_topics: Optional[bool] = None


@dataclass
class ChatLocation(BaseObject):
    location: Location
    address: str


@dataclass
class ForumTopic(BaseObject):
    message_thread_id: int
    name: str
    icon_color: int
    icon_custom_emoji_id: Optional[str] = None


@dataclass
class BotCommand(BaseObject):
    command: str
    description: str


@dataclass
class BotCommandScope(BaseObject):
    pass


@dataclass
class BotCommandScopeDefault(BotCommandScope):
    type: BotCommandScopeType = bot_command_scope_type.DEFAULT


@dataclass
class BotCommandScopeAllPrivateChats(BotCommandScope):
    type: BotCommandScopeType = bot_command_scope_type.ALL_PRIVATE_CHATS


@dataclass
class BotCommandScopeAllGroupChats(BotCommandScope):
    type: BotCommandScopeType = bot_command_scope_type.ALL_GROUP_CHATS


@dataclass
class BotCommandScopeAllChatAdministrators(BotCommandScope):
    type: BotCommandScopeType = bot_command_scope_type.ALL_CHAT_ADMINISTRATORS


@dataclass
class BotCommandScopeChat(BotCommandScope):
    chat_id: str
    type: BotCommandScopeType = bot_command_scope_type.CHAT


@dataclass
class BotCommandScopeChatAdministrators(BotCommandScope):
    chat_id: str
    type: BotCommandScopeType = bot_command_scope_type.CHAT_ADMINISTRATORS


@dataclass
class BotCommandScopeChatMember(BotCommandScope):
    chat_id: str
    user_id: str
    type: BotCommandScopeType = bot_command_scope_type.CHAT_MEMBER


@dataclass
class MenuButton(BaseObject):
    pass


@dataclass
class MenuButtonCommands(MenuButton):
    type: MenuButtonType = menu_button_type.COMMANDS


@dataclass
class MenuButtonWebApp(MenuButton):
    text: str
    web_app: WebAppInfo
    type: MenuButtonType = menu_button_type.WEB_APP


@dataclass
class MenuButtonDefault(MenuButton):
    type: MenuButtonType = menu_button_type.DEFAULT


@dataclass
class ResponseParameters(BaseObject):
    migrate_to_chat_id: Optional[int] = None
    retry_after: Optional[int] = None


@dataclass
class InputMedia(BaseObject):
    pass


@dataclass
class InputMediaPhoto(InputMedia):
    media: str
    type: InputMediaType = input_media_type.PHOTO
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    has_spoiler: Optional[bool] = None


@dataclass
class InputMediaVideo(InputMedia):
    media: str
    type: InputMediaType = input_media_type.VIDEO
    thumb: Optional[InputFile] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
    supports_streaming: Optional[bool] = None
    has_spoiler: Optional[bool] = None


@dataclass
class InputMediaAnimation(InputMedia):
    media: str
    type: InputMediaType = input_media_type.ANIMATION
    thumb: Optional[InputFile] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
    has_spoiler: Optional[bool] = None


@dataclass
class InputMediaAudio(InputMedia):
    media: str
    type: InputMediaType = input_media_type.AUDIO
    thumb: Optional[InputFile] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    duration: Optional[int] = None
    performer: Optional[str] = None
    title: Optional[str] = None


@dataclass
class InputMediaDocument(InputMedia):
    media: str
    type: InputMediaType = input_media_type.DOCUMENT
    thumb: Optional[InputFile] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    disable_content_type_detection: Optional[bool] = None


@dataclass
class InputFile(BaseObject):
    pass


@dataclass
class InputFileStored(InputFile):
    file_id: str
    type: InputFileType = input_file_type.STORED


@dataclass
class InputFileUrl(InputFile):
    url: str
    type: InputFileType = input_file_type.URL


@dataclass
class InputFilePath(InputFile):
    path: pathlib.Path
    type: InputFileType = input_file_type.PATH


@dataclass
class Sticker(BaseObject):
    file_id: str
    file_unique_id: str
    type: StickerType
    width: int
    height: int
    is_animated: bool
    is_video: bool
    thumb: Optional[PhotoSize] = None
    emoji: Optional[str] = None
    set_name: Optional[str] = None
    premium_animation: Optional[File] = None
    mask_position: Optional[MaskPosition] = None
    custom_emoji_id: Optional[str] = None
    file_size: Optional[int] = None


@dataclass
class StickerSet(BaseObject):
    name: str
    title: str
    type: StickerType
    is_animated: bool
    is_video: bool
    stickers: List[Sticker]
    thumb: Optional[PhotoSize] = None


@dataclass
class MaskPosition(BaseObject):
    point: MaskPositionPoint
    x_shift: float
    y_shift: float
    scale: float


@dataclass
class InlineQuery(BaseObject):
    id: str
    from_: User
    query: str
    offset: str
    chat_type: Optional[InlineQueryChatType] = None
    location: Optional[Location] = None


@dataclass
class InlineQueryResult(BaseObject):
    pass


@dataclass
class InlineQueryResultArticle(InlineQueryResult):
    id: str
    title: str
    input_message_content: InputMessageContent
    type: InlineQueryResultType = inline_query_result_type.ARTICLE
    reply_markup: Optional[InlineKeyboardMarkup] = None
    url: Optional[str] = None
    hide_url: Optional[bool] = None
    description: Optional[str] = None
    thumb_url: Optional[str] = None
    thumb_width: Optional[int] = None
    thumb_height: Optional[int] = None


@dataclass
class InlineQueryResultPhoto(InlineQueryResult):
    id: str
    photo_url: str
    thumb_url: str
    type: InlineQueryResultType = inline_query_result_type.PHOTO
    photo_width: Optional[int] = None
    photo_height: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None


@dataclass
class InlineQueryResultGif(InlineQueryResult):
    id: str
    gif_url: str
    type: InlineQueryResultType = inline_query_result_type.GIF
    gif_width: Optional[int] = None
    gif_height: Optional[int] = None
    gif_duration: Optional[int] = None
    thumb_url: Optional[str] = None
    thumb_mime_type: Optional[str] = None
    title: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None


@dataclass
class InlineQueryResultMpeg4Gif(InlineQueryResult):
    id: str
    mpeg4_url: str
    type: InlineQueryResultType = inline_query_result_type.MPEG4_GIF
    mpeg4_width: Optional[int] = None
    mpeg4_height: Optional[int] = None
    mpeg4_duration: Optional[int] = None
    thumb_url: Optional[str] = None
    thumb_mime_type: Optional[str] = None
    title: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None


@dataclass
class InlineQueryResultVideo(InlineQueryResult):
    id: str
    video_url: str
    mime_type: str
    thumb_url: str
    title: str
    type: InlineQueryResultType = inline_query_result_type.VIDEO
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    video_width: Optional[int] = None
    video_height: Optional[int] = None
    video_duration: Optional[int] = None
    description: Optional[str] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None


@dataclass
class InlineQueryResultAudio(InlineQueryResult):
    id: str
    audio_url: str
    title: str
    type: InlineQueryResultType = inline_query_result_type.AUDIO
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    performer: Optional[str] = None
    audio_duration: Optional[int] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None


@dataclass
class InlineQueryResultVoice(InlineQueryResult):
    id: str
    voice_url: str
    title: str
    type: InlineQueryResultType = inline_query_result_type.VOICE
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    voice_duration: Optional[int] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None


@dataclass
class InlineQueryResultDocument(InlineQueryResult):
    id: str
    title: str
    document_url: str
    mime_type: str
    type: InlineQueryResultType = inline_query_result_type.DOCUMENT
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    description: Optional[str] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None
    thumb_url: Optional[str] = None
    thumb_width: Optional[int] = None
    thumb_height: Optional[int] = None


@dataclass
class InlineQueryResultLocation(InlineQueryResult):
    id: str
    latitude: float
    longitude: float
    title: str
    type: InlineQueryResultType = inline_query_result_type.LOCATION
    horizontal_accuracy: Optional[float] = None
    live_period: Optional[int] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None
    thumb_url: Optional[str] = None
    thumb_width: Optional[int] = None
    thumb_height: Optional[int] = None


@dataclass
class InlineQueryResultVenue(InlineQueryResult):
    id: str
    latitude: float
    longitude: float
    title: str
    address: str
    type: InlineQueryResultType = inline_query_result_type.VENUE
    foursquare_id: Optional[str] = None
    foursquare_type: Optional[str] = None
    google_place_id: Optional[str] = None
    google_place_type: Optional[str] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None
    thumb_url: Optional[str] = None
    thumb_width: Optional[int] = None
    thumb_height: Optional[int] = None


@dataclass
class InlineQueryResultContact(InlineQueryResult):
    id: str
    phone_number: str
    first_name: str
    type: InlineQueryResultType = inline_query_result_type.CONTACT
    last_name: Optional[str] = None
    vcard: Optional[str] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None
    thumb_url: Optional[str] = None
    thumb_width: Optional[int] = None
    thumb_height: Optional[int] = None


@dataclass
class InlineQueryResultGame(InlineQueryResult):
    id: str
    game_short_name: str
    type: InlineQueryResultType = inline_query_result_type.GAME
    reply_markup: Optional[InlineKeyboardMarkup] = None


@dataclass
class InlineQueryResultCachedPhoto(InlineQueryResult):
    id: str
    photo_file_id: str
    type: InlineQueryResultType = inline_query_result_type.PHOTO
    title: Optional[str] = None
    description: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None


@dataclass
class InlineQueryResultCachedGif(InlineQueryResult):
    id: str
    gif_file_id: str
    type: InlineQueryResultType = inline_query_result_type.GIF
    title: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None


@dataclass
class InlineQueryResultCachedMpeg4Gif(InlineQueryResult):
    id: str
    mpeg4_file_id: str
    type: InlineQueryResultType = inline_query_result_type.MPEG4_GIF
    title: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None


@dataclass
class InlineQueryResultCachedSticker(InlineQueryResult):
    id: str
    sticker_file_id: str
    type: InlineQueryResultType = inline_query_result_type.STICKER
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None


@dataclass
class InlineQueryResultCachedDocument(InlineQueryResult):
    id: str
    title: str
    document_file_id: str
    type: InlineQueryResultType = inline_query_result_type.DOCUMENT
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    description: Optional[str] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None


@dataclass
class InlineQueryResultCachedVideo(InlineQueryResult):
    id: str
    video_file_id: str
    title: str
    type: InlineQueryResultType = inline_query_result_type.VIDEO
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    description: Optional[str] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None


@dataclass
class InlineQueryResultCachedVoice(InlineQueryResult):
    id: str
    voice_file_id: str
    title: str
    type: InlineQueryResultType = inline_query_result_type.VOICE
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None


@dataclass
class InlineQueryResultCachedAudio(InlineQueryResult):
    id: str
    audio_file_id: str
    type: InlineQueryResultType = inline_query_result_type.AUDIO
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None


@dataclass
class InputMessageContent(BaseObject):
    pass


@dataclass
class InputTextMessageContent(InputMessageContent):
    message_text: str
    parse_mode: Optional[str] = None
    entities: Optional[List[MessageEntity]] = None
    disable_web_page_preview: Optional[bool] = None


@dataclass
class InputLocationMessageContent(InputMessageContent):
    latitude: float
    longitude: float
    horizontal_accuracy: Optional[float] = None
    live_period: Optional[int] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None


@dataclass
class InputVenueMessageContent(InputMessageContent):
    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: Optional[str] = None
    foursquare_type: Optional[str] = None
    google_place_id: Optional[str] = None
    google_place_type: Optional[str] = None


@dataclass
class InputContactMessageContent(InputMessageContent):
    phone_number: str
    first_name: str
    last_name: Optional[str] = None
    vcard: Optional[str] = None


@dataclass
class InputInvoiceMessageContent(InputMessageContent):
    title: str
    description: str
    payload: str
    provider_token: str
    currency: str
    prices: List[LabeledPrice]
    max_tip_amount: Optional[int] = None
    suggested_tip_amounts: Optional[List[int]] = None
    provider_data: Optional[str] = None
    photo_url: Optional[str] = None
    photo_size: Optional[int] = None
    photo_width: Optional[int] = None
    photo_height: Optional[int] = None
    need_name: Optional[bool] = None
    need_phone_number: Optional[bool] = None
    need_email: Optional[bool] = None
    need_shipping_address: Optional[bool] = None
    send_phone_number_to_provider: Optional[bool] = None
    send_email_to_provider: Optional[bool] = None
    is_flexible: Optional[bool] = None


@dataclass
class ChosenInlineResult(BaseObject):
    result_id: str
    from_: User
    location: Optional[Location] = None
    inline_message_id: Optional[str] = None
    query: Optional[str] = None


@dataclass
class SentWebAppMessage(BaseObject):
    inline_message_id: Optional[str] = None


@dataclass
class LabeledPrice(BaseObject):
    label: str
    amount: int


@dataclass
class Invoice(BaseObject):
    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int


@dataclass
class ShippingAddress(BaseObject):
    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str


@dataclass
class OrderInfo(BaseObject):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    shipping_address: Optional[ShippingAddress] = None


@dataclass
class ShippingOption(BaseObject):
    id: str
    title: str
    prices: List[LabeledPrice]


@dataclass
class SuccessfulPayment(BaseObject):
    currency: str
    total_amount: int
    invoice_payload: str
    telegram_payment_charge_id: str
    provider_payment_charge_id: str
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None


@dataclass
class ShippingQuery(BaseObject):
    id: str
    from_: User
    invoice_payload: str
    shipping_address: ShippingAddress


@dataclass
class PreCheckoutQuery(BaseObject):
    id: str
    from_: User
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str] = None
    order_info: Optional[OrderInfo] = None


@dataclass
class PassportData(BaseObject):
    data: List[EncryptedPassportElement]
    credentials: EncryptedCredentials


@dataclass
class PassportFile(BaseObject):
    file_id: str
    file_unique_id: str
    file_size: int
    file_date: int


@dataclass
class EncryptedPassportElement(BaseObject):
    type: EncryptedPassportElementType
    hash: str
    data: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    files: Optional[List[PassportFile]] = None
    front_side: Optional[PassportFile] = None
    reverse_side: Optional[PassportFile] = None
    selfie: Optional[PassportFile] = None
    translation: Optional[List[PassportFile]] = None


@dataclass
class EncryptedCredentials(BaseObject):
    data: str
    hash: str
    secret: str


@dataclass
class PassportElementError(BaseObject):
    pass


@dataclass
class PassportElementErrorDataField(PassportElementError):
    type: EncryptedPassportElementType
    field_name: str
    data_hash: str
    message: str
    source: PassportElementErrorSource = passport_element_error_source.DATA


@dataclass
class PassportElementErrorFrontSide(PassportElementError):
    type: EncryptedPassportElementType
    file_hash: str
    message: str
    source: PassportElementErrorSource = passport_element_error_source.FRONT_SIDE


@dataclass
class PassportElementErrorReverseSide(PassportElementError):
    type: EncryptedPassportElementType
    file_hash: str
    message: str
    source: PassportElementErrorSource = passport_element_error_source.REVERSE_SIDE


@dataclass
class PassportElementErrorSelfie(PassportElementError):
    type: EncryptedPassportElementType
    file_hash: str
    message: str
    source: PassportElementErrorSource = passport_element_error_source.SELFIE


@dataclass
class PassportElementErrorFile(PassportElementError):
    type: EncryptedPassportElementType
    file_hash: str
    message: str
    source: PassportElementErrorSource = passport_element_error_source.FILE


@dataclass
class PassportElementErrorFiles(PassportElementError):
    type: EncryptedPassportElementType
    file_hashes: List[str]
    message: str
    source: PassportElementErrorSource = passport_element_error_source.FILES


@dataclass
class PassportElementErrorTranslationFile(PassportElementError):
    type: EncryptedPassportElementType
    file_hash: str
    message: str
    source: PassportElementErrorSource = passport_element_error_source.TRANSLATION_FILE


@dataclass
class PassportElementErrorTranslationFiles(PassportElementError):
    type: EncryptedPassportElementType
    file_hashes: List[str]
    message: str
    source: PassportElementErrorSource = passport_element_error_source.TRANSLATION_FILES


@dataclass
class PassportElementErrorUnspecified(PassportElementError):
    type: EncryptedPassportElementType
    element_hash: str
    message: str
    source: PassportElementErrorSource = passport_element_error_source.UNSPECIFIED


@dataclass
class Game(BaseObject):
    title: str
    description: str
    photo: List[PhotoSize]
    text: Optional[str] = None
    text_entities: Optional[List[MessageEntity]] = None
    animation: Optional[Animation] = None


@dataclass
class CallbackGame(BaseObject):
    pass


@dataclass
class GameHighScore(BaseObject):
    position: int
    user: User
    score: int


@dataclass
class BaseContext:
    update: Update
    update_type: Optional[UpdateType] = None
    chat_id: Optional[int] = None
    user_id: Optional[int] = None

    @property
    def is_message(self) -> bool:
        return self.update.message is not None

    @property
    def is_edited_message(self) -> bool:
        return self.update.edited_message is not None

    @property
    def is_channel_post(self) -> bool:
        return self.update.channel_post is not None

    @property
    def is_edited_channel_post(self) -> bool:
        return self.update.edited_channel_post is not None

    @property
    def is_inline_query(self) -> bool:
        return self.update.inline_query is not None

    @property
    def is_chosen_inline_result(self) -> bool:
        return self.update.chosen_inline_result is not None

    @property
    def is_callback_query(self) -> bool:
        return self.update.callback_query is not None

    @property
    def is_shipping_query(self) -> bool:
        return self.update.shipping_query is not None

    @property
    def is_pre_checkout_query(self) -> bool:
        return self.update.pre_checkout_query is not None

    @property
    def is_poll(self) -> bool:
        return self.update.poll is not None

    @property
    def is_poll_answer(self) -> bool:
        return self.update.poll_answer is not None

    @property
    def is_my_chat_member(self) -> bool:
        return self.update.my_chat_member is not None

    @property
    def is_chat_member(self) -> bool:
        return self.update.chat_member is not None

    @property
    def is_chat_join_request(self) -> bool:
        return self.update.chat_join_request is not None

    @property
    def is_message_command(self) -> bool:
        return self.is_message and self.update.message.text is not None and self.update.message.text.startswith('/')

    @property
    def is_message_text(self) -> bool:
        return self.is_message and self.update.message.text is not None and not self.update.message.text.startswith('/')

    @property
    def is_message_dice(self) -> bool:
        return self.is_message and self.update.message.dice is not None

    @property
    def is_message_document(self) -> bool:
        return self.is_message and self.update.message.document is not None and self.update.message.animation is None

    @property
    def is_message_animation(self) -> bool:
        return self.is_message and self.update.message.animation is not None

    @property
    def is_message_audio(self) -> bool:
        return self.is_message and self.update.message.audio is not None

    @property
    def is_message_contact(self) -> bool:
        return self.is_message and self.update.message.contact is not None

    @property
    def is_message_game(self) -> bool:
        return self.is_message and self.update.message.game is not None

    @property
    def is_message_invoice(self) -> bool:
        return self.is_message and self.update.message.invoice is not None

    @property
    def is_message_left_chat_member(self) -> bool:
        return self.is_message and self.update.message.left_chat_member is not None

    @property
    def is_message_location(self) -> bool:
        return self.is_message and self.update.message.location is not None

    @property
    def is_message_new_chat_members(self) -> bool:
        return self.is_message and self.update.message.new_chat_members is not None

    @property
    def is_message_new_chat_photo(self) -> bool:
        return self.is_message and self.update.message.new_chat_photo is not None

    @property
    def is_message_new_chat_title(self) -> bool:
        return self.is_message and self.update.message.new_chat_title is not None

    @property
    def is_message_photo(self) -> bool:
        return self.is_message and self.update.message.photo is not None

    @property
    def is_message_sticker(self) -> bool:
        return self.is_message and self.update.message.sticker is not None

    @property
    def is_message_successful_payment(self) -> bool:
        return self.is_message and self.update.message.successful_payment is not None

    @property
    def is_message_venue(self) -> bool:
        return self.is_message and self.update.message.venue is not None

    @property
    def is_message_video(self) -> bool:
        return self.is_message and self.update.message.video is not None

    @property
    def is_message_video_note(self) -> bool:
        return self.is_message and self.update.message.video_note is not None

    @property
    def is_message_voice(self) -> bool:
        return self.is_message and self.update.message.voice is not None

    @property
    def is_message_poll(self) -> bool:
        return self.is_message and self.update.message.poll is not None


HandleFunction = Callable[[BaseContext], Awaitable[None]]
MiddlewareFunction = Callable[[BaseContext], Awaitable[bool]]
