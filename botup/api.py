import io
import json
from typing import (
    Optional,
    List,
    Union,
    Any,
    Type,
    get_type_hints,
    get_origin,
    get_args
)

from aiohttp import ClientSession

from botup.constants import api_method
from botup.constants.chat_action import ChatAction
from botup.constants.sticker_type import StickerType
from botup.types import (
    Update,
    InputFile,
    WebhookInfo,
    User,
    Message,
    MessageEntity,
    InlineKeyboardMarkup,
    MessageId,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    UserProfilePhotos,
    File,
    ChatPermissions,
    ChatInviteLink,
    Chat,
    ChatMember,
    Sticker,
    ForumTopic,
    BotCommand,
    BotCommandScope,
    MenuButton,
    ChatAdministratorRights,
    InputMedia,
    Poll,
    StickerSet,
    MaskPosition,
    InlineQueryResult,
    SentWebAppMessage,
    LabeledPrice,
    ShippingOption,
    PassportElementError,
    GameHighScore,
    InputFilePath,
    InputFileStored,
    InputFileUrl,
    BaseObject,
    Keyboard
)
from botup.utils import get_logger

logger = get_logger()


class Api:
    def __init__(self, token: str, timeout: int = 5):
        self.token = token
        self.timeout = timeout
        self._url = f'https://api.telegram.org/bot{self.token}/'
        self._session = ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.close_session()

    async def close_session(self):
        await self._session.close()

    async def _request(self, method: api_method.ApiMethod, data: dict, hints: dict) -> Any:
        response = await self._session.post(
            url=self._url + method,
            data=_prepare_args(data, hints),
            timeout=self.timeout
        )
        response_data = await response.json()

        if not response_data['ok']:
            raise Exception(response_data)

        return self._response(response_data['result'], hints['return'])

    @staticmethod
    def _response(data: Any, hint: Type) -> Any:
        origin = get_origin(hint)
        args = get_args(hint)

        if origin is list:
            class_ = args[0]
            return [class_.from_dict(d) for d in data]

        if origin is Union:
            class_, type_ = args
            if isinstance(data, type_):
                return data
            return class_.from_dict(data)

        if issubclass(hint, BaseObject):
            return hint.from_dict(data)

        return data

    async def get_updates(
            self,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            timeout: Optional[int] = None,
            allowed_updates: Optional[List[str]] = None
    ) -> List[Update]:

        return await self._request(
            method=api_method.GET_UPDATES,
            data=locals(),
            hints=get_type_hints(self.get_updates)
        )

    async def set_webhook(
            self,
            url: str,
            certificate: Optional[InputFilePath] = None,
            ip_address: Optional[str] = None,
            max_connections: Optional[int] = None,
            allowed_updates: Optional[List[str]] = None,
            drop_pending_updates: Optional[bool] = None,
            secret_token: Optional[str] = None
    ) -> bool:

        return await self._request(
            method=api_method.SET_WEBHOOK,
            data=locals(),
            hints=get_type_hints(self.set_webhook)
        )

    async def delete_webhook(
            self,
            drop_pending_updates: Optional[bool] = None
    ) -> bool:

        return await self._request(
            method=api_method.DELETE_WEBHOOK,
            data=locals(),
            hints=get_type_hints(self.delete_webhook)
        )

    async def get_webhook_info(self) -> WebhookInfo:
        return await self._request(
            method=api_method.GET_WEBHOOK_INFO,
            data=locals(),
            hints=get_type_hints(self.get_webhook_info)
        )

    async def get_me(self) -> User:
        return await self._request(
            method=api_method.GET_ME,
            data=locals(),
            hints=get_type_hints(self.get_me)
        )

    async def logout(self) -> bool:
        return await self._request(
            method=api_method.LOGOUT,
            data=locals(),
            hints=get_type_hints(self.logout)
        )

    async def close(self) -> bool:
        return await self._request(
            method=api_method.CLOSE,
            data=locals(),
            hints=get_type_hints(self.close)
        )

    async def send_message(
            self,
            chat_id: Union[int, str],
            text: str,
            parse_mode: Optional[str] = None,
            entities: Optional[List[MessageEntity]] = None,
            disable_web_page_preview: Optional[bool] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Optional[Keyboard] = None
    ) -> Message:

        return await self._request(
            method=api_method.SEND_MESSAGE,
            data=locals(),
            hints=get_type_hints(self.send_message)
        )

    async def forward_message(
            self,
            chat_id: Union[int, str],
            from_chat_id: Union[int, str],
            message_id: int,
            message_thread_id: Optional[int] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None
    ) -> Message:

        return await self._request(
            method=api_method.FORWARD_MESSAGE,
            data=locals(),
            hints=get_type_hints(self.forward_message)
        )

    async def copy_message(
            self,
            chat_id: Union[int, str],
            from_chat_id: Union[int, str],
            message_id: int,
            message_thread_id: Optional[int] = None,
            caption: Optional[str] = None,
            parse_mode: Optional[str] = None,
            caption_entities: Optional[List[MessageEntity]] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Optional[Keyboard] = None
    ) -> MessageId:

        return await self._request(
            method=api_method.COPY_MESSAGE,
            data=locals(),
            hints=get_type_hints(self.copy_message)
        )

    async def send_photo(
            self,
            chat_id: Union[int, str],
            photo: InputFile,
            message_thread_id: Optional[int] = None,
            caption: Optional[str] = None,
            parse_mode: Optional[str] = None,
            caption_entities: Optional[List[MessageEntity]] = None,
            has_spoiler: Optional[bool] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Optional[Keyboard] = None
    ) -> Message:

        return await self._request(
            method=api_method.SEND_PHOTO,
            data=locals(),
            hints=get_type_hints(self.send_photo)
        )

    async def send_audio(
            self,
            chat_id: Union[int, str],
            audio: InputFile,
            message_thread_id: Optional[int] = None,
            caption: Optional[str] = None,
            parse_mode: Optional[str] = None,
            caption_entities: Optional[List[MessageEntity]] = None,
            duration: Optional[int] = None,
            performer: Optional[str] = None,
            title: Optional[str] = None,
            thumb: Optional[InputFile] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Optional[Keyboard] = None
    ) -> Message:

        return await self._request(
            method=api_method.SEND_AUDIO,
            data=locals(),
            hints=get_type_hints(self.send_audio)
        )

    async def send_document(
            self,
            chat_id: Union[int, str],
            document: InputFile,
            message_thread_id: Optional[int] = None,
            thumb: Optional[InputFile] = None,
            caption: Optional[str] = None,
            parse_mode: Optional[str] = None,
            caption_entities: Optional[List[MessageEntity]] = None,
            disable_content_type_detection: Optional[bool] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Optional[Keyboard] = None
    ) -> Message:

        return await self._request(
            method=api_method.SEND_DOCUMENT,
            data=locals(),
            hints=get_type_hints(self.send_document)
        )

    async def send_video(
            self,
            chat_id: Union[int, str],
            video: InputFile,
            message_thread_id: Optional[int] = None,
            duration: Optional[int] = None,
            width: Optional[int] = None,
            height: Optional[int] = None,
            thumb: Optional[InputFile] = None,
            caption: Optional[str] = None,
            parse_mode: Optional[str] = None,
            caption_entities: Optional[List[MessageEntity]] = None,
            has_spoiler: Optional[bool] = None,
            supports_streaming: Optional[bool] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Optional[Keyboard] = None
    ) -> Message:

        return await self._request(
            method=api_method.SEND_VIDEO,
            data=locals(),
            hints=get_type_hints(self.send_video)
        )

    async def send_animation(
            self,
            chat_id: Union[int, str],
            animation: InputFile,
            message_thread_id: Optional[int] = None,
            duration: Optional[int] = None,
            width: Optional[int] = None,
            height: Optional[int] = None,
            thumb: Optional[InputFile] = None,
            caption: Optional[str] = None,
            parse_mode: Optional[str] = None,
            caption_entities: Optional[List[MessageEntity]] = None,
            has_spoiler: Optional[bool] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Optional[Keyboard] = None
    ) -> Message:

        return await self._request(
            method=api_method.SEND_ANIMATION,
            data=locals(),
            hints=get_type_hints(self.send_animation)
        )

    async def send_voice(
            self,
            chat_id: Union[int, str],
            voice: InputFile,
            message_thread_id: Optional[int] = None,
            caption: Optional[str] = None,
            parse_mode: Optional[str] = None,
            caption_entities: Optional[List[MessageEntity]] = None,
            duration: Optional[int] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Optional[Keyboard] = None
    ) -> Message:

        return await self._request(
            method=api_method.SEND_VOICE,
            data=locals(),
            hints=get_type_hints(self.send_voice)
        )

    async def send_video_note(
            self,
            chat_id: Union[int, str],
            video_note: InputFile,
            message_thread_id: Optional[int] = None,
            duration: Optional[int] = None,
            length: Optional[int] = None,
            thumb: Optional[InputFile] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Optional[Keyboard] = None
    ) -> Message:

        return await self._request(
            method=api_method.SEND_VIDEO_NOTE,
            data=locals(),
            hints=get_type_hints(self.send_video_note)
        )

    async def send_media_group(
            self,
            chat_id: Union[int, str],
            media: List[Union[InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo]],
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None
    ) -> List[Message]:

        return await self._request(
            method=api_method.SEND_MEDIA_GROUP,
            data=locals(),
            hints=get_type_hints(self.send_media_group)
        )

    async def send_location(
            self,
            chat_id: Union[int, str],
            latitude: float,
            longitude: float,
            message_thread_id: Optional[int] = None,
            horizontal_accuracy: Optional[float] = None,
            live_period: Optional[int] = None,
            heading: Optional[int] = None,
            proximity_alert_radius: Optional[int] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Optional[Keyboard] = None
    ) -> Message:

        return await self._request(
            method=api_method.SEND_LOCATION,
            data=locals(),
            hints=get_type_hints(self.send_location)
        )

    async def edit_message_live_location(
            self,
            latitude: float,
            longitude: float,
            chat_id: Union[int, str, None] = None,
            message_id: Optional[int] = None,
            inline_message_id: Optional[int] = None,
            horizontal_accuracy: Optional[float] = None,
            heading: Optional[int] = None,
            proximity_alert_radius: Optional[int] = None,
            reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, bool]:

        return await self._request(
            method=api_method.EDIT_MESSAGE_LIVE_LOCATION,
            data=locals(),
            hints=get_type_hints(self.edit_message_live_location)
        )

    async def stop_message_live_location(
            self,
            chat_id: Union[int, str, None] = None,
            message_id: Optional[int] = None,
            inline_message_id: Optional[str] = None,
            reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, bool]:

        return await self._request(
            method=api_method.STOP_MESSAGE_LIVE_LOCATION,
            data=locals(),
            hints=get_type_hints(self.stop_message_live_location)
        )

    async def send_venue(
            self,
            chat_id: Union[int, str],
            latitude: float,
            longitude: float,
            title: str,
            address: str,
            message_thread_id: Optional[int] = None,
            foursquare_id: Optional[str] = None,
            foursquare_type: Optional[str] = None,
            google_place_id: Optional[str] = None,
            google_place_type: Optional[str] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Optional[Keyboard] = None
    ) -> Message:

        return await self._request(
            method=api_method.SEND_VENUE,
            data=locals(),
            hints=get_type_hints(self.send_venue)
        )

    async def send_contact(
            self,
            chat_id: Union[int, str],
            phone_number: str,
            first_name: str,
            message_thread_id: Optional[int] = None,
            last_name: Optional[str] = None,
            vcard: Optional[str] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Optional[Keyboard] = None
    ) -> Message:

        return await self._request(
            method=api_method.SEND_CONTACT,
            data=locals(),
            hints=get_type_hints(self.send_contact)
        )

    async def send_poll(
            self,
            chat_id: Union[int, str],
            question: str,
            options: List[str],
            message_thread_id: Optional[int] = None,
            is_anonymous: Optional[bool] = None,
            type: Optional[str] = None,
            allows_multiple_answers: Optional[bool] = None,
            correct_option_id: Optional[int] = None,
            explanation: Optional[str] = None,
            explanation_parse_mode: Optional[str] = None,
            explanation_entities: Optional[List[MessageEntity]] = None,
            open_period: Optional[int] = None,
            close_date: Optional[int] = None,
            is_closed: Optional[bool] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Optional[Keyboard] = None
    ) -> Message:

        data = locals()
        data['options'] = json.dumps(data['options'])
        return await self._request(
            method=api_method.SEND_POLL,
            data=data,
            hints=get_type_hints(self.send_poll)
        )

    async def send_dice(
            self,
            chat_id: Union[int, str],
            message_thread_id: Optional[int] = None,
            emoji: Optional[str] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Optional[Keyboard] = None
    ) -> Message:

        return await self._request(
            method=api_method.SEND_DICE,
            data=locals(),
            hints=get_type_hints(self.send_dice)
        )

    async def send_chat_action(
            self,
            chat_id: Union[int, str],
            action: ChatAction,
            message_thread_id: Optional[int] = None
    ) -> bool:

        return await self._request(
            method=api_method.SEND_CHAT_ACTION,
            data=locals(),
            hints=get_type_hints(self.send_chat_action)
        )

    async def get_user_profile_photos(
            self,
            user_id: int,
            offset: Optional[int] = None,
            limit: Optional[int] = None
    ) -> UserProfilePhotos:

        return await self._request(
            method=api_method.GET_USER_PROFILE_PHOTOS,
            data=locals(),
            hints=get_type_hints(self.get_user_profile_photos)
        )

    async def get_file(
            self,
            file_id: str
    ) -> File:

        return await self._request(
            method=api_method.GET_FILE,
            data=locals(),
            hints=get_type_hints(self.get_file)
        )

    async def ban_chat_member(
            self,
            chat_id: Union[int, str],
            user_id: int,
            until_date: Optional[int] = None,
            revoke_messages: Optional[bool] = None
    ) -> bool:

        return await self._request(
            method=api_method.BAN_CHAT_MEMBER,
            data=locals(),
            hints=get_type_hints(self.ban_chat_member)
        )

    async def unban_chat_member(
            self,
            chat_id: Union[int, str],
            user_id: int,
            only_if_banned: Optional[bool] = None
    ) -> bool:

        return await self._request(
            method=api_method.UNBAN_CHAT_MEMBER,
            data=locals(),
            hints=get_type_hints(self.unban_chat_member)
        )

    async def restrict_chat_member(
            self,
            chat_id: Union[int, str],
            user_id: int,
            permissions: ChatPermissions,
            until_date: Optional[int] = None
    ) -> bool:

        return await self._request(
            method=api_method.RESTRICT_CHAT_MEMBER,
            data=locals(),
            hints=get_type_hints(self.restrict_chat_member)
        )

    async def promote_chat_member(
            self,
            chat_id: Union[int, str],
            user_id: int,
            is_anonymous: Optional[bool] = None,
            can_manage_chat: Optional[bool] = None,
            can_post_messages: Optional[bool] = None,
            can_edit_messages: Optional[bool] = None,
            can_delete_messages: Optional[bool] = None,
            can_manage_video_chats: Optional[bool] = None,
            can_restrict_members: Optional[bool] = None,
            can_promote_members: Optional[bool] = None,
            can_change_info: Optional[bool] = None,
            can_invite_users: Optional[bool] = None,
            can_pin_messages: Optional[bool] = None,
            can_manage_topics: Optional[bool] = None
    ) -> bool:

        return await self._request(
            method=api_method.PROMOTE_CHAT_MEMBER,
            data=locals(),
            hints=get_type_hints(self.promote_chat_member)
        )

    async def set_chat_administrator_custom_title(
            self,
            chat_id: Union[int, str],
            user_id: int,
            custom_title: str
    ) -> bool:

        return await self._request(
            method=api_method.SET_CHAT_ADMINISTRATOR_CUSTOM_TITLE,
            data=locals(),
            hints=get_type_hints(self.set_chat_administrator_custom_title)
        )

    async def ban_chat_sender_chat(
            self,
            chat_id: Union[int, str],
            sender_chat_id: int
    ) -> bool:

        return await self._request(
            method=api_method.BAN_CHAT_SENDER_CHAT,
            data=locals(),
            hints=get_type_hints(self.ban_chat_sender_chat)
        )

    async def unban_chat_sender_chat(
            self,
            chat_id: Union[int, str],
            sender_chat_id: int
    ) -> bool:

        return await self._request(
            method=api_method.UNBAN_CHAT_SENDER_CHAT,
            data=locals(),
            hints=get_type_hints(self.unban_chat_sender_chat)
        )

    async def set_chat_permissions(
            self,
            chat_id: Union[int, str],
            permissions: ChatPermissions
    ) -> bool:

        return await self._request(
            method=api_method.SET_CHAT_PERMISSIONS,
            data=locals(),
            hints=get_type_hints(self.set_chat_permissions)
        )

    async def export_chat_invite_link(
            self,
            chat_id: Union[int, str]
    ) -> str:

        return await self._request(
            method=api_method.EXPORT_CHAT_INVITE_LINK,
            data=locals(),
            hints=get_type_hints(self.export_chat_invite_link)
        )

    async def create_chat_invite_link(
            self,
            chat_id: Union[int, str],
            name: Optional[str] = None,
            expire_date: Optional[int] = None,
            member_limit: Optional[int] = None,
            creates_join_request: Optional[bool] = None
    ) -> ChatInviteLink:

        return await self._request(
            method=api_method.CREATE_CHAT_INVITE_LINK,
            data=locals(),
            hints=get_type_hints(self.create_chat_invite_link)
        )

    async def edit_chat_invite_link(
            self,
            chat_id: Union[int, str],
            invite_link: str,
            name: Optional[str] = None,
            expire_date: Optional[int] = None,
            member_limit: Optional[int] = None,
            creates_join_request: Optional[bool] = None
    ) -> ChatInviteLink:

        return await self._request(
            method=api_method.EDIT_CHAT_INVITE_LINK,
            data=locals(),
            hints=get_type_hints(self.edit_chat_invite_link)
        )

    async def revoke_chat_invite_link(
            self,
            chat_id: Union[int, str],
            invite_link: str
    ) -> ChatInviteLink:

        return await self._request(
            method=api_method.REVOKE_CHAT_INVITE_LINK,
            data=locals(),
            hints=get_type_hints(self.revoke_chat_invite_link)
        )

    async def approve_chat_join_request(
            self,
            chat_id: Union[int, str],
            user_id: int
    ) -> bool:

        return await self._request(
            method=api_method.APPROVE_CHAT_JOIN_REQUEST,
            data=locals(),
            hints=get_type_hints(self.approve_chat_join_request)
        )

    async def decline_chat_join_request(
            self,
            chat_id: Union[int, str],
            user_id: int
    ) -> bool:

        return await self._request(
            method=api_method.DECLINE_CHAT_JOIN_REQUEST,
            data=locals(),
            hints=get_type_hints(self.decline_chat_join_request)
        )

    async def set_chat_photo(
            self,
            chat_id: Union[int, str],
            photo: InputFile
    ) -> bool:

        return await self._request(
            method=api_method.SET_CHAT_PHOTO,
            data=locals(),
            hints=get_type_hints(self.set_chat_photo)
        )

    async def delete_chat_photo(
            self,
            chat_id: Union[int, str]
    ) -> bool:

        return await self._request(
            method=api_method.DELETE_CHAT_PHOTO,
            data=locals(),
            hints=get_type_hints(self.delete_chat_photo)
        )

    async def set_chat_title(
            self,
            chat_id: Union[int, str],
            title: str
    ) -> bool:

        return await self._request(
            method=api_method.SET_CHAT_TITLE,
            data=locals(),
            hints=get_type_hints(self.set_chat_title)
        )

    async def set_chat_description(
            self,
            chat_id: Union[int, str],
            description: Optional[str] = None
    ) -> bool:

        return await self._request(
            method=api_method.SET_CHAT_DESCRIPTION,
            data=locals(),
            hints=get_type_hints(self.set_chat_description)
        )

    async def pin_chat_message(
            self,
            chat_id: Union[int, str],
            message_id: int,
            disable_notification: Optional[bool] = None
    ) -> bool:

        return await self._request(
            method=api_method.PIN_CHAT_MESSAGE,
            data=locals(),
            hints=get_type_hints(self.pin_chat_message)
        )

    async def unpin_chat_message(
            self,
            chat_id: Union[int, str],
            message_id: Optional[int] = None
    ) -> bool:

        return await self._request(
            method=api_method.UNPIN_CHAT_MESSAGE,
            data=locals(),
            hints=get_type_hints(self.unpin_chat_message)
        )

    async def unpin_all_chat_messages(
            self,
            chat_id: Union[int, str]
    ) -> bool:

        return await self._request(
            method=api_method.UNPIN_ALL_CHAT_MESSAGES,
            data=locals(),
            hints=get_type_hints(self.unpin_all_chat_messages)
        )

    async def leave_chat(
            self,
            chat_id: Union[int, str]
    ) -> bool:

        return await self._request(
            method=api_method.LEAVE_CHAT,
            data=locals(),
            hints=get_type_hints(self.leave_chat)
        )

    async def get_chat(
            self,
            chat_id: Union[int, str]
    ) -> Chat:

        return await self._request(
            method=api_method.GET_CHAT,
            data=locals(),
            hints=get_type_hints(self.get_chat)
        )

    async def get_chat_administrators(
            self,
            chat_id: Union[int, str]
    ) -> List[ChatMember]:

        return await self._request(
            method=api_method.GET_CHAT_ADMINISTRATORS,
            data=locals(),
            hints=get_type_hints(self.get_chat_administrators)
        )

    async def get_chat_member_count(
            self,
            chat_id: Union[int, str]
    ) -> int:

        return await self._request(
            method=api_method.GET_CHAT_MEMBER_COUNT,
            data=locals(),
            hints=get_type_hints(self.get_chat_member_count)
        )

    async def get_chat_member(
            self,
            chat_id: Union[int, str],
            user_id: int
    ) -> ChatMember:

        return await self._request(
            method=api_method.GET_CHAT_MEMBER,
            data=locals(),
            hints=get_type_hints(self.get_chat_member)
        )

    async def set_chat_sticker_set(
            self,
            chat_id: Union[int, str],
            sticker_set_name: str
    ) -> bool:

        return await self._request(
            method=api_method.SET_CHAT_STICKER_SET,
            data=locals(),
            hints=get_type_hints(self.set_chat_sticker_set)
        )

    async def delete_chat_sticker_set(
            self,
            chat_id: Union[int, str]
    ) -> bool:

        return await self._request(
            method=api_method.DELETE_CHAT_STICKER_SET,
            data=locals(),
            hints=get_type_hints(self.delete_chat_sticker_set)
        )

    async def get_forum_topic_icon_stickers(
            self
    ) -> List[Sticker]:

        return await self._request(
            method=api_method.GET_FORUM_TOPIC_ICON_STICKERS,
            data=locals(),
            hints=get_type_hints(self.get_forum_topic_icon_stickers)
        )

    async def create_forum_topic(
            self,
            chat_id: Union[int, str],
            name: str,
            icon_color: Optional[int] = None,
            icon_custom_emoji_id: Optional[str] = None
    ) -> ForumTopic:

        return await self._request(
            method=api_method.CREATE_FORUM_TOPIC,
            data=locals(),
            hints=get_type_hints(self.create_forum_topic)
        )

    async def edit_forum_topic(
            self,
            chat_id: Union[int, str],
            message_thread_id: int,
            name: Optional[str] = None,
            icon_custom_emoji_id: Optional[str] = None
    ) -> bool:

        return await self._request(
            method=api_method.EDIT_FORUM_TOPIC,
            data=locals(),
            hints=get_type_hints(self.edit_forum_topic)
        )

    async def close_forum_topic(
            self,
            chat_id: Union[int, str],
            message_thread_id: int
    ) -> bool:

        return await self._request(
            method=api_method.CLOSE_FORUM_TOPIC,
            data=locals(),
            hints=get_type_hints(self.close_forum_topic)
        )

    async def reopen_forum_topic(
            self,
            chat_id: Union[int, str],
            message_thread_id: int
    ) -> bool:

        return await self._request(
            method=api_method.REOPEN_FORUM_TOPIC,
            data=locals(),
            hints=get_type_hints(self.reopen_forum_topic)
        )

    async def delete_forum_topic(
            self,
            chat_id: Union[int, str],
            message_thread_id: int
    ) -> bool:

        return await self._request(
            method=api_method.DELETE_FORUM_TOPIC,
            data=locals(),
            hints=get_type_hints(self.delete_forum_topic)
        )

    async def unpin_all_forum_topic_messages(
            self,
            chat_id: Union[int, str],
            message_thread_id: int
    ) -> bool:

        return await self._request(
            method=api_method.UNPIN_ALL_FORUM_TOPIC_MESSAGES,
            data=locals(),
            hints=get_type_hints(self.unpin_all_forum_topic_messages)
        )

    async def edit_general_forum_topic(
            self,
            chat_id: Union[int, str],
            name: str
    ) -> bool:

        return await self._request(
            method=api_method.EDIT_GENERAL_FORUM_TOPIC,
            data=locals(),
            hints=get_type_hints(self.edit_general_forum_topic)
        )

    async def close_general_forum_topic(
            self,
            chat_id: Union[int, str]
    ) -> bool:

        return await self._request(
            method=api_method.CLOSE_GENERAL_FORUM_TOPIC,
            data=locals(),
            hints=get_type_hints(self.close_general_forum_topic)
        )

    async def reopen_general_forum_topic(
            self,
            chat_id: Union[int, str]
    ) -> bool:

        return await self._request(
            method=api_method.REOPEN_GENERAL_FORUM_TOPIC,
            data=locals(),
            hints=get_type_hints(self.reopen_general_forum_topic)
        )

    async def hide_general_forum_topic(
            self,
            chat_id: Union[int, str]
    ) -> bool:

        return await self._request(
            method=api_method.HIDE_GENERAL_FORUM_TOPIC,
            data=locals(),
            hints=get_type_hints(self.hide_general_forum_topic)
        )

    async def unhide_general_forum_topic(
            self,
            chat_id: Union[int, str]
    ) -> bool:

        return await self._request(
            method=api_method.UNHIDE_GENERAL_FORUM_TOPIC,
            data=locals(),
            hints=get_type_hints(self.unhide_general_forum_topic)
        )

    async def answer_callback_query(
            self,
            callback_query_id: str,
            text: Optional[str] = None,
            show_alert: Optional[bool] = None,
            url: Optional[str] = None,
            cache_time: Optional[int] = None
    ) -> bool:

        return await self._request(
            method=api_method.ANSWER_CALLBACK_QUERY,
            data=locals(),
            hints=get_type_hints(self.answer_callback_query)
        )

    async def set_my_commands(
            self,
            commands: List[BotCommand],
            scope: Optional[BotCommandScope] = None,
            language_code: Optional[str] = None
    ) -> bool:

        return await self._request(
            method=api_method.SET_MY_COMMANDS,
            data=locals(),
            hints=get_type_hints(self.set_my_commands)
        )

    async def delete_my_commands(
            self,
            scope: Optional[BotCommandScope] = None,
            language_code: Optional[str] = None
    ) -> bool:

        return await self._request(
            method=api_method.DELETE_MY_COMMANDS,
            data=locals(),
            hints=get_type_hints(self.delete_my_commands)
        )

    async def get_my_commands(
            self,
            scope: Optional[BotCommandScope] = None,
            language_code: Optional[str] = None
    ) -> List[BotCommand]:

        return await self._request(
            method=api_method.GET_MY_COMMANDS,
            data=locals(),
            hints=get_type_hints(self.get_my_commands)
        )

    async def set_chat_menu_button(
            self,
            chat_id: Optional[int] = None,
            menu_button: Optional[MenuButton] = None
    ) -> bool:

        return await self._request(
            method=api_method.SET_CHAT_MENU_BUTTON,
            data=locals(),
            hints=get_type_hints(self.set_chat_menu_button)
        )

    async def get_chat_menu_button(
            self,
            chat_id: Optional[int] = None
    ) -> MenuButton:

        return await self._request(
            method=api_method.GET_CHAT_MENU_BUTTON,
            data=locals(),
            hints=get_type_hints(self.get_chat_menu_button)
        )

    async def set_my_default_administrator_rights(
            self,
            rights: Optional[ChatAdministratorRights] = None,
            for_channels: Optional[bool] = None
    ) -> bool:

        return await self._request(
            method=api_method.SET_MY_DEFAULT_ADMINISTRATOR_RIGHTS,
            data=locals(),
            hints=get_type_hints(self.set_my_default_administrator_rights)
        )

    async def get_my_default_administrator_rights(
            self,
            for_channels: Optional[bool] = None
    ) -> ChatAdministratorRights:

        return await self._request(
            method=api_method.GET_MY_DEFAULT_ADMINISTRATOR_RIGHTS,
            data=locals(),
            hints=get_type_hints(self.get_my_default_administrator_rights)
        )

    async def edit_message_text(
            self,
            text: str,
            chat_id: Union[int, str, None] = None,
            message_id: Optional[int] = None,
            inline_message_id: Optional[str] = None,
            parse_mode: Optional[str] = None,
            entities: Optional[List[MessageEntity]] = None,
            disable_web_page_preview: Optional[bool] = None,
            reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, bool]:

        return await self._request(
            method=api_method.EDIT_MESSAGE_TEXT,
            data=locals(),
            hints=get_type_hints(self.edit_message_text)
        )

    async def edit_message_caption(
            self,
            chat_id: Union[int, str, None] = None,
            message_id: Optional[int] = None,
            inline_message_id: Optional[str] = None,
            caption: Optional[str] = None,
            parse_mode: Optional[str] = None,
            caption_entities: Optional[List[MessageEntity]] = None,
            reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, bool]:

        return await self._request(
            method=api_method.EDIT_MESSAGE_CAPTION,
            data=locals(),
            hints=get_type_hints(self.edit_message_caption)
        )

    async def edit_message_media(
            self,
            media: InputMedia,
            chat_id: Union[int, str, None] = None,
            message_id: Optional[int] = None,
            inline_message_id: Optional[str] = None,
            reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, bool]:

        return await self._request(
            method=api_method.EDIT_MESSAGE_MEDIA,
            data=locals(),
            hints=get_type_hints(self.edit_message_media)
        )

    async def edit_message_reply_markup(
            self,
            chat_id: Union[int, str, None] = None,
            message_id: Optional[int] = None,
            inline_message_id: Optional[str] = None,
            reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, bool]:

        return await self._request(
            method=api_method.EDIT_MESSAGE_REPLY_MARKUP,
            data=locals(),
            hints=get_type_hints(self.edit_message_reply_markup)
        )

    async def stop_poll(
            self,
            chat_id: Union[int, str],
            message_id: int,
            reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Poll:

        return await self._request(
            method=api_method.STOP_POLL,
            data=locals(),
            hints=get_type_hints(self.stop_poll)
        )

    async def delete_message(
            self,
            chat_id: Union[int, str],
            message_id: int
    ) -> bool:

        return await self._request(
            method=api_method.DELETE_MESSAGE,
            data=locals(),
            hints=get_type_hints(self.delete_message)
        )

    async def send_sticker(
            self,
            chat_id: Union[int, str],
            sticker: InputFile,
            message_thread_id: Optional[int] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Optional[Keyboard] = None
    ) -> Message:

        return await self._request(
            method=api_method.SEND_STICKER,
            data=locals(),
            hints=get_type_hints(self.send_sticker)
        )

    async def get_sticker_set(
            self,
            name: str
    ) -> StickerSet:

        return await self._request(
            method=api_method.GET_STICKER_SET,
            data=locals(),
            hints=get_type_hints(self.get_sticker_set)
        )

    async def get_custom_emoji_stickers(
            self,
            custom_emoji_ids: List[str]
    ) -> List[Sticker]:

        return await self._request(
            method=api_method.GET_CUSTOM_EMOJI_STICKERS,
            data=locals(),
            hints=get_type_hints(self.get_custom_emoji_stickers)
        )

    async def upload_sticker_file(
            self,
            user_id: int,
            png_sticker: InputFile
    ) -> File:

        return await self._request(
            method=api_method.UPLOAD_STICKER_FILE,
            data=locals(),
            hints=get_type_hints(self.upload_sticker_file)
        )

    async def create_new_sticker_set(
            self,
            user_id: int,
            name: str,
            title: str,
            emojis: str,
            png_sticker: Optional[InputFile] = None,
            tgs_sticker: Optional[InputFile] = None,
            webm_sticker: Optional[InputFile] = None,
            sticker_type: Optional[StickerType] = None,
            mask_position: Optional[MaskPosition] = None
    ) -> bool:

        return await self._request(
            method=api_method.CREATE_NEW_STICKER_SET,
            data=locals(),
            hints=get_type_hints(self.create_new_sticker_set)
        )

    async def add_sticker_to_set(
            self,
            user_id: int,
            name: str,
            emojis: str,
            png_sticker: Optional[InputFile] = None,
            tgs_sticker: Optional[InputFile] = None,
            webm_sticker: Optional[InputFile] = None,
            mask_position: Optional[MaskPosition] = None
    ) -> bool:

        return await self._request(
            method=api_method.ADD_STICKER_TO_SET,
            data=locals(),
            hints=get_type_hints(self.add_sticker_to_set)
        )

    async def set_sticker_position_in_set(
            self,
            sticker: str,
            position: int
    ) -> bool:

        return await self._request(
            method=api_method.SET_STICKER_POSITION_IN_SET,
            data=locals(),
            hints=get_type_hints(self.set_sticker_position_in_set)
        )

    async def delete_sticker_from_set(
            self,
            sticker: str
    ) -> bool:

        return await self._request(
            method=api_method.DELETE_STICKER_FROM_SET,
            data=locals(),
            hints=get_type_hints(self.delete_sticker_from_set)
        )

    async def set_sticker_set_thumb(
            self,
            name: str,
            user_id: int,
            thumb: Optional[InputFile] = None
    ) -> bool:

        return await self._request(
            method=api_method.SET_STICKER_SET_THUMB,
            data=locals(),
            hints=get_type_hints(self.set_sticker_set_thumb)
        )

    async def answer_inline_query(
            self,
            inline_query_id: str,
            results: List[InlineQueryResult],
            cache_time: Optional[int] = None,
            is_personal: Optional[bool] = None,
            next_offset: Optional[str] = None,
            switch_pm_text: Optional[str] = None,
            switch_pm_parameter: Optional[str] = None
    ) -> bool:

        return await self._request(
            method=api_method.ANSWER_INLINE_QUERY,
            data=locals(),
            hints=get_type_hints(self.answer_inline_query)
        )

    async def answer_web_app_query(
            self,
            web_app_query_id: str,
            result: InlineQueryResult
    ) -> SentWebAppMessage:

        return await self._request(
            method=api_method.ANSWER_WEB_APP_QUERY,
            data=locals(),
            hints=get_type_hints(self.answer_web_app_query)
        )

    async def send_invoice(
            self,
            chat_id: Union[int, str],
            title: str,
            description: str,
            payload: str,
            provider_token: str,
            currency: str,
            prices: List[LabeledPrice],
            message_thread_id: Optional[int] = None,
            max_tip_amount: Optional[int] = None,
            suggested_tip_amounts: Optional[List[int]] = None,
            start_parameter: Optional[str] = None,
            provider_data: Optional[str] = None,
            photo_url: Optional[str] = None,
            photo_size: Optional[int] = None,
            photo_width: Optional[int] = None,
            photo_height: Optional[int] = None,
            need_name: Optional[bool] = None,
            need_phone_number: Optional[bool] = None,
            need_email: Optional[bool] = None,
            need_shipping_address: Optional[bool] = None,
            send_phone_number_to_provider: Optional[bool] = None,
            send_email_to_provider: Optional[bool] = None,
            is_flexible: Optional[bool] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Message:

        return await self._request(
            method=api_method.SEND_INVOICE,
            data=locals(),
            hints=get_type_hints(self.send_invoice)
        )

    async def create_invoice_link(
            self,
            title: str,
            description: str,
            payload: str,
            provider_token: str,
            currency: str,
            prices: List[LabeledPrice],
            max_tip_amount: Optional[int] = None,
            suggested_tip_amounts: Optional[List[int]] = None,
            provider_data: Optional[str] = None,
            photo_url: Optional[str] = None,
            photo_size: Optional[int] = None,
            photo_width: Optional[int] = None,
            photo_height: Optional[int] = None,
            need_name: Optional[bool] = None,
            need_phone_number: Optional[bool] = None,
            need_email: Optional[bool] = None,
            need_shipping_address: Optional[bool] = None,
            send_phone_number_to_provider: Optional[bool] = None,
            send_email_to_provider: Optional[bool] = None,
            is_flexible: Optional[bool] = None
    ) -> str:

        return await self._request(
            method=api_method.CREATE_INVOICE_LINK,
            data=locals(),
            hints=get_type_hints(self.create_invoice_link)
        )

    async def answer_shipping_query(
            self,
            shipping_query_id: str,
            ok: bool,
            shipping_options: Optional[List[ShippingOption]] = None,
            error_message: Optional[str] = None
    ) -> bool:

        return await self._request(
            method=api_method.ANSWER_SHIPPING_QUERY,
            data=locals(),
            hints=get_type_hints(self.answer_shipping_query)
        )

    async def answer_pre_checkout_query(
            self,
            pre_checkout_query_id: str,
            ok: bool,
            error_message: Optional[str] = None
    ) -> bool:

        return await self._request(
            method=api_method.ANSWER_PRE_CHECKOUT_QUERY,
            data=locals(),
            hints=get_type_hints(self.answer_pre_checkout_query)
        )

    async def set_passport_data_errors(
            self,
            user_id: int,
            errors: List[PassportElementError]
    ) -> bool:

        return await self._request(
            method=api_method.SET_PASSPORT_DATA_ERRORS,
            data=locals(),
            hints=get_type_hints(self.set_passport_data_errors)
        )

    async def send_game(
            self,
            chat_id: int,
            game_short_name: str,
            message_thread_id: Optional[int] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Message:

        return await self._request(
            method=api_method.SEND_GAME,
            data=locals(),
            hints=get_type_hints(self.send_game)
        )

    async def set_game_score(
            self,
            user_id: int,
            score: int,
            force: Optional[bool] = None,
            disable_edit_message: Optional[bool] = None,
            chat_id: Optional[int] = None,
            message_id: Optional[int] = None,
            inline_message_id: Optional[str] = None
    ) -> Union[Message, bool]:

        return await self._request(
            method=api_method.SET_GAME_HIGH_SCORE,
            data=locals(),
            hints=get_type_hints(self.set_game_score)
        )

    async def get_game_high_scores(
            self,
            user_id: int,
            chat_id: Optional[int] = None,
            message_id: Optional[int] = None,
            inline_message_id: Optional[str] = None
    ) -> List[GameHighScore]:

        return await self._request(
            method=api_method.GET_GAME_HIGH_SCORES,
            data=locals(),
            hints=get_type_hints(self.get_game_high_scores)
        )


def _prepare_args(locals_args: dict, hints: dict) -> dict:
    result = {k: v for k, v in locals_args.items() if v is not None and k != 'self'}

    for key, value in result.items():
        func = _prepare_arg_by_type.get(type(value)) or _prepare_arg_by_list.get(hints[key])
        if func:
            result[key] = func(value)

    if _is_multipart_form_data(result):
        for key, value in result.items():
            if isinstance(value, (int, bool)):
                result[key] = str(result[key])

    return result


def _prepare_input_file(value: InputFile) -> Any:
    if isinstance(value, InputFileStored):
        return value.file_id

    if isinstance(value, InputFileUrl):
        return value.url

    assert isinstance(value, InputFilePath)
    return value.path.open('rb')


def _prepare_json_dumps_list(value: List[BaseObject]) -> Any:
    result = []

    for v in value:
        hints = get_type_hints(type(v))
        result.append(_prepare_args(v.as_dict(), hints))

    return json.dumps(result)


def _prepare_json_dumps(value: BaseObject) -> Any:
    return json.dumps(value.as_dict())


_prepare_arg_by_type = {
    InputFileStored: _prepare_input_file,
    InputFileUrl: _prepare_input_file,
    InputFilePath: _prepare_input_file,
    InlineKeyboardMarkup: _prepare_json_dumps,
    ChatPermissions: _prepare_json_dumps,
    BotCommandScope: _prepare_json_dumps,
    MenuButton: _prepare_json_dumps,
    ChatAdministratorRights: _prepare_json_dumps,
    MaskPosition: _prepare_json_dumps,
    InlineQueryResult: _prepare_json_dumps
}

_prepare_arg_by_list = {
    Optional[List[MessageEntity]]: _prepare_json_dumps_list,
    List[Union[InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo]]: _prepare_json_dumps_list,
    List[BotCommand]: _prepare_json_dumps_list,
    List[InlineQueryResult]: _prepare_json_dumps_list,
    List[LabeledPrice]: _prepare_json_dumps_list,
    Optional[List[ShippingOption]]: _prepare_json_dumps_list,
    List[PassportElementError]: _prepare_json_dumps_list
}


def _is_multipart_form_data(data: dict) -> bool:
    for value in data.values():
        if isinstance(value, io.BufferedReader) or (isinstance(value, dict) and _is_multipart_form_data(value)):
            return True

    return False
