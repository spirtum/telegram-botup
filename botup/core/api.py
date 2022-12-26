from typing import Optional, List, Union, Any

from aiohttp import ClientSession

try:
    import ujson as json
except ImportError:
    import json

from . import constants
from .types import Update, InputFile, WebhookInfo, User, \
    Message, MessageEntity, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply, MessageId, \
    InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo, UserProfilePhotos, File, ChatPermissions, \
    ChatInviteLink, Chat, ChatMember, Sticker, ForumTopic, BotCommand, BotCommandScope, MenuButton, \
    ChatAdministratorRights, InputMedia, Poll, StickerSet, MaskPosition, InlineQueryResult, SentWebAppMessage, \
    LabeledPrice, ShippingOption, PassportElementError, GameHighScore
from .utils import get_logger

logger = get_logger()


class Api:
    def __init__(self, token: str, timeout: int = 5):
        self.token = token
        self.timeout = timeout
        self._url = f'https://api.telegram.org/bot{self.token}/'
        self._session = ClientSession()

    async def close_session(self):
        await self._session.close()

    async def _request(self, method: constants.ApiMethod, data: dict) -> Any:
        response = await self._session.post(self._url + method, data=data, timeout=self.timeout)
        response_data = await response.json()

        if not response_data['ok']:
            raise Exception(response_data)

        return response_data['result']

    async def get_updates(
            self,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            timeout: Optional[int] = None,
            allowed_updates: Optional[List[str]] = None
    ) -> List[Update]:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_GET_UPDATES, data=data)
        return [Update.from_dict(r) for r in response]

    async def set_webhook(
            self,
            url: str,
            certificate: Optional[InputFile] = None,
            ip_address: Optional[str] = None,
            max_connections: Optional[int] = None,
            allowed_updates: Optional[List[str]] = None,
            drop_pending_updates: Optional[bool] = None,
            secret_token: Optional[str] = None
    ) -> bool:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SET_WEBHOOK, data=data)
        assert isinstance(response, bool)
        return response

    async def delete_webhook(
            self,
            drop_pending_updates: Optional[bool] = None
    ) -> bool:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_DELETE_WEBHOOK, data=data)
        assert isinstance(response, bool)
        return response

    async def get_webhook_info(self) -> WebhookInfo:
        response = await self._request(constants.API_METHOD_GET_WEBHOOK_INFO, data={})
        return WebhookInfo.from_dict(response)

    async def get_me(self) -> User:
        response = await self._request(constants.API_METHOD_GET_ME, data={})
        return User.from_dict(response)

    async def logout(self) -> bool:
        response = await self._request(constants.API_METHOD_LOGOUT, data={})
        assert isinstance(response, bool)
        return response

    async def close(self) -> bool:
        response = await self._request(constants.API_METHOD_CLOSE, data={})
        assert isinstance(response, bool)
        return response

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
            reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply] = None
    ) -> Message:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SEND_MESSAGE, data=data)
        return Message.from_dict(response)

    async def forward_message(
            self,
            chat_id: Union[int, str],
            from_chat_id: Union[int, str],
            message_id: int,
            message_thread_id: Optional[int] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None
    ) -> Message:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_FORWARD_MESSAGE, data=data)
        return Message.from_dict(response)

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
            reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply] = None
    ) -> MessageId:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_COPY_MESSAGE, data=data)
        return MessageId.from_dict(response)

    async def send_photo(
            self,
            chat_id: Union[int, str],
            photo: InputFile,
            message_thread_id: Optional[int] = None,
            caption: Optional[str] = None,
            parse_mode: Optional[str] = None,
            caption_entities: Optional[List[MessageEntity]] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply] = None
    ) -> Message:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SEND_PHOTO, data=data)
        return Message.from_dict(response)

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
            reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply] = None
    ) -> Message:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SEND_AUDIO, data=data)
        return Message.from_dict(response)

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
            reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply] = None
    ) -> Message:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SEND_DOCUMENT, data=data)
        return Message.from_dict(response)

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
            supports_streaming: Optional[bool] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply] = None
    ) -> Message:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SEND_VIDEO, data=data)
        return Message.from_dict(response)

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
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply] = None
    ) -> Message:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SEND_ANIMATION, data=data)
        return Message.from_dict(response)

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
            reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply] = None
    ) -> Message:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SEND_VOICE, data=data)
        return Message.from_dict(response)

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
            reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply] = None
    ) -> Message:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SEND_VIDEO_NOTE, data=data)
        return Message.from_dict(response)

    async def send_media_group(
            self,
            chat_id: Union[int, str],
            media: List[Union[InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo]],
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None
    ) -> List[Message]:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SEND_MEDIA_GROUP, data=data)
        return [Message.from_dict(r) for r in response]

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
            reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply] = None
    ) -> Message:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SEND_LOCATION, data=data)
        return MessageEntity.from_dict(response)

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

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_EDIT_MESSAGE_LIVE_LOCATION, data=data)

        if isinstance(response, bool):
            return response

        return Message.from_dict(response)

    async def stop_message_live_location(
            self,
            chat_id: Union[int, str, None] = None,
            message_id: Optional[int] = None,
            inline_message_id: Optional[str] = None,
            reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, bool]:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_STOP_MESSAGE_LIVE_LOCATION, data=data)

        if isinstance(response, bool):
            return response

        return Message.from_dict(response)

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
            reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply] = None
    ) -> Message:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SEND_VENUE, data=data)
        return Message.from_dict(response)

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
            reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply] = None
    ) -> Message:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SEND_CONTACT, data=data)
        return Message.from_dict(response)

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
            reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply] = None
    ) -> Message:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SEND_POLL, data=data)
        return Message.from_dict(response)

    async def send_dice(
            self,
            chat_id: Union[int, str],
            message_thread_id: Optional[int] = None,
            emoji: Optional[str] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply] = None
    ) -> Message:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SEND_DICE, data=data)
        return Message.from_dict(response)

    async def send_chat_action(self, chat_id: Union[int, str], action: constants.ChatAction) -> bool:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SEND_CHAT_ACTION, data=data)
        assert isinstance(response, bool)
        return response

    async def get_user_profile_photos(
            self,
            user_id: int,
            offset: Optional[int] = None,
            limit: Optional[int] = None
    ) -> UserProfilePhotos:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_GET_USER_PROFILE_PHOTOS, data=data)
        return UserProfilePhotos.from_dict(response)

    async def get_file(self, file_id: str) -> File:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_GET_FILE, data=data)
        return File.from_dict(response)

    async def ban_chat_member(
            self,
            chat_id: Union[int, str],
            user_id: int,
            until_date: Optional[int] = None,
            revoke_messages: Optional[bool] = None
    ) -> bool:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_BAN_CHAT_MEMBER, data=data)
        assert isinstance(response, bool)
        return response

    async def unban_chat_member(
            self,
            chat_id: Union[int, str],
            user_id: int,
            only_if_banned: Optional[bool] = None
    ) -> bool:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_UNBAN_CHAT_MEMBER, data=data)
        assert isinstance(response, bool)
        return response

    async def restrict_chat_member(
            self,
            chat_id: Union[int, str],
            user_id: int,
            permissions: ChatPermissions,
            until_date: Optional[int] = None
    ) -> bool:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_RESTRICT_CHAT_MEMBER, data=data)
        assert isinstance(response, bool)
        return response

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

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_PROMOTE_CHAT_MEMBER, data=data)
        assert isinstance(response, bool)
        return response

    async def set_chat_administrator_custom_title(
            self,
            chat_id: Union[int, str],
            user_id: int,
            custom_title: str
    ) -> bool:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SET_CHAT_ADMINISTRATOR_CUSTOM_TITLE, data=data)
        assert isinstance(response, bool)
        return response

    async def ban_chat_sender_chat(self, chat_id: Union[int, str], sender_chat_id: int) -> bool:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_BAN_CHAT_SENDER_CHAT, data=data)
        assert isinstance(response, bool)
        return response

    async def unban_chat_sender_chat(self, chat_id: Union[int, str], sender_chat_id: int) -> bool:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_UNBAN_CHAT_SENDER_CHAT, data=data)
        assert isinstance(response, bool)
        return response

    async def set_chat_permissions(self, chat_id: Union[int, str], permissions: ChatPermissions) -> bool:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SET_CHAT_PERMISSIONS, data=data)
        assert isinstance(response, bool)
        return response

    async def export_chat_invite_link(self, chat_id: Union[int, str]) -> str:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_EXPORT_CHAT_INVITE_LINK, data=data)
        assert isinstance(response, str)
        return response

    async def create_chat_invite_link(
            self,
            chat_id: Union[int, str],
            name: Optional[str] = None,
            expire_date: Optional[int] = None,
            member_limit: Optional[int] = None,
            creates_join_request: Optional[bool] = None
    ) -> ChatInviteLink:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_CREATE_CHAT_INVITE_LINK, data=data)
        return ChatInviteLink.from_dict(response)

    async def edit_chat_invite_link(
            self,
            chat_id: Union[int, str],
            invite_link: str,
            name: Optional[str] = None,
            expire_date: Optional[int] = None,
            member_limit: Optional[int] = None,
            creates_join_request: Optional[bool] = None
    ) -> ChatInviteLink:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_EDIT_CHAT_INVITE_LINK, data=data)
        return ChatInviteLink.from_dict(response)

    async def revoke_chat_invite_link(self, chat_id: Union[int, str], invite_link: str) -> ChatInviteLink:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_REVOKE_CHAT_INVITE_LINK, data=data)
        return ChatInviteLink.from_dict(response)

    async def approve_chat_join_request(self, chat_id: Union[int, str], user_id: int) -> bool:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_APPROVE_CHAT_JOIN_REQUEST, data=data)
        assert isinstance(response, bool)
        return response

    async def decline_chat_join_request(self, chat_id: Union[int, str], user_id: int) -> bool:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_DECLINE_CHAT_JOIN_REQUEST, data=data)
        assert isinstance(response, bool)
        return response

    async def set_chat_photo(self, chat_id: Union[int, str], photo: InputFile) -> bool:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SET_CHAT_PHOTO, data=data)
        assert isinstance(response, bool)
        return response

    async def delete_chat_photo(self, chat_id: Union[int, str]) -> bool:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_DELETE_CHAT_PHOTO, data=data)
        assert isinstance(response, bool)
        return response

    async def set_chat_title(self, chat_id: Union[int, str], title: str) -> bool:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SET_CHAT_TITLE, data=data)
        assert isinstance(response, bool)
        return response

    async def set_chat_description(self, chat_id: Union[int, str], description: Optional[str] = None) -> bool:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SET_CHAT_DESCRIPTION, data=data)
        assert isinstance(response, bool)
        return response

    async def pin_chat_message(
            self,
            chat_id: Union[int, str],
            message_id: int,
            disable_notification: Optional[bool] = None
    ) -> bool:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_PIN_CHAT_MESSAGE, data=data)
        assert isinstance(response, bool)
        return response

    async def unpin_chat_message(self, chat_id: Union[int, str], message_id: Optional[int] = None) -> bool:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_UNPIN_CHAT_MESSAGE, data=data)
        assert isinstance(response, bool)
        return response

    async def unpin_all_chat_messages(self, chat_id: Union[int, str]) -> bool:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_UNPIN_ALL_CHAT_MESSAGES, data=data)
        assert isinstance(response, bool)
        return response

    async def leave_chat(self, chat_id: Union[int, str]) -> bool:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_LEAVE_CHAT, data=data)
        assert isinstance(response, bool)
        return response

    async def get_chat(self, chat_id: Union[int, str]) -> Chat:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_GET_CHAT, data=data)
        return Chat.from_dict(response)

    async def get_chat_administrators(self, chat_id: Union[int, str]) -> List[ChatMember]:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_GET_CHAT_ADMINISTRATORS, data=data)
        return [ChatMember.from_dict(r) for r in response]

    async def get_chat_member_count(self, chat_id: Union[int, str]) -> int:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_GET_CHAT_MEMBER_COUNT, data=data)
        assert isinstance(response, int)
        return response

    async def get_chat_member(self, chat_id: Union[int, str], user_id: int) -> ChatMember:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_GET_CHAT_MEMBER, data=data)
        return ChatMember.from_dict(response)

    async def set_chat_sticker_set(self, chat_id: Union[int, str], sticker_set_name: str) -> bool:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SET_CHAT_STICKER_SET, data=data)
        assert isinstance(response, bool)
        return response

    async def delete_chat_sticker_set(self, chat_id: Union[int, str]) -> bool:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_DELETE_CHAT_STICKER_SET, data=data)
        assert isinstance(response, bool)
        return response

    async def get_forum_topic_icon_stickers(self) -> List[Sticker]:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_GET_FORUM_TOPIC_ICON_STICKERS, data=data)
        return [Sticker.from_dict(r) for r in response]

    async def create_forum_topic(
            self,
            chat_id: Union[int, str],
            name: str,
            icon_color: Optional[int] = None,
            icon_custom_emoji_id: Optional[str] = None
    ) -> ForumTopic:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_CREATE_FORUM_TOPIC, data=data)
        return ForumTopic.from_dict(response)

    async def edit_forum_topic(
            self,
            chat_id: Union[int, str],
            message_thread_id: int,
            name: str,
            icon_custom_emoji_id: str
    ) -> bool:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_EDIT_FORUM_TOPIC, data=data)
        assert isinstance(response, bool)
        return response

    async def close_forum_topic(
            self,
            chat_id: Union[int, str],
            message_thread_id: int
    ) -> bool:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_CLOSE_FORUM_TOPIC, data=data)
        assert isinstance(response, bool)
        return response

    async def reopen_forum_topic(
            self,
            chat_id: Union[int, str],
            message_thread_id: int
    ) -> bool:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_REOPEN_FORUM_TOPIC, data=data)
        assert isinstance(response, bool)
        return response

    async def delete_forum_topic(
            self,
            chat_id: Union[int, str],
            message_thread_id: int
    ):

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_DELETE_FORUM_TOPIC, data=data)
        assert isinstance(response, bool)
        return response

    async def unpin_all_forum_topic_messages(
            self,
            chat_id: Union[int, str],
            message_thread_id: int
    ):

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_UNPIN_ALL_FORUM_TOPIC_MESSAGES, data=data)
        assert isinstance(response, bool)
        return response

    async def answer_callback_query(
            self,
            callback_query_id: str,
            text: Optional[str] = None,
            show_alert: Optional[bool] = None,
            url: Optional[str] = None,
            cache_time: Optional[int] = None
    ) -> bool:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_ANSWER_CALLBACK_QUERY, data=data)
        assert isinstance(response, bool)
        return response

    async def set_my_commands(
            self,
            commands: List[BotCommand],
            scope: Optional[BotCommandScope] = None,
            language_code: Optional[str] = None
    ) -> bool:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SET_MY_COMMANDS, data=data)
        assert isinstance(response, bool)
        return response

    async def delete_my_commands(
            self,
            scope: Optional[BotCommandScope] = None,
            language_code: Optional[str] = None
    ) -> bool:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_DELETE_MY_COMMANDS, data=data)
        assert isinstance(response, bool)
        return response

    async def get_my_commands(
            self,
            scope: Optional[BotCommandScope] = None,
            language_code: Optional[str] = None
    ) -> List[BotCommand]:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_GET_MY_COMMANDS, data=data)
        return [BotCommand.from_dict(r) for r in response]

    async def set_chat_menu_button(
            self,
            chat_id: Optional[int] = None,
            menu_button: Optional[MenuButton] = None
    ) -> bool:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SET_CHAT_MENU_BUTTON, data=data)
        assert isinstance(response, bool)
        return response

    async def get_chat_menu_button(self, chat_id: Optional[int] = None) -> MenuButton:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_GET_CHAT_MENU_BUTTON, data=data)
        return MenuButton.from_dict(response)

    async def set_my_default_administrator_rights(
            self,
            rights: Optional[ChatAdministratorRights] = None,
            for_channels: Optional[bool] = None
    ) -> bool:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SET_MY_DEFAULT_ADMINISTRATOR_RIGHTS, data=data)
        assert isinstance(response, bool)
        return response

    async def get_my_default_administrator_rights(
            self,
            for_channels: Optional[bool] = None
    ) -> ChatAdministratorRights:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_GET_MY_DEFAULT_ADMINISTRATOR_RIGHTS, data=data)
        return ChatAdministratorRights.from_dict(response)

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

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_EDIT_MESSAGE_TEXT, data=data)

        if isinstance(response, bool):
            return response

        return Message.from_dict(response)

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

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_EDIT_MESSAGE_CAPTION, data=data)

        if isinstance(response, bool):
            return response

        return Message.from_dict(response)

    async def edit_message_media(
            self,
            media: InputMedia,
            chat_id: Union[int, str, None] = None,
            message_id: Optional[int] = None,
            inline_message_id: Optional[str] = None,
            reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, bool]:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_EDIT_MESSAGE_MEDIA, data=data)

        if isinstance(response, bool):
            return response

        return Message.from_dict(response)

    async def edit_message_reply_markup(
            self,
            chat_id: Union[int, str, None] = None,
            message_id: Optional[int] = None,
            inline_message_id: Optional[str] = None,
            reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, bool]:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_EDIT_MESSAGE_REPLY_MARKUP, data=data)

        if isinstance(response, bool):
            return response

        return Message.from_dict(response)

    async def stop_poll(
            self,
            chat_id: Union[int, str],
            message_id: int,
            reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Poll:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_STOP_POLL, data=data)
        return Poll.from_dict(response)

    async def delete_message(
            self,
            chat_id: Union[int, str],
            message_id: int
    ) -> bool:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_DELETE_MESSAGE, data=data)
        assert isinstance(response, bool)
        return response

    async def send_sticker(
            self,
            chat_id: Union[int, str],
            sticker: InputFile,
            message_thread_id: Optional[int] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply] = None
    ) -> Message:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SEND_STICKER, data=data)
        return Message.from_dict(response)

    async def get_sticker_set(self, name: str) -> StickerSet:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_GET_STICKER_SET, data=data)
        return StickerSet.from_dict(response)

    async def get_custom_emoji_stickers(self, custom_emoji_ids: List[str]) -> List[Sticker]:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_GET_CUSTOM_EMOJI_STICKERS, data=data)
        return [Sticker.from_dict(r) for r in response]

    async def upload_sticker_file(self, user_id: int, png_sticker: InputFile) -> File:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_UPLOAD_STICKER_FILE, data=data)
        return File.from_dict(response)

    async def create_new_sticker_set(
            self,
            user_id: int,
            name: str,
            title: str,
            emojis: str,
            png_sticker: Optional[InputFile] = None,
            tgs_sticker: Optional[InputFile] = None,
            webm_sticker: Optional[InputFile] = None,
            sticker_type: Optional[constants.StickerType] = None,
            mask_position: Optional[MaskPosition] = None
    ) -> bool:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_CREATE_NEW_STICKER_SET, data=data)
        assert isinstance(response, bool)
        return response

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

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_ADD_STICKER_TO_SET, data=data)
        assert isinstance(response, bool)
        return response

    async def set_sticker_position_in_set(
            self,
            sticker: str,
            position: int
    ) -> bool:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SET_STICKER_POSITION_IN_SET, data=data)
        assert isinstance(response, bool)
        return response

    async def delete_sticker_from_set(self, sticker: str) -> bool:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_DELETE_STICKER_FROM_SET, data=data)
        assert isinstance(response, bool)
        return response

    async def set_sticker_set_thumb(
            self,
            name: str,
            user_id: int,
            thumb: Optional[InputFile] = None
    ) -> bool:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SET_STICKER_SET_THUMB, data=data)
        assert isinstance(response, bool)
        return response

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

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_ANSWER_INLINE_QUERY, data=data)
        assert isinstance(response, bool)
        return response

    async def answer_web_app_query(
            self,
            web_app_query_id: str,
            result: InlineQueryResult
    ) -> SentWebAppMessage:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_ANSWER_WEB_APP_QUERY, data=data)
        return SentWebAppMessage.from_dict(response)

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

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SEND_INVOICE, data=data)
        return Message.from_dict(response)

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

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_CREATE_INVOICE_LINK, data=data)
        assert isinstance(response, str)
        return response

    async def answer_shipping_query(
            self,
            shipping_query_id: str,
            ok: bool,
            shipping_options: Optional[List[ShippingOption]] = None,
            error_message: Optional[str] = None
    ) -> bool:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_ANSWER_SHIPPING_QUERY, data=data)
        assert isinstance(response, bool)
        return response

    async def answer_pre_checkout_query(
            self,
            pre_checkout_query_id: str,
            ok: bool,
            error_message: Optional[str] = None
    ) -> bool:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_ANSWER_PRE_CHECKOUT_QUERY, data=data)
        assert isinstance(response, bool)
        return response

    async def set_passport_data_errors(
            self,
            user_id: int,
            errors: List[PassportElementError]
    ) -> bool:
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SET_PASSPORT_DATA_ERRORS, data=data)
        assert isinstance(response, bool)
        return response

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

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SEND_GAME, data=data)
        return Message.from_dict(response)

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

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_SET_GAME_HIGH_SCORE, data=data)

        if isinstance(response, bool):
            return response

        return Message.from_dict(response)

    async def get_game_high_scores(
            self,
            user_id: int,
            chat_id: Optional[int] = None,
            message_id: Optional[int] = None,
            inline_message_id: Optional[str] = None
    ) -> List[GameHighScore]:

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        response = await self._request(constants.API_METHOD_GET_GAME_HIGH_SCORES, data=data)
        return [GameHighScore.from_dict(r) for r in response]
