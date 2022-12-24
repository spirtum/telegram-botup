from __future__ import annotations
import pathlib
from dataclasses import dataclass, asdict, is_dataclass
from typing import get_type_hints, get_origin, get_args, Optional, Union, List, Any

from .constants import ChatType, MessageEntityType, PollType, ChatMemberStatus, CHAT_MEMBER_STATUS_CREATOR, \
    CHAT_MEMBER_STATUS_ADMINISTRATOR, CHAT_MEMBER_STATUS_MEMBER, CHAT_MEMBER_STATUS_RESTRICTED, CHAT_MEMBER_STATUS_LEFT, \
    CHAT_MEMBER_STATUS_KICKED, BotCommandScopeType, BOT_COMMAND_SCOPE_TYPE_DEFAULT, \
    BOT_COMMAND_SCOPE_TYPE_ALL_PRIVATE_CHATS, BOT_COMMAND_SCOPE_TYPE_ALL_GROUP_CHATS, \
    BOT_COMMAND_SCOPE_TYPE_ALL_CHAT_ADMINISTRATORS, BOT_COMMAND_SCOPE_TYPE_CHAT, \
    BOT_COMMAND_SCOPE_TYPE_CHAT_ADMINISTRATORS, BOT_COMMAND_SCOPE_TYPE_CHAT_MEMBER, MenuButtonType, \
    MENU_BUTTON_TYPE_COMMANDS, MENU_BUTTON_TYPE_WEB_APP, MENU_BUTTON_TYPE_DEFAULT, InputMediaType, \
    INPUT_MEDIA_TYPE_PHOTO, INPUT_MEDIA_TYPE_VIDEO, INPUT_MEDIA_TYPE_ANIMATION, INPUT_MEDIA_TYPE_AUDIO, \
    INPUT_MEDIA_TYPE_DOCUMENT, InputFileType, INPUT_FILE_TYPE_STORED, INPUT_FILE_TYPE_URL, INPUT_FILE_TYPE_PATH, \
    StickerType, MaskPositionPoint

try:
    import ujson as json
except ImportError:
    import json


NoneType = type(None)


_rename_key_mapping = {
    'from_': 'from'
}


def _from_dict_helper(data: Any, class_: Any) -> Any:
    if is_dataclass(class_):
        assert isinstance(data, dict)
        return class_.from_dict(data)

    origin = get_origin(class_)
    args = get_args(class_)

    if origin is Union:
        return _from_dict_helper(data, args[0])

    if origin is list:
        assert isinstance(data, list)
        inner_type = get_args(class_)[0]
        return [_from_dict_helper(v, inner_type) for v in data]

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

            kwargs[hint_key] = _from_dict_helper(
                data=value,
                class_=hint_value
            )

        return cls(**kwargs)

    def as_dict(self):
        return asdict(self)

    def is_error(self):
        return isinstance(self, ErrorResponse)


@dataclass
class RawResponse(BaseObject):
    raw_data: dict
    ok: bool
    result: bool
    description: str


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
    passport_data: Optional[PassportData] = None
    proximity_alert_triggered: Optional[ProximityAlertTriggered] = None
    forum_topic_created: Optional[ForumTopicCreated] = None
    forum_topic_closed: Optional[ForumTopicClosed] = None
    forum_topic_reopened: Optional[ForumTopicReopened] = None
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
    thumb: Optional[PhotoSize]
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
class ForumTopicReopened(BaseObject):
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
    file_size: Optional[int]
    file_path: Optional[str]


@dataclass
class WebAppInfo(BaseObject):
    url: str


@dataclass
class ReplyKeyboardMarkup(BaseObject):
    keyboard: List[List[KeyboardButton]]
    resize_keyboard: Optional[bool]
    one_time_keyboard: Optional[bool]
    input_field_placeholder: Optional[str]
    selective: Optional[bool]


@dataclass
class KeyboardButton(BaseObject):
    text: str
    request_contact: Optional[bool]
    request_location: Optional[bool]
    request_poll: Optional[KeyboardButtonPollType]
    web_app: Optional[WebAppInfo]


@dataclass
class KeyboardButtonPollType(BaseObject):
    type: PollType


@dataclass
class ReplyKeyboardRemove(BaseObject):
    remove_keyboard: bool = True
    selective: Optional[bool] = None


@dataclass
class InlineKeyboardMarkup(BaseObject):
    inline_keyboard: List[List[InlineKeyboardButton]]


@dataclass
class InlineKeyboardButton(BaseObject):
    text: str
    url: Optional[str]
    callback_data: Optional[str]
    web_app: Optional[WebAppInfo]
    login_url: Optional[LoginUrl]
    switch_inline_query: Optional[str]
    switch_inline_query_current_chat: Optional[str]
    callback_game: Optional[CallbackGame]
    pay: Optional[bool]


@dataclass
class LoginUrl(BaseObject):
    url: str
    forward_text: Optional[str]
    bot_username: Optional[str]
    request_write_access: Optional[bool]


@dataclass
class CallbackQuery(BaseObject):
    id: str
    from_: User
    message: Optional[Message]
    inline_message_id: Optional[str]
    chat_instance: Optional[str]
    data: Optional[str]
    game_short_name: Optional[str]


@dataclass
class ForceReply(BaseObject):
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
    name: Optional[str]
    expire_date: Optional[int]
    member_limit: Optional[int]
    pending_join_request_count: Optional[int]


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
    can_post_messages: Optional[bool]
    can_edit_messages: Optional[bool]
    can_pin_messages: Optional[bool]
    can_manage_topics: Optional[bool]


@dataclass
class ChatMember(BaseObject):
    pass


@dataclass
class ChatMemberOwner(ChatMember):
    user: User
    is_anonymous: bool
    status: ChatMemberStatus = CHAT_MEMBER_STATUS_CREATOR
    custom_title: Optional[str] = None


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
    status: ChatMemberStatus = CHAT_MEMBER_STATUS_ADMINISTRATOR
    can_post_messages: Optional[bool] = None
    can_edit_messages: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    can_manage_topics: Optional[bool] = None
    custom_title: Optional[str] = None


@dataclass
class ChatMemberMember(ChatMember):
    user: User
    status: ChatMemberStatus = CHAT_MEMBER_STATUS_MEMBER


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
    status: ChatMemberStatus = CHAT_MEMBER_STATUS_RESTRICTED


@dataclass
class ChatMemberLeft(ChatMember):
    user: User
    status: ChatMemberStatus = CHAT_MEMBER_STATUS_LEFT


@dataclass
class ChatMemberBanned(ChatMember):
    user: User
    until_date: int
    status: ChatMemberStatus = CHAT_MEMBER_STATUS_KICKED


@dataclass
class ChatMemberUpdated(BaseObject):
    chat: Chat
    from_: User
    date: int
    old_chat_member: ChatMember
    new_chat_member: ChatMember
    invite_link: Optional[ChatInviteLink]


@dataclass
class ChatJoinRequest(BaseObject):
    chat: Chat
    from_: User
    date: int
    bio: Optional[str]
    invite_link: Optional[ChatInviteLink]


@dataclass
class ChatPermissions(BaseObject):
    can_send_messages: Optional[bool]
    can_send_media_messages: Optional[bool]
    can_send_polls: Optional[bool]
    can_send_other_messages: Optional[bool]
    can_add_web_page_previews: Optional[bool]
    can_change_info: Optional[bool]
    can_invite_users: Optional[bool]
    can_pin_messages: Optional[bool]
    can_manage_topics: Optional[bool]


@dataclass
class ChatLocation(BaseObject):
    location: Location
    address: str


@dataclass
class ForumTopic(BaseObject):
    message_thread_id: int
    name: str
    icon_color: int
    icon_custom_emoji_id: Optional[str]


@dataclass
class BotCommand(BaseObject):
    command: str
    description: str


@dataclass
class BotCommandScope(BaseObject):
    pass


@dataclass
class BotCommandScoreDefault(BotCommandScope):
    type: BotCommandScopeType = BOT_COMMAND_SCOPE_TYPE_DEFAULT


@dataclass
class BotCommandScopeAllPrivateChats(BotCommandScope):
    type: BotCommandScopeType = BOT_COMMAND_SCOPE_TYPE_ALL_PRIVATE_CHATS


@dataclass
class BotCommandScopeAllGroupChats(BotCommandScope):
    type: BotCommandScopeType = BOT_COMMAND_SCOPE_TYPE_ALL_GROUP_CHATS


@dataclass
class BotCommandScopeAllChatAdministrators(BotCommandScope):
    type: BotCommandScopeType = BOT_COMMAND_SCOPE_TYPE_ALL_CHAT_ADMINISTRATORS


@dataclass
class BotCommandScopeChat(BotCommandScope):
    chat_id: str
    type: BotCommandScopeType = BOT_COMMAND_SCOPE_TYPE_CHAT


@dataclass
class BotCommandScopeChatAdministrators(BotCommandScope):
    chat_id: str
    type: BotCommandScopeType = BOT_COMMAND_SCOPE_TYPE_CHAT_ADMINISTRATORS


@dataclass
class BotCommandScopeChatMember(BotCommandScope):
    chat_id: str
    user_id: str
    type: BotCommandScopeType = BOT_COMMAND_SCOPE_TYPE_CHAT_MEMBER


@dataclass
class MenuButton(BaseObject):
    pass


@dataclass
class MenuButtonCommands(MenuButton):
    type: MenuButtonType = MENU_BUTTON_TYPE_COMMANDS


@dataclass
class MenuButtonWebApp(MenuButton):
    text: str
    web_app: WebAppInfo
    type: MenuButtonType = MENU_BUTTON_TYPE_WEB_APP


@dataclass
class MenuButtonDefault(MenuButton):
    type: MenuButtonType = MENU_BUTTON_TYPE_DEFAULT


@dataclass
class ResponseParameters(BaseObject):
    migrate_to_chat_id: Optional[int]
    retry_after: Optional[int]


@dataclass
class InputMedia(BaseObject):
    pass


@dataclass
class InputMediaPhoto(InputMedia):
    media: str
    type: InputMediaType = INPUT_MEDIA_TYPE_PHOTO
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None


@dataclass
class InputMediaVideo(InputMedia):
    media: str
    type: InputMediaType = INPUT_MEDIA_TYPE_VIDEO
    thumb: Optional[Union[InputFile, str]] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
    supports_streaming: Optional[bool] = None


@dataclass
class InputMediaAnimation(InputMedia):
    media: str
    type: InputMediaType = INPUT_MEDIA_TYPE_ANIMATION
    thumb: Optional[Union[InputFile, str]] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None


@dataclass
class InputMediaAudio(InputMedia):
    media: str
    type: InputMediaType = INPUT_MEDIA_TYPE_AUDIO
    thumb: Optional[Union[InputFile, str]] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    duration: Optional[int] = None
    performer: Optional[str] = None
    title: Optional[str] = None


@dataclass
class InputMediaDocument(InputMedia):
    media: str
    type: InputMediaType = INPUT_MEDIA_TYPE_DOCUMENT
    thumb: Optional[Union[InputFile, str]] = None
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
    type: InputFileType = INPUT_FILE_TYPE_STORED


@dataclass
class InputFileUrl(InputFile):
    url: str
    type: InputFileType = INPUT_FILE_TYPE_URL


@dataclass
class InputFilePath(InputFile):
    path: pathlib.Path
    type: InputFileType = INPUT_FILE_TYPE_PATH


@dataclass
class CallbackGame(BaseObject):
    pass


@dataclass
class Sticker(BaseObject):
    file_id: str
    file_unique_id: str
    type: StickerType
    width: int
    height: int
    is_animated: bool
    is_video: bool
    thumb: Optional[PhotoSize]
    emoji: Optional[str]
    set_name: Optional[str]
    premium_animation: Optional[File]
    mask_position: Optional[MaskPosition]
    custom_emoji_id: Optional[str]
    file_size: Optional[int]


@dataclass
class StickerSet(BaseObject):
    name: str
    title: str
    type: StickerType
    is_animated: bool
    is_video: bool
    stickers: List[Sticker]
    thumb: Optional[PhotoSize]


@dataclass
class MaskPosition(BaseObject):
    point: MaskPositionPoint
    x_shift: float
    y_shift: float
    scale: float


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
